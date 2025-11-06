package database

import (
	"encoding/csv"
	"fmt"
	"github.com/SzymonSkrzypczyk/db/extract"
	"github.com/SzymonSkrzypczyk/db/utils"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"gorm.io/gorm/clause"
	"log"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"time"
)

// InitDatabase initializes the database connection and performs auto-migration
func InitDatabase() (*gorm.DB, error) {
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

	dsn := fmt.Sprintf("host=%s user=%s password=%s dbname=%s port=%s sslmode=require",
		dbHost, dbUser, dbPassword, dbName, dbPort)

	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		return nil, fmt.Errorf("failed to connect to database: %v", err)
	}

	// Auto-migrate the schema
	err = db.AutoMigrate(
		&BoulderKIndex1m{},
		&DscovrMag1s{},
		&Magnetometers1Day{},
		&PlanetaryKIndex1m{},
		&PrimaryIntegralProtons1Day{},
		&PrimaryXray1Day{},
		&SecondaryIntegralProtons1Day{},
		&SecondaryXray1Day{},
		&SolarRegions{},
		&ProcessingLog{},
	)
	if err != nil {
		return nil, fmt.Errorf("failed to migrate database schema: %v", err)
	}

	fmt.Println("Database connection established and schema migrated successfully")
	return db, nil
}

// saveDataToSpecificTable saves the parsed CSV records to the corresponding database table
func saveDataToSpecificTable(db *gorm.DB, dataType string, records [][]string) error {
	if len(records) < 2 {
		return nil
	}

	switch dataType {
	case "boulder_k_index_1m":
		var data []BoulderKIndex1m
		for _, record := range records[1:] {
			if timeTag, err := utils.ParseTime(record[0]); err == nil {
				if kIndex, err := strconv.ParseFloat(record[1], 32); err == nil {
					data = append(data, BoulderKIndex1m{
						TimeTag: timeTag,
						KIndex:  float32(kIndex),
					})
				}
			}
		}
		if len(data) > 0 {
			return db.Clauses(clause.OnConflict{DoNothing: true}).CreateInBatches(data, 1000).Error
		}

	case "dscovr_mag_1s":
		var data []DscovrMag1s
		for _, record := range records[1:] {
			if timeTag, err := utils.ParseTime(record[0]); err == nil && len(record) >= 12 {
				bt, _ := strconv.ParseFloat(record[1], 32)
				// bxGse, _ := strconv.ParseFloat(record[2], 32)  // Not in model
				// byGse, _ := strconv.ParseFloat(record[3], 32)  // Not in model
				// bzGse, _ := strconv.ParseFloat(record[4], 32)  // Not in model
				// thetaGse, _ := strconv.ParseFloat(record[5], 32)  // Not in model
				// phiGse, _ := strconv.ParseFloat(record[6], 32)  // Not in model
				bxGsm, _ := strconv.ParseFloat(record[7], 32)
				byGsm, _ := strconv.ParseFloat(record[8], 32)
				bzGsm, _ := strconv.ParseFloat(record[9], 32)
				// thetaGsm, _ := strconv.ParseFloat(record[10], 32)  // Not in model
				// phiGsm, _ := strconv.ParseFloat(record[11], 32)  // Not in model

				data = append(data, DscovrMag1s{
					TimeTag: timeTag,
					Bt:      float32(bt),
					BxGsm:   float32(bxGsm),
					ByGsm:   float32(byGsm),
					BzGsm:   float32(bzGsm),
				})
			}
		}
		if len(data) > 0 {
			return db.Clauses(clause.OnConflict{DoNothing: true}).CreateInBatches(data, 1000).Error
		}

	case "magnetometers-1-day":
		var data []Magnetometers1Day
		for _, record := range records[1:] {
			if timeTag, err := utils.ParseTime(record[0]); err == nil && len(record) >= 6 {
				satellite := utils.ParseInt8(record[1])
				// he, _ := strconv.ParseFloat(record[2], 32)  // Not in model
				// hp, _ := strconv.ParseFloat(record[3], 32)  // Not in model
				// hn, _ := strconv.ParseFloat(record[4], 32)  // Not in model
				total, _ := strconv.ParseFloat(record[5], 32)
				// arcJetFlag := utils.ParseBool(record[6])  // Not in model

				data = append(data, Magnetometers1Day{
					TimeTag:   timeTag,
					Satellite: satellite,
					Total:     float32(total),
				})
			}
		}
		if len(data) > 0 {
			return db.Clauses(clause.OnConflict{DoNothing: true}).CreateInBatches(data, 1000).Error
		}

	case "planetary_k_index_1m":
		var data []PlanetaryKIndex1m
		for _, record := range records[1:] {
			if timeTag, err := utils.ParseTime(record[0]); err == nil && len(record) >= 4 {
				kpIndex, _ := strconv.Atoi(record[1])
				estimatedKp, _ := strconv.ParseFloat(record[2], 32)

				data = append(data, PlanetaryKIndex1m{
					TimeTag:     timeTag,
					KpIndex:     int8(kpIndex),
					EstimatedKp: float32(estimatedKp),
					Kp:          record[3],
				})
			}
		}
		if len(data) > 0 {
			return db.Clauses(clause.OnConflict{DoNothing: true}).CreateInBatches(data, 1000).Error
		}

	case "solar_regions":
		var data []SolarRegions
		for _, record := range records[1:] {
			if observedDate, err := time.Parse("2006-01-02", record[0]); err == nil && len(record) >= 28 {
				region, _ := strconv.Atoi(record[1])
				// latitude := utils.ParseInt8Ptr(record[2])  // Not in model
				// longitude := utils.ParseInt8Ptr(record[3])  // Not in model
				// location := utils.ParseStringPtr(record[4])  // Not in model
				// carringtonLongitude := utils.ParseInt8Ptr(record[5])  // Not in model
				// oldCarringtonLongitude := utils.ParseInt8Ptr(record[6])  // Not in model
				area := utils.ParseInt16Ptr(record[7])
				// spotClass := utils.ParseStringPtr(record[8])  // Not in model
				// extent := utils.ParseInt8Ptr(record[9])  // Not in model
				// numberSpots := utils.ParseInt8Ptr(record[10])  // Not in model
				magClass := utils.ParseStringPtr(record[11])
				// magString := utils.ParseStringPtr(record[12])  // Not in model
				// status := utils.ParseStringPtr(record[13])  // Not in model
				// cXrayEvents := utils.ParseInt8Ptr(record[14])  // Not in model
				mXrayEvents := utils.ParseInt8Ptr(record[15])
				xXrayEvents := utils.ParseInt8Ptr(record[16])
				// protonEvents := utils.ParseStringPtr(record[17])  // Not in model
				// sFlares := utils.ParseInt8Ptr(record[18])  // Not in model
				// impulseFlares1 := utils.ParseInt8Ptr(record[19])  // Not in model
				// impulseFlares2 := utils.ParseInt8Ptr(record[20])  // Not in model
				// impulseFlares3 := utils.ParseInt8Ptr(record[21])  // Not in model
				// impulseFlares4 := utils.ParseInt8Ptr(record[22])  // Not in model
				// protons := utils.ParseStringPtr(record[23])  // Not in model
				// cFlareProbability := utils.ParseInt8Ptr(record[24])  // Not in model
				mFlareProbability := utils.ParseInt8Ptr(record[25])
				xFlareProbability := utils.ParseInt8Ptr(record[26])
				// protonProbability := utils.ParseInt8Ptr(record[27])  // Not in model
				// firstDate := utils.ParseTimePtr(record[28])  // Not in model

				data = append(data, SolarRegions{
					ObservedDate:      observedDate,
					Region:            int16(region),
					Area:              area,
					MagClass:          magClass,
					MXrayEvents:       mXrayEvents,
					XXrayEvents:       xXrayEvents,
					MFlareProbability: mFlareProbability,
					XFlareProbability: xFlareProbability,
				})
			}
		}
		if len(data) > 0 {
			return db.Clauses(clause.OnConflict{DoNothing: true}).CreateInBatches(data, 1000).Error
		}

	default:
		if strings.Contains(dataType, "protons") {
			return saveProtonData(db, dataType, records)
		} else if strings.Contains(dataType, "xray") {
			return saveXrayData(db, dataType, records)
		}
	}

	return nil
}

