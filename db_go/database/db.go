package database

import (
	"encoding/csv"
	"fmt"
	"github.com/SzymonSkrzypczyk/db_go/extract"
	"github.com/SzymonSkrzypczyk/db_go/utils"
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
		&PrimaryDifferentialElectrons1Day{},
		&PrimaryDifferentialProtons1Day{},
		&PrimaryIntegralElectrons1Day{},
		&PrimaryIntegralProtons1Day{},
		&PrimaryXray1Day{},
		&SatelliteLongitudes{},
		&SecondaryDifferentialElectrons1Day{},
		&SecondaryDifferentialProtons1Day{},
		&SecondaryIntegralElectrons1Day{},
		&SecondaryIntegralProtons1Day{},
		&SecondaryXray1Day{},
		&SolarRadioFlux{},
		&SolarRegions{},
		&ProcessingLog{},
	)
	if err != nil {
		return nil, fmt.Errorf("failed to migrate database schema: %v", err)
	}

	fmt.Println("Database connection established and schema migrated successfully")
	return db, nil
}

func saveDataToSpecificTable(db *gorm.DB, dataType string, records [][]string, dateStr string) error {
	if len(records) < 2 {
		return nil
	}

	// Parse the date for use in models that need it
	processDate, err := time.Parse("2006-01-02", dateStr)
	if err != nil {
		return fmt.Errorf("invalid date format %s: %v", dateStr, err)
	}

	switch dataType {
	case "boulder_k_index_1m":
		var data []BoulderKIndex1m
		for _, record := range records[1:] {
			if timeTag, err := utils.ParseTime(record[0]); err == nil {
				if kIndex, err := strconv.ParseFloat(record[1], 64); err == nil {
					data = append(data, BoulderKIndex1m{TimeTag: timeTag, KIndex: kIndex})
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
				bt, _ := strconv.ParseFloat(record[1], 64)
				bxGse, _ := strconv.ParseFloat(record[2], 64)
				byGse, _ := strconv.ParseFloat(record[3], 64)
				bzGse, _ := strconv.ParseFloat(record[4], 64)
				thetaGse, _ := strconv.ParseFloat(record[5], 64)
				phiGse, _ := strconv.ParseFloat(record[6], 64)
				bxGsm, _ := strconv.ParseFloat(record[7], 64)
				byGsm, _ := strconv.ParseFloat(record[8], 64)
				bzGsm, _ := strconv.ParseFloat(record[9], 64)
				thetaGsm, _ := strconv.ParseFloat(record[10], 64)
				phiGsm, _ := strconv.ParseFloat(record[11], 64)

				data = append(data, DscovrMag1s{
					TimeTag: timeTag, Bt: bt, BxGse: bxGse, ByGse: byGse, BzGse: bzGse,
					ThetaGse: thetaGse, PhiGse: phiGse, BxGsm: bxGsm, ByGsm: byGsm,
					BzGsm: bzGsm, ThetaGsm: thetaGsm, PhiGsm: phiGsm,
				})
			}
		}
		if len(data) > 0 {
			return db.Clauses(clause.OnConflict{DoNothing: true}).CreateInBatches(data, 1000).Error
		}

	case "magnetometers-1-day":
		var data []Magnetometers1Day
		for _, record := range records[1:] {
			if timeTag, err := utils.ParseTime(record[0]); err == nil && len(record) >= 7 {
				satellite := record[1]
				he, _ := strconv.ParseFloat(record[2], 64)
				hp, _ := strconv.ParseFloat(record[3], 64)
				hn, _ := strconv.ParseFloat(record[4], 64)
				total, _ := strconv.ParseFloat(record[5], 64)

				data = append(data, Magnetometers1Day{
					TimeTag: timeTag, Satellite: satellite, He: he, Hp: hp,
					Hn: hn, Total: total, ArcJetFlag: utils.ParseBool(record[6]),
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
				estimatedKp, _ := strconv.ParseFloat(record[2], 64)

				data = append(data, PlanetaryKIndex1m{
					TimeTag: timeTag, KpIndex: kpIndex, EstimatedKp: estimatedKp, Kp: record[3],
				})
			}
		}
		if len(data) > 0 {
			return db.Clauses(clause.OnConflict{DoNothing: true}).CreateInBatches(data, 1000).Error
		}

	case "satellite-longitudes":
		var data []SatelliteLongitudes
		for _, record := range records[1:] {
			if len(record) >= 2 {
				data = append(data, SatelliteLongitudes{
					Satellite: record[0],
					Longitude: utils.ParseFloatPtr(record[1]),
					TimeTag:   processDate,
				})
			}
		}
		if len(data) > 0 {
			return db.Clauses(clause.OnConflict{DoNothing: true}).CreateInBatches(data, 1000).Error
		}

	case "solar-radio-flux":
		var data []SolarRadioFlux
		for _, record := range records[1:] {
			if timeTag, err := utils.ParseTime(record[0]); err == nil && len(record) >= 3 {
				commonName := record[1]
				data = append(data, SolarRadioFlux{
					TimeTag: timeTag, CommonName: commonName, Details: record[2],
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
				var firstDate *time.Time
				if len(record) > 28 && record[28] != "" {
					if fd, err := utils.ParseTime(record[28]); err == nil {
						firstDate = &fd
					}
				}

				data = append(data, SolarRegions{
					ObservedDate: observedDate, Region: region,
					Latitude: utils.ParseIntPtr(record[2]), Longitude: utils.ParseIntPtr(record[3]),
					Location: utils.ParseStringPtr(record[4]), CarringtonLongitude: utils.ParseIntPtr(record[5]),
					OldCarringtonLongitude: utils.ParseIntPtr(record[6]), Area: utils.ParseIntPtr(record[7]),
					SpotClass: utils.ParseStringPtr(record[8]), Extent: utils.ParseIntPtr(record[9]),
					NumberSpots: utils.ParseIntPtr(record[10]), MagClass: utils.ParseStringPtr(record[11]),
					MagString: utils.ParseStringPtr(record[12]), Status: utils.ParseStringPtr(record[13]),
					CXrayEvents: utils.ParseIntPtr(record[14]), MXrayEvents: utils.ParseIntPtr(record[15]),
					XXrayEvents: utils.ParseIntPtr(record[16]), ProtonEvents: utils.ParseStringPtr(record[17]),
					SFlares: utils.ParseIntPtr(record[18]), ImpulseFlares1: utils.ParseIntPtr(record[19]),
					ImpulseFlares2: utils.ParseIntPtr(record[20]), ImpulseFlares3: utils.ParseIntPtr(record[21]),
					ImpulseFlares4: utils.ParseIntPtr(record[22]), Protons: utils.ParseStringPtr(record[23]),
					CFlareProbability: utils.ParseIntPtr(record[24]), MFlareProbability: utils.ParseIntPtr(record[25]),
					XFlareProbability: utils.ParseIntPtr(record[26]), ProtonProbability: utils.ParseIntPtr(record[27]),
					FirstDate: firstDate,
				})
			}
		}
		if len(data) > 0 {
			return db.Clauses(clause.OnConflict{DoNothing: true}).CreateInBatches(data, 1000).Error
		}

	// Handle particle data patterns
	default:
		if strings.Contains(dataType, "electrons") {
			return saveElectronData(db, dataType, records)
		} else if strings.Contains(dataType, "protons") {
			return saveProtonData(db, dataType, records)
		} else if strings.Contains(dataType, "xray") {
			return saveXrayData(db, dataType, records)
		}
	}

	return nil
}

func saveElectronData(db *gorm.DB, dataType string, records [][]string) error {
	switch {
	case strings.Contains(dataType, "primary-differential"):
		var data []PrimaryDifferentialElectrons1Day
		for _, record := range records[1:] {
			if timeTag, err := utils.ParseTime(record[0]); err == nil && len(record) >= 4 {
				satellite := record[1]
				energy := record[3]
				flux, _ := strconv.ParseFloat(record[2], 64)
				data = append(data, PrimaryDifferentialElectrons1Day{
					TimeTag: timeTag, Satellite: satellite, Flux: flux, Energy: energy,
				})
			}
		}
		if len(data) > 0 {
			return db.Clauses(clause.OnConflict{DoNothing: true}).CreateInBatches(data, 1000).Error
		}
	case strings.Contains(dataType, "primary-integral"):
		var data []PrimaryIntegralElectrons1Day
		for _, record := range records[1:] {
			if timeTag, err := utils.ParseTime(record[0]); err == nil && len(record) >= 4 {
				satellite := record[1]
				energy := record[3]
				flux, _ := strconv.ParseFloat(record[2], 64)
				data = append(data, PrimaryIntegralElectrons1Day{
					TimeTag: timeTag, Satellite: satellite, Flux: flux, Energy: energy,
				})
			}
		}
		if len(data) > 0 {
			return db.Clauses(clause.OnConflict{DoNothing: true}).CreateInBatches(data, 1000).Error
		}
	case strings.Contains(dataType, "secondary-differential"):
		var data []SecondaryDifferentialElectrons1Day
		for _, record := range records[1:] {
			if timeTag, err := utils.ParseTime(record[0]); err == nil && len(record) >= 4 {
				satellite := record[1]
				energy := record[3]
				flux, _ := strconv.ParseFloat(record[2], 64)
				data = append(data, SecondaryDifferentialElectrons1Day{
					TimeTag: timeTag, Satellite: satellite, Flux: flux, Energy: energy,
				})
			}
		}
		if len(data) > 0 {
			return db.Clauses(clause.OnConflict{DoNothing: true}).CreateInBatches(data, 1000).Error
		}
	case strings.Contains(dataType, "secondary-integral"):
		var data []SecondaryIntegralElectrons1Day
		for _, record := range records[1:] {
			if timeTag, err := utils.ParseTime(record[0]); err == nil && len(record) >= 4 {
				satellite := record[1]
				energy := record[3]
				flux, _ := strconv.ParseFloat(record[2], 64)
				data = append(data, SecondaryIntegralElectrons1Day{
					TimeTag: timeTag, Satellite: satellite, Flux: flux, Energy: energy,
				})
			}
		}
		if len(data) > 0 {
			return db.Clauses(clause.OnConflict{DoNothing: true}).CreateInBatches(data, 1000).Error
		}
	}
	return nil
}

func saveProtonData(db *gorm.DB, dataType string, records [][]string) error {
	switch {
	case strings.Contains(dataType, "primary-differential"):
		var data []PrimaryDifferentialProtons1Day
		for _, record := range records[1:] {
			if timeTag, err := utils.ParseTime(record[0]); err == nil && len(record) >= 6 {
				satellite := record[1]
				energy := record[3]
				channel := record[5]
				flux, _ := strconv.ParseFloat(record[2], 64)
				yawFlip, _ := strconv.Atoi(record[4])
				data = append(data, PrimaryDifferentialProtons1Day{
					TimeTag: timeTag, Satellite: satellite, Flux: flux, Energy: energy,
					YawFlip: yawFlip, Channel: channel,
				})
			}
		}
		if len(data) > 0 {
			return db.Clauses(clause.OnConflict{DoNothing: true}).CreateInBatches(data, 1000).Error
		}
	case strings.Contains(dataType, "primary-integral"):
		var data []PrimaryIntegralProtons1Day
		for _, record := range records[1:] {
			if timeTag, err := utils.ParseTime(record[0]); err == nil && len(record) >= 4 {
				satellite := record[1]
				energy := record[3]
				flux, _ := strconv.ParseFloat(record[2], 64)
				data = append(data, PrimaryIntegralProtons1Day{
					TimeTag: timeTag, Satellite: satellite, Flux: flux, Energy: energy,
				})
			}
		}
		if len(data) > 0 {
			return db.Clauses(clause.OnConflict{DoNothing: true}).CreateInBatches(data, 1000).Error
		}
	case strings.Contains(dataType, "secondary-differential"):
		var data []SecondaryDifferentialProtons1Day
		for _, record := range records[1:] {
			if timeTag, err := utils.ParseTime(record[0]); err == nil && len(record) >= 6 {
				satellite := record[1]
				energy := record[3]
				channel := record[5]
				flux, _ := strconv.ParseFloat(record[2], 64)
				yawFlip, _ := strconv.Atoi(record[4])
				data = append(data, SecondaryDifferentialProtons1Day{
					TimeTag: timeTag, Satellite: satellite, Flux: flux, Energy: energy,
					YawFlip: yawFlip, Channel: channel,
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
				satellite := record[1]
				energy := record[3]
				flux, _ := strconv.ParseFloat(record[2], 64)
				data = append(data, SecondaryIntegralProtons1Day{
					TimeTag: timeTag, Satellite: satellite, Flux: flux, Energy: energy,
				})
			}
		}
		if len(data) > 0 {
			return db.Clauses(clause.OnConflict{DoNothing: true}).CreateInBatches(data, 1000).Error
		}
	}
	return nil
}

func saveXrayData(db *gorm.DB, dataType string, records [][]string) error {
	switch {
	case strings.Contains(dataType, "primary"):
		var data []PrimaryXray1Day
		for _, record := range records[1:] {
			if timeTag, err := utils.ParseTime(record[0]); err == nil && len(record) >= 7 {
				satellite := record[1]
				energy := record[6]
				flux, _ := strconv.ParseFloat(record[2], 64)
				observedFlux, _ := strconv.ParseFloat(record[3], 64)
				electronCorrection, _ := strconv.ParseFloat(record[4], 64)
				data = append(data, PrimaryXray1Day{
					TimeTag: timeTag, Satellite: satellite, Flux: flux, ObservedFlux: observedFlux,
					ElectronCorrection: electronCorrection, ElectronContamination: utils.ParseBool(record[5]),
					Energy: energy,
				})
			}
		}
		if len(data) > 0 {
			return db.Clauses(clause.OnConflict{DoNothing: true}).CreateInBatches(data, 1000).Error
		}
	case strings.Contains(dataType, "secondary"):
		var data []SecondaryXray1Day
		for _, record := range records[1:] {
			if timeTag, err := utils.ParseTime(record[0]); err == nil && len(record) >= 7 {
				satellite := record[1]
				energy := record[6]
				flux, _ := strconv.ParseFloat(record[2], 64)
				observedFlux, _ := strconv.ParseFloat(record[3], 64)
				electronCorrection, _ := strconv.ParseFloat(record[4], 64)
				data = append(data, SecondaryXray1Day{
					TimeTag: timeTag, Satellite: satellite, Flux: flux, ObservedFlux: observedFlux,
					ElectronCorrection: electronCorrection, ElectronContamination: utils.ParseBool(record[5]),
					Energy: energy,
				})
			}
		}
		if len(data) > 0 {
			return db.Clauses(clause.OnConflict{DoNothing: true}).CreateInBatches(data, 1000).Error
		}
	}
	return nil
}

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

		filesProcessed := 0
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

			if err = saveDataToSpecificTable(db, dataType, records, dateStr); err != nil {
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
	if targetDate != "" {
		return fmt.Errorf("target date %s not found in data directory", targetDate)
	}

	fmt.Println("\n=== DATABASE PROCESSING COMPLETE ===")
	return nil
}
