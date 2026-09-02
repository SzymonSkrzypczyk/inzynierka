// Command recovery restores space-weather archives from Dropbox to PostgreSQL.
package main

import (
	"errors"
	"flag"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/SzymonSkrzypczyk/db/database"
	"github.com/SzymonSkrzypczyk/db/dropbox"
	"github.com/SzymonSkrzypczyk/db/extract"
	"github.com/SzymonSkrzypczyk/db/secrets"
	"github.com/SzymonSkrzypczyk/db/utils"
)

func parseArgs(args []string) (string, error) {
	flags := flag.NewFlagSet("recovery", flag.ContinueOnError)
	flags.SetOutput(os.Stderr)
	date := flags.String("date", "", "restore one archive in YYYY-MM-DD format")
	if err := flags.Parse(args); err != nil {
		return "", err
	}
	if flags.NArg() != 0 {
		return "", fmt.Errorf("unexpected argument: %s", flags.Arg(0))
	}
	if *date == "" {
		return "", nil
	}
	if _, err := time.Parse("2006-01-02", *date); err != nil {
		return "", fmt.Errorf("invalid --date %q: use YYYY-MM-DD", *date)
	}
	return *date, nil
}

func run(args []string) error {
	targetDate, err := parseArgs(args)
	if err != nil {
		return err
	}
	defer func() {
		if err := utils.RemoveDataDirectory(extract.DataDirectory); err != nil {
			log.Printf("cleanup failed: %v", err)
		}
	}()

	dropboxAppSecret, dropboxAppKey, dropboxRefreshToken := secrets.LoadSecrets()
	accessToken, err := secrets.GetAccessToken(dropboxAppKey, dropboxAppSecret, dropboxRefreshToken)
	if err != nil {
		return fmt.Errorf("get Dropbox access token: %w", err)
	}

	tempFilePath, err := dropbox.DownloadFromDropboxWithTargetDate(accessToken, targetDate)
	if err != nil {
		return fmt.Errorf("download Dropbox archive: %w", err)
	}
	if tempFilePath != extract.AlreadyProcessedMessage {
		defer os.Remove(tempFilePath)
	}
	if err := extract.ExtractZipContents(tempFilePath, targetDate); err != nil {
		return fmt.Errorf("extract Dropbox archive: %w", err)
	}

	db, err := database.InitDatabase()
	if err != nil {
		return fmt.Errorf("initialize database: %w", err)
	}
	if err := database.ProcessDailyData(db, targetDate); err != nil {
		return err
	}
	return nil
}

func main() {
	if err := run(os.Args[1:]); err != nil {
		if !errors.Is(err, flag.ErrHelp) {
			log.Printf("Recovery failed: %v", err)
		}
		os.Exit(1)
	}
	fmt.Println("Recovery completed successfully.")
}