// saveProtonData saves proton data to the corresponding database table
func saveProtonData(db *gorm.DB, dataType string, records [][]string) error {
	switch {
	case strings.Contains(dataType, "primary-integral"):
		var data []PrimaryIntegralProtons1Day
		for _, record := range records[1:] {
			if timeTag, err := utils.ParseTime(record[0]); err == nil && len(record) >= 4 {
				satellite := utils.ParseInt8(record[1])
				energy := record[3]
				flux, _ := strconv.ParseFloat(record[2], 32)
				data = append(data, PrimaryIntegralProtons1Day{
					TimeTag:   timeTag,
					Satellite: satellite,
					Flux:      float32(flux),
					Energy:    energy,
				})
			}
		}
		if len(data) > 0 {
			return db.Clauses(clause.OnConflict{DoNothing: true}).CreateInBatches(data, 1000).Error
		}
	case strings.Contains(dataType, "secondary-integral"):
		var data []SecondaryIntegralProtons1Day
		for _, record := range records[1:] {
			if timeTag, err := utils.ParseTime(record[0]); err == nil && len(record) >= 4 {
				satellite := utils.ParseInt8(record[1])
				energy := record[3]
				flux, _ := strconv.ParseFloat(record[2], 32)
				data = append(data, SecondaryIntegralProtons1Day{
					TimeTag:   timeTag,
					Satellite: satellite,
					Flux:      float32(flux),
					Energy:    energy,
				})
			}
		}
		if len(data) > 0 {
			return db.Clauses(clause.OnConflict{DoNothing: true}).CreateInBatches(data, 1000).Error
		}
	}
	return nil
}

