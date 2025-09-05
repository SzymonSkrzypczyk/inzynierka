package main

import (
	"archive/zip"
	"encoding/json"
	"fmt"
	"github.com/dropbox/dropbox-sdk-go-unofficial/v6/dropbox"
	_ "github.com/dropbox/dropbox-sdk-go-unofficial/v6/dropbox"
	"github.com/dropbox/dropbox-sdk-go-unofficial/v6/dropbox/files"
	_ "github.com/dropbox/dropbox-sdk-go-unofficial/v6/dropbox/files"
	"io"
	"log"
	"net/http"
	"net/url"
	"os"
	"path/filepath"
	"strings"
	"time"
)

const DATA_DIRECTORY = "./data"

type TokenResponse struct {
	AccessToken string `json:"access_token"`
	TokenType   string `json:"token_type"`
	ExpiresIn   int    `json:"expires_in"`
}

func getAccessToken(appKey, appSecret, refreshToken string) (string, error) {
	data := url.Values{}
	data.Set("grant_type", "refresh_token")
	data.Set("refresh_token", refreshToken)
	data.Set("client_id", appKey)
	data.Set("client_secret", appSecret)

	req, err := http.NewRequest("POST", "https://api.dropbox.com/oauth2/token", strings.NewReader(data.Encode()))
	if err != nil {
		return "", err
	}
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}

	if resp.StatusCode != 200 {
		return "", fmt.Errorf("failed to get access token: %s", string(body))
	}

	var tokenResp TokenResponse
	err = json.Unmarshal(body, &tokenResp)
	if err != nil {
		return "", err
	}

	return tokenResp.AccessToken, nil
}

func loadSecrets() (DropboxAppSecret, DropboxAppKey, DropboxRefreshToken string) {
	DropboxAppKey = os.Getenv("DROPBOX_APP_KEY")
	if DropboxAppKey == "" {
		fmt.Println("DROPBOX_APP_KEY environment variable not set")
		os.Exit(1)
	}
	DropboxAppSecret = os.Getenv("DROPBOX_APP_SECRET")
	if DropboxAppSecret == "" {
		fmt.Println("DROPBOX_APP_SECRET environment variable not set")
		os.Exit(1)
	}
	DropboxRefreshToken = os.Getenv("DROPBOX_REFRESH_TOKEN")
	if DropboxRefreshToken == "" {
		fmt.Println("DROPBOX_REFRESH_TOKEN environment variable not set")
		os.Exit(1)
	}

	return
}

func extractZipContents(zipFilePath string) error {
	err := os.MkdirAll(DATA_DIRECTORY, 0755)
	if err != nil {
		return fmt.Errorf("failed to create data directory: %v", err)
	}

	reader, err := zip.OpenReader(zipFilePath)
	if err != nil {
		return err
	}
	defer reader.Close()

	fmt.Println("\n=== EXTRACTING ZIP CONTENTS ===")
	fmt.Printf("Total files: %d\n", len(reader.File))
	fmt.Printf("Extracting to: %s\n\n", DATA_DIRECTORY)

	for _, file := range reader.File {
		if file.FileInfo().IsDir() {
			continue
		}

		fmt.Printf("Extracting: %s\n", file.Name)

		rc, err := file.Open()
		if err != nil {
			return fmt.Errorf("failed to open file %s in zip: %v", file.Name, err)
		}

		fileName := filepath.Base(file.Name)
		destPath := filepath.Join(DATA_DIRECTORY, fileName)

		destFile, err := os.Create(destPath)
		if err != nil {
			rc.Close()
			return fmt.Errorf("failed to create destination file %s: %v", destPath, err)
		}

		_, err = io.Copy(destFile, rc)
		rc.Close()
		destFile.Close()

		if err != nil {
			return fmt.Errorf("failed to copy file %s: %v", file.Name, err)
		}

		fmt.Printf("  → Saved as: %s\n", destPath)

		if strings.HasSuffix(strings.ToLower(fileName), ".zip") {
			fmt.Printf("  → Detected nested zip, extracting contents...\n")
			err = extractNestedZip(destPath, DATA_DIRECTORY)
			if err != nil {
				log.Printf("Warning: failed to extract nested zip %s: %v", fileName, err)
			}
		}
	}

	fmt.Println("\n=== EXTRACTION COMPLETE ===")
	return nil
}

func extractNestedZip(zipPath, baseDataDir string) error {
	reader, err := zip.OpenReader(zipPath)
	if err != nil {
		return err
	}
	defer reader.Close()

	zipName := strings.TrimSuffix(filepath.Base(zipPath), ".zip")
	subDir := filepath.Join(baseDataDir, zipName)
	err = os.MkdirAll(subDir, 0755)
	if err != nil {
		return fmt.Errorf("failed to create subdirectory %s: %v", subDir, err)
	}

	fmt.Printf("    → Extracting %d files to: %s\n", len(reader.File), subDir)

	for _, file := range reader.File {
		// Skip directories
		if file.FileInfo().IsDir() {
			continue
		}

		rc, err := file.Open()
		if err != nil {
			return fmt.Errorf("failed to open nested file %s: %v", file.Name, err)
		}

		fileName := filepath.Base(file.Name)
		destPath := filepath.Join(subDir, fileName)
		destFile, err := os.Create(destPath)
		if err != nil {
			rc.Close()
			return fmt.Errorf("failed to create nested file %s: %v", destPath, err)
		}

		_, err = io.Copy(destFile, rc)
		rc.Close()
		destFile.Close()

		if err != nil {
			return fmt.Errorf("failed to copy nested file %s: %v", file.Name, err)
		}

		fmt.Printf("    → %s\n", destPath)
	}

	return nil
}

func main() {
	dropboxAppSecret, dropboxAppKey, dropboxRefreshToken := loadSecrets()

	// Get access token from refresh token
	accessToken, err := getAccessToken(dropboxAppKey, dropboxAppSecret, dropboxRefreshToken)
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

	// Create a temporary directory holding the daily reports
	tempDir := os.TempDir()
	timestamp := time.Now().Format("20060102_150405")
	tempFileName := fmt.Sprintf("dropbox_inzynierka_%s.zip", timestamp)
	tempFilePath := filepath.Join(tempDir, tempFileName)

	tempFile, err := os.Create(tempFilePath)
	if err != nil {
		log.Fatalf("Failed to create temp file: %v", err)
	}
	defer tempFile.Close()

	bytesWritten, err := io.Copy(tempFile, content)
	if err != nil {
		log.Fatalf("Failed to write zip content to temp file: %v", err)
	}

	fmt.Println("Download successful!")
	fmt.Printf("Zip file saved to: %s\n", tempFilePath)
	fmt.Printf("File size: %d bytes\n", bytesWritten)

	// Extract the contents of the downloaded zip
	if err := extractZipContents(tempFilePath); err != nil {
		log.Fatalf("Failed to extract zip contents: %v", err)
	}

	fmt.Println("Response:", res)
}
