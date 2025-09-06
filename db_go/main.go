package main

import (
	"archive/zip"
	"encoding/csv"
	"encoding/json"
	"fmt"
	"github.com/dropbox/dropbox-sdk-go-unofficial/v6/dropbox"
	"github.com/dropbox/dropbox-sdk-go-unofficial/v6/dropbox/files"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"io"
	"log"
	"net/http"
	"net/url"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"time"
)

const (
	DataDirectory           = "./data"
	AlreadyProcessedMessage = "Already Processed Skipping..." // Message indicating already processed data
)

// Example Database Models
type SpaceWeatherData struct {
	ID        uint      `gorm:"primaryKey"`
	Date      time.Time `gorm:"index"`
	DataType  string    `gorm:"index"`
	TimeTag   time.Time
	Data      string `gorm:"type:jsonb"` // Store CSV data as JSON
	CreatedAt time.Time
}

type ProcessingLog struct {
	ID          uint   `gorm:"primaryKey"`
	Date        string `gorm:"uniqueIndex"`
	FilesCount  int
	ProcessedAt time.Time
	Status      string
}

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

func downloadFromDropbox(content io.Reader) (string, error) {
	// Create a temporary directory holding the daily reports

	fileInfo, err := os.Stat(DataDirectory)
	if err == nil && !fileInfo.IsDir() {
		return "", fmt.Errorf("data directory %s exists and is not a directory", DataDirectory)
	} else if err == nil {
		fmt.Printf("Data directory %s already exists, skipping extraction\n", DataDirectory)
		return AlreadyProcessedMessage, nil
	}

	tempDir := os.TempDir()
	timestamp := time.Now().Format("20060102_150405")
	tempFileName := fmt.Sprintf("dropbox_inzynierka_%s.zip", timestamp)
	tempFilePath := filepath.Join(tempDir, tempFileName)

	tempFile, err := os.Create(tempFilePath)
	if err != nil {
		log.Fatalf("Failed to create temp file: %v", err)
		return "", err
	}

	// extra defer to ensure file is closed
	defer func(tempFile *os.File) {
		err := tempFile.Close()
		if err != nil {
			log.Fatalf("Failed to close temp file: %v", err)
		}
	}(tempFile)

	bytesWritten, err := io.Copy(tempFile, content)
	if err != nil {
		log.Fatalf("Failed to write zip content to temp file: %v", err)
		return "", err
	}

	fmt.Println("Download successful!")
	fmt.Printf("Zip file saved to: %s\n", tempFilePath)
	fmt.Printf("File size: %d bytes\n", bytesWritten)

	return tempFilePath, nil
}

func extractZipContents(zipFilePath string) error {
	if zipFilePath == AlreadyProcessedMessage {
		fmt.Println("Data already processed, skipping zip extraction")
		return nil
	}
	err := os.MkdirAll(DataDirectory, 0755)
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
	fmt.Printf("Extracting to: %s\n\n", DataDirectory)

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
		destPath := filepath.Join(DataDirectory, fileName)

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
			err = extractNestedZip(destPath, DataDirectory)
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

// Database functions
func initDatabase() (*gorm.DB, error) {
	// Get database connection string from environment variables
	dbHost := os.Getenv("DB_HOST")
	if dbHost == "" {
		dbHost = "localhost"
	}
	dbUser := os.Getenv("DB_USER")
	if dbUser == "" {
		dbUser = "postgres"
	}
	dbPassword := os.Getenv("DB_PASSWORD")
	if dbPassword == "" {
		dbPassword = "postgres"
	}
	dbName := os.Getenv("DB_NAME")
	if dbName == "" {
		dbName = "postgres"
	}
	dbPort := os.Getenv("DB_PORT")
	if dbPort == "" {
		dbPort = "5432"
	}

	dsn := fmt.Sprintf("host=%s user=%s password=%s dbname=%s port=%s sslmode=disable",
		dbHost, dbUser, dbPassword, dbName, dbPort)

	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		return nil, fmt.Errorf("failed to connect to database: %v", err)
	}

	// Auto-migrate the schema
	err = db.AutoMigrate(&SpaceWeatherData{}, &ProcessingLog{})
	if err != nil {
		return nil, fmt.Errorf("failed to migrate database schema: %v", err)
	}

	fmt.Println("Database connection established and schema migrated successfully")
	return db, nil
}

