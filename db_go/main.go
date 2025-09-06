package main

import (
	"db/database"
	"db/extract"
	_ "db/extract"
	"db/secrets"
	"db/utils"
	"fmt"
	"github.com/dropbox/dropbox-sdk-go-unofficial/v6/dropbox"
	"github.com/dropbox/dropbox-sdk-go-unofficial/v6/dropbox/files"
	"log"
	"os"
)

func main() {
	dropboxAppSecret, dropboxAppKey, dropboxRefreshToken := secrets.LoadSecrets()

	// Get access token from refresh token
	accessToken, err := secrets.GetAccessToken(dropboxAppKey, dropboxAppSecret, dropboxRefreshToken)
	if err != nil {
		log.Fatalf("Failed to get access token: %v", err)
	}

	downloadDirectory := files.DownloadZipArg{
		Path: "/inzynierka",
	}

	config := dropbox.Config{
		Token:    accessToken,
		LogLevel: dropbox.LogInfo,
	}
	client := files.New(config)
	fmt.Println("Downloading files from path:", downloadDirectory.Path)

	res, content, err := client.DownloadZip(&downloadDirectory)

	if err != nil {
		log.Fatal(err)
	}
	defer content.Close()

	tempFilePath, err := extract.DownloadFromDropbox(content)
	if err != nil {
		log.Fatalf("Failed to download from Dropbox: %v", err)
	}
	// Extract the contents of the downloaded zip
	if err := extract.ExtractZipContents(tempFilePath); err != nil {
		log.Fatalf("Failed to extract zip contents: %v", err)
	}

	// Initialize database connection
	db, err := database.InitDatabase()
	if err != nil {
		log.Fatalf("Failed to initialize database: %v", err)
	}

	// Process and save daily data to database
	err = database.ProcessDailyData(db)
	if err != nil {
		log.Fatalf("Failed to process daily data: %v", err)
	}

	fmt.Println("All operations completed successfully!")
	fmt.Printf("Response: %+v\n", res)

	err = utils.RemoveDataDirectory(extract.DataDirectory)
	if err != nil {
		os.Exit(1)
	}
}
