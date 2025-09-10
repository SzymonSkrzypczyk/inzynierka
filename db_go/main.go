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
	"strings"
	"time"
)

func main() {
	// Check for optional date argument
	var targetDate string
	if len(os.Args) > 1 {
		dateArg := os.Args[1]
		// Validate date format
		if _, err := time.Parse("2006-01-02", dateArg); err != nil {
			log.Fatalf("Invalid date format. Please use YYYY-MM-DD format. Example: 2025-05-19")
		}
		targetDate = dateArg
		fmt.Printf("Processing data for specific date: %s\n", targetDate)
	} else {
		fmt.Println("No specific date provided. Processing all available dates.")
	}

	dropboxAppSecret, dropboxAppKey, dropboxRefreshToken := secrets.LoadSecrets()

	// Get access token from refresh token
	accessToken, err := secrets.GetAccessToken(dropboxAppKey, dropboxAppSecret, dropboxRefreshToken)
	if err != nil {
		log.Fatalf("Failed to get access token: %v", err)
	}

	config := dropbox.Config{
		Token:    accessToken,
		LogLevel: dropbox.LogInfo,
	}
	client := files.New(config)

	// Set download path based on whether target date is specified
	var downloadPath string
	if targetDate != "" {
		// Check if the target date exists as either a zip file or folder
		listArg := files.ListFolderArg{
			Path: "/inzynierka",
		}

		listResult, err := client.ListFolder(&listArg)
		if err != nil {
			log.Printf("Warning: Could not list /inzynierka directory: %v", err)
			// Fallback to trying the zip file directly
			downloadPath = "/inzynierka/" + targetDate + ".zip"
		} else {
			found := false
			expectedZipName := targetDate + ".zip"

			// Check for zip file first, then folder
			for _, entry := range listResult.Entries {
				switch e := entry.(type) {
				case *files.FileMetadata:
					if e.Name == expectedZipName {
						downloadPath = "/inzynierka/" + expectedZipName
						found = true
						break
					}
				case *files.FolderMetadata:
					if e.Name == targetDate {
						downloadPath = "/inzynierka/" + targetDate
						found = true
						break
					}
				}
			}

			if !found {
				log.Fatalf("Target date '%s' not found in Dropbox (looked for '%s' file or '%s' folder).", targetDate, expectedZipName, targetDate)
			}
		}

	} else {
		downloadPath = "/inzynierka"
	}

	fmt.Println("Downloading files from path:", downloadPath)

	// Use different download methods based on what we're downloading
	var tempFilePath string
	if targetDate != "" && strings.HasSuffix(downloadPath, ".zip") {
		// Downloading a single zip file - use Download method
		downloadArg := files.DownloadArg{
			Path: downloadPath,
		}

		_, content, err := client.Download(&downloadArg)
		if err != nil {
			log.Fatal(err)
		}
		defer content.Close()

		tempFilePath, err = extract.DownloadFromDropbox(content)
		if err != nil {
			log.Fatalf("Failed to download from Dropbox: %v", err)
		}
	} else {
		// Downloading a folder - use DownloadZip method
		downloadDirectory := files.DownloadZipArg{
			Path: downloadPath,
		}

		res, content, err := client.DownloadZip(&downloadDirectory)
		if err != nil {
			log.Fatal(err)
		}
		defer content.Close()

		tempFilePath, err = extract.DownloadFromDropbox(content)
		if err != nil {
			log.Fatalf("Failed to download from Dropbox: %v", err)
		}

		fmt.Printf("Response: %+v\n", res)
	}

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
