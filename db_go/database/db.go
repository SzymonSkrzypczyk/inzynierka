package database

import (
	"db/extract"
	"encoding/csv"
	"encoding/json"
	"fmt"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"log"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"time"
)

// Database functions
func InitDatabase() (*gorm.DB, error) {
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

func ProcessDailyData(db *gorm.DB) error {
	fmt.Println("\n=== PROCESSING DAILY DATA TO DATABASE ===")

	// Read all directories in the data folder
	entries, err := os.ReadDir(extract.DataDirectory)
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

		dayDir := filepath.Join(extract.DataDirectory, dateStr)
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