func processCSVFile(filePath string, dataType string, date time.Time) ([]map[string]interface{}, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, fmt.Errorf("failed to open CSV file %s: %v", filePath, err)
	}
	defer file.Close()

	reader := csv.NewReader(file)
	records, err := reader.ReadAll()
	if err != nil {
		return nil, fmt.Errorf("failed to read CSV file %s: %v", filePath, err)
	}

	if len(records) < 1 {
		return nil, fmt.Errorf("CSV file %s is empty", filePath)
	}

	headers := records[0]
	var data []map[string]interface{}

	for i, record := range records[1:] {
		if len(record) != len(headers) {
			log.Printf("Warning: Record %d in %s has different number of columns than headers", i+1, filePath)
			continue
		}

		row := make(map[string]interface{})
		for j, value := range record {
			if j < len(headers) {
				// Try to parse as number first, otherwise keep as string
				if floatVal, err := strconv.ParseFloat(value, 64); err == nil {
					row[headers[j]] = floatVal
				} else {
					row[headers[j]] = value
				}
			}
		}
		data = append(data, row)
	}

	return data, nil
}

func saveDataToDatabase(db *gorm.DB, date time.Time, dataType string, data []map[string]interface{}) error {
	jsonData, err := json.Marshal(data)
	if err != nil {
		return fmt.Errorf("failed to marshal data to JSON: %v", err)
	}

	// Extract time_tag from first record if available
	var timeTag time.Time
	if len(data) > 0 {
		if timeTagStr, ok := data[0]["time_tag"].(string); ok {
			if parsedTime, err := time.Parse(time.RFC3339, timeTagStr); err == nil {
				timeTag = parsedTime
			}
		}
	}

	spaceWeatherData := SpaceWeatherData{
		Date:      date,
		DataType:  dataType,
		TimeTag:   timeTag,
		Data:      string(jsonData),
		CreatedAt: time.Now(),
	}

	result := db.Create(&spaceWeatherData)
	if result.Error != nil {
		return fmt.Errorf("failed to save data to database: %v", result.Error)
	}

	fmt.Printf("Saved %s data for %s to database (ID: %d)\n", dataType, date.Format("2006-01-02"), spaceWeatherData.ID)
	return nil
}

func processDailyData(db *gorm.DB) error {
	fmt.Println("\n=== PROCESSING DAILY DATA TO DATABASE ===")

	// Read all directories in the data folder
	entries, err := os.ReadDir(DataDirectory)
	if err != nil {
		return fmt.Errorf("failed to read data directory: %v", err)
	}

	for _, entry := range entries {
		if !entry.IsDir() {
			continue
		}

		dateStr := entry.Name()
		date, err := time.Parse("2006-01-02", dateStr)
		if err != nil {
			log.Printf("Skipping directory %s: not a valid date format", dateStr)
			continue
		}

		// Check if this date has already been processed
		var existingLog ProcessingLog
		result := db.Where("date = ?", dateStr).First(&existingLog)
		if result.Error == nil {
			fmt.Printf("Date %s already processed, skipping...\n", dateStr)
			continue
		}

		fmt.Printf("\nProcessing data for date: %s\n", dateStr)

		dayDir := filepath.Join(DataDirectory, dateStr)
		files, err := os.ReadDir(dayDir)
		if err != nil {
			log.Printf("Failed to read directory %s: %v", dayDir, err)
			continue
		}

		filesProcessed := 0
		for _, file := range files {
			if file.IsDir() || !strings.HasSuffix(file.Name(), ".csv") {
				continue
			}

			filePath := filepath.Join(dayDir, file.Name())

			// Extract data type from filename (remove date suffix)
			dataType := strings.TrimSuffix(file.Name(), "_"+dateStr+".csv")

			fmt.Printf("  Processing: %s (type: %s)\n", file.Name(), dataType)

			data, err := processCSVFile(filePath, dataType, date)
			if err != nil {
				log.Printf("    Error processing %s: %v", file.Name(), err)
				continue
			}

			err = saveDataToDatabase(db, date, dataType, data)
			if err != nil {
				log.Printf("    Error saving %s to database: %v", file.Name(), err)
				continue
			}

			filesProcessed++
		}

		// Log the processing
		processingLog := ProcessingLog{
			Date:        dateStr,
			FilesCount:  filesProcessed,
			ProcessedAt: time.Now(),
			Status:      "completed",
		}

		result = db.Create(&processingLog)
		if result.Error != nil {
			log.Printf("Failed to log processing for date %s: %v", dateStr, result.Error)
		}

		fmt.Printf("  Completed processing %d files for %s\n", filesProcessed, dateStr)
	}

	fmt.Println("\n=== DATABASE PROCESSING COMPLETE ===")
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

	tempFilePath, err := downloadFromDropbox(content)
	if err != nil {
		log.Fatalf("Failed to download from Dropbox: %v", err)
	}
	// Extract the contents of the downloaded zip
	if err := extractZipContents(tempFilePath); err != nil {
		log.Fatalf("Failed to extract zip contents: %v", err)
	}

	// Initialize database connection
	db, err := initDatabase()
	if err != nil {
		log.Fatalf("Failed to initialize database: %v", err)
	}

	// Process and save daily data to database
	err = processDailyData(db)
	if err != nil {
		log.Fatalf("Failed to process daily data: %v", err)
	}

	fmt.Println("All operations completed successfully!")
	fmt.Printf("Response: %+v\n", res)
}
