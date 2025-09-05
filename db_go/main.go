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

func listZipContents(zipFilePath string) error {
	// Open zip file
	reader, err := zip.OpenReader(zipFilePath)
	if err != nil {
		return err
	}
	defer reader.Close()

	fmt.Println("\n=== ZIP CONTENTS ===")
	fmt.Printf("Total files/directories: %d\n\n", len(reader.File))

	// Track directories
	directories := make(map[string]bool)

	for _, file := range reader.File {
		fmt.Printf("Name: %s\n", file.Name)
		fmt.Printf("  Size: %d bytes\n", file.UncompressedSize64)
		fmt.Printf("  Modified: %s\n", file.Modified)

		if file.FileInfo().IsDir() {
			fmt.Printf("  Type: Directory\n")
			directories[file.Name] = true
		} else {
			fmt.Printf("  Type: File\n")
			// Add parent directories
			dir := filepath.Dir(file.Name)
			for dir != "." && dir != "/" {
				directories[dir+"/"] = true
				dir = filepath.Dir(dir)
			}
		}
		fmt.Println()
	}

	// List unique directories
	if len(directories) > 0 {
		fmt.Println("=== DIRECTORIES FOUND ===")
		for dir := range directories {
			fmt.Printf("📁 %s\n", dir)
		}
	} else {
		fmt.Println("No directories found in zip file")
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

	// List the contents of the downloaded zip
	if err := listZipContents(tempFilePath); err != nil {
		log.Printf("Failed to list zip contents: %v", err)
	}

	fmt.Println("Response:", res)
}
