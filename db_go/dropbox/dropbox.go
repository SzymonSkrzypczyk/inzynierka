package dropbox

import (
	"db/extract"
	"fmt"
	"github.com/dropbox/dropbox-sdk-go-unofficial/v6/dropbox"
	"github.com/dropbox/dropbox-sdk-go-unofficial/v6/dropbox/files"
	"log"
	"strings"
)

func DownloadFromDropbox(tempFilePath *string, accessToken, targetDate string) error {
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
				return fmt.Errorf("target date '%s' not found in Dropbox (looked for '%s' file or '%s' folder)", targetDate, expectedZipName, targetDate)
			}
		}
	} else {
		downloadPath = "/inzynierka"
	}

	fmt.Println("Downloading files from path:", downloadPath)

	// Use different download methods based on what we're downloading
	if targetDate != "" && strings.HasSuffix(downloadPath, ".zip") {
		// Downloading a single zip file - use Download method
		downloadArg := files.DownloadArg{
			Path: downloadPath,
		}

		_, content, err := client.Download(&downloadArg)
		if err != nil {
			return fmt.Errorf("failed to download file: %v", err)
		}
		defer content.Close()

		filePath, err := extract.DownloadFromDropbox(content)
		if err != nil {
			return fmt.Errorf("failed to save downloaded content: %v", err)
		}
		*tempFilePath = filePath
	} else {
		// Downloading a folder - use DownloadZip method
		downloadDirectory := files.DownloadZipArg{
			Path: downloadPath,
		}

		_, content, err := client.DownloadZip(&downloadDirectory)
		if err != nil {
			return fmt.Errorf("failed to download zip: %v", err)
		}
		defer content.Close()

		filePath, err := extract.DownloadFromDropbox(content)
		if err != nil {
			return fmt.Errorf("failed to save downloaded content: %v", err)
		}
		*tempFilePath = filePath
	}

	return nil
}

func DownloadFromDropboxWithTargetDate(accessToken, targetDate string) (string, error) {
	var tempFilePath string
	err := DownloadFromDropbox(&tempFilePath, accessToken, targetDate)
	return tempFilePath, err
}
