package main

import (
	"fmt"
	"github.com/SzymonSkrzypczyk/db_go/database"
	"github.com/SzymonSkrzypczyk/db_go/dropbox"
	"github.com/SzymonSkrzypczyk/db_go/extract"
	_ "github.com/SzymonSkrzypczyk/db_go/extract"
	"github.com/SzymonSkrzypczyk/db_go/secrets"
	"github.com/SzymonSkrzypczyk/db_go/utils"
	"log"
	"os"
	"time"
)

func main() {
	var targetDate string
	if len(os.Args) > 1 {
		dateArg := os.Args[1]
		// date format validation
		if _, err := time.Parse("2006-01-02", dateArg); err != nil {
			log.Fatalf("Invalid date format. Please use YYYY-MM-DD format. Example: 2025-05-19")
		}
		targetDate = dateArg
		fmt.Printf("Processing data for specific date: %s\n", targetDate)
	} else {
		fmt.Println("No specific date provided. Processing all available dates.")
	}

	dropboxAppSecret, dropboxAppKey, dropboxRefreshToken := secrets.LoadSecrets()

	// refresh token used to get dropbox access token
	accessToken, err := secrets.GetAccessToken(dropboxAppKey, dropboxAppSecret, dropboxRefreshToken)
	if err != nil {
		log.Fatalf("Failed to get access token: %v", err)
	}

	tempFilePath, err := dropbox.DownloadFromDropboxWithTargetDate(accessToken, targetDate)
	if err != nil {
		log.Fatalf("Failed to download from Dropbox: %v", err)
	}

	fmt.Printf("Downloaded file: %s\n", tempFilePath)

	// Extract the contents of the downloaded zip
	if err := extract.ExtractZipContents(tempFilePath, targetDate); err != nil {
		log.Fatalf("Failed to extract zip contents: %v", err)
	}

	// Initialize database connection
	db, err := database.InitDatabase()
	if err != nil {
		log.Fatalf("Failed to initialize database: %v", err)
	}

	// Process and save daily data to database
	err = database.ProcessDailyData(db, targetDate)
	if err != nil {
		log.Fatalf("Failed to process daily data: %v", err)
	}

	fmt.Println("All operations completed successfully!")

	err = utils.RemoveDataDirectory(extract.DataDirectory)
	if err != nil {
		os.Exit(1)
	}
}