// saveXrayData saves X-ray data to the corresponding database table
func saveXrayData(db *gorm.DB, dataType string, records [][]string) error {
	switch {
	case strings.Contains(dataType, "primary"):
		var data []PrimaryXray1Day
		for _, record := range records[1:] {
			if timeTag, err := utils.ParseTime(record[0]); err == nil && len(record) >= 3 {
				satellite := utils.ParseInt8(record[1])
				flux, _ := strconv.ParseFloat(record[2], 32)
				data = append(data, PrimaryXray1Day{
					TimeTag:   timeTag,
					Satellite: satellite,
					Flux:      float32(flux),
				})
			}
		}
		if len(data) > 0 {
			return db.Clauses(clause.OnConflict{DoNothing: true}).CreateInBatches(data, 1000).Error
		}
	case strings.Contains(dataType, "secondary"):
		var data []SecondaryXray1Day
		for _, record := range records[1:] {
			if timeTag, err := utils.ParseTime(record[0]); err == nil && len(record) >= 3 {
				satellite := utils.ParseInt8(record[1])
				flux, _ := strconv.ParseFloat(record[2], 32)
				data = append(data, SecondaryXray1Day{
					TimeTag:   timeTag,
					Satellite: satellite,
					Flux:      float32(flux),
				})
			}
		}
		if len(data) > 0 {
			return db.Clauses(clause.OnConflict{DoNothing: true}).CreateInBatches(data, 1000).Error
		}
	}
	return nil
}

// ProcessDailyData processes daily data files and saves them to the database
func ProcessDailyData(db *gorm.DB, targetDate string) error {
	fmt.Println("\n=== PROCESSING DAILY DATA TO DATABASE ===")

	if targetDate != "" {
		fmt.Printf("Target date specified: %s\n", targetDate)
	}

	entries, err := os.ReadDir(extract.DataDirectory)
	if err != nil {
		return fmt.Errorf("failed to read data directory: %v", err)
	}

	for _, entry := range entries {
		if !entry.IsDir() {
			continue
		}

		dateStr := entry.Name()
		if _, err := time.Parse("2006-01-02", dateStr); err != nil {
			log.Printf("Skipping directory %s: not a valid date format", dateStr)
			continue
		}

		// If targetDate is specified, only process that date
		if targetDate != "" && dateStr != targetDate {
			continue
		}

		// Check if already processed
		var existingLog ProcessingLog
		if db.Where("date = ?", dateStr).First(&existingLog).Error == nil {
			if targetDate != "" {
				fmt.Printf("Date %s already processed. Skipping to avoid duplicates.\n", dateStr)
				return nil
			} else {
				fmt.Printf("Date %s already processed, skipping...\n", dateStr)
				continue
			}
		}

		fmt.Printf("\nProcessing data for date: %s\n", dateStr)

		dayDir := filepath.Join(extract.DataDirectory, dateStr)
		files, err := os.ReadDir(dayDir)
		if err != nil {
			log.Printf("Failed to read directory %s: %v", dayDir, err)
			if targetDate != "" {
				return fmt.Errorf("failed to read target date directory: %v", err)
			}
			continue
		}

		var filesProcessed int16 = 0
		for _, file := range files {
			if file.IsDir() || !strings.HasSuffix(file.Name(), ".csv") {
				continue
			}

			filePath := filepath.Join(dayDir, file.Name())
			dataType := strings.TrimSuffix(file.Name(), "_"+dateStr+".csv")

			// Files containing data from longer period
			if dataType == "predicted-solar-cycle" || dataType == "observed-solar-cycle-indices" || dataType == "f10-7cm-flux" {
				fmt.Printf("  Skipping excluded file: %s\n", file.Name())
				continue
			}

			fmt.Printf("  Processing: %s (type: %s)\n", file.Name(), dataType)

			csvFile, err := os.Open(filePath)
			if err != nil {
				log.Printf("    Error opening %s: %v", file.Name(), err)
				continue
			}

			reader := csv.NewReader(csvFile)
			records, err := reader.ReadAll()
			csvFile.Close()

			if err != nil {
				log.Printf("    Error reading CSV %s: %v", file.Name(), err)
				continue
			}

			if err = saveDataToSpecificTable(db, dataType, records); err != nil {
				log.Printf("    Error saving %s to database: %v", file.Name(), err)
				continue
			}

			filesProcessed++
			fmt.Printf("    ✓ Saved %s\n", file.Name())
		}

		// log processing to sync the progress
		processingLog := ProcessingLog{
			Date:        dateStr,
			FilesCount:  filesProcessed,
			ProcessedAt: time.Now(),
			Status:      "completed",
		}

		if err := db.Create(&processingLog).Error; err != nil {
			log.Printf("Failed to log processing for date %s: %v", dateStr, err)
		}

		fmt.Printf("  Completed processing %d files for %s\n", filesProcessed, dateStr)

		// If processing a specific date, we're done
		if targetDate != "" {
			fmt.Printf("\n=== COMPLETED PROCESSING FOR TARGET DATE %s ===\n", targetDate)
			return nil
		}
	}

	// Check if target date was not found
	// Check if target date was not found
	if targetDate != "" {
		return fmt.Errorf("target date %s not found in data directory", targetDate)
	}

	fmt.Println("\n=== DATABASE PROCESSING COMPLETE ===")
	return nil
}
