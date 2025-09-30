package database

import "time"

// defined models for Database tables

type BoulderKIndex1m struct {
	ID      uint      `gorm:"primaryKey"`
	TimeTag time.Time `gorm:"uniqueIndex"`
	KIndex  float64
}

type DscovrMag1s struct {
	ID      uint      `gorm:"primaryKey"`
	TimeTag time.Time `gorm:"uniqueIndex"`
	Bt      float64
	BxGsm   float64
	ByGsm   float64
	BzGsm   float64
}

type Magnetometers1Day struct {
	ID        uint      `gorm:"primaryKey"`
	TimeTag   time.Time `gorm:"uniqueIndex:idx_mag_time_satellite"`
	Satellite string    `gorm:"uniqueIndex:idx_mag_time_satellite"`
	Total     float64
}

type PlanetaryKIndex1m struct {
	ID          uint      `gorm:"primaryKey"`
	TimeTag     time.Time `gorm:"uniqueIndex"`
	KpIndex     int
	EstimatedKp float64
	Kp          string
}

type PrimaryIntegralProtons1Day struct {
	ID        uint      `gorm:"primaryKey"`
	TimeTag   time.Time `gorm:"uniqueIndex:idx_pip_time_satellite_energy"`
	Satellite string    `gorm:"uniqueIndex:idx_pip_time_satellite_energy"`
	Flux      float64
	Energy    string `gorm:"uniqueIndex:idx_pip_time_satellite_energy"`
}

type PrimaryXray1Day struct {
	ID        uint      `gorm:"primaryKey"`
	TimeTag   time.Time `gorm:"uniqueIndex:idx_pxr_time_satellite_energy"`
	Satellite string    `gorm:"uniqueIndex:idx_pxr_time_satellite_energy"`
	Flux      float64
}

type SecondaryIntegralProtons1Day struct {
	ID        uint      `gorm:"primaryKey"`
	TimeTag   time.Time `gorm:"uniqueIndex:idx_sip_time_satellite_energy"`
	Satellite string    `gorm:"uniqueIndex:idx_sip_time_satellite_energy"`
	Flux      float64
	Energy    string `gorm:"uniqueIndex:idx_sip_time_satellite_energy"`
}

type SecondaryXray1Day struct {
	ID        uint      `gorm:"primaryKey"`
	TimeTag   time.Time `gorm:"uniqueIndex:idx_sxr_time_satellite_energy"`
	Satellite string    `gorm:"uniqueIndex:idx_sxr_time_satellite_energy"`
	Flux      float64
}

type SolarRegions struct {
	ID                uint      `gorm:"primaryKey"`
	ObservedDate      time.Time `gorm:"uniqueIndex:idx_solar_date_region"`
	Region            int       `gorm:"uniqueIndex:idx_solar_date_region"`
	Area              *int
	MagClass          *string
	MXrayEvents       *int
	XXrayEvents       *int
	MFlareProbability *int
	XFlareProbability *int
}

type ProcessingLog struct {
	ID          uint   `gorm:"primaryKey"`
	Date        string `gorm:"uniqueIndex"`
	FilesCount  int
	ProcessedAt time.Time
	Status      string
}
