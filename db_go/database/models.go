package database

import "time"

// defined models for Database tables

type BoulderKIndex1m struct {
	ID      uint      `gorm:"primaryKey"`
	TimeTag time.Time `gorm:"uniqueIndex;type:timestamp(0)"`
	KIndex  float32   `gorm:"type:real"`
}

type DscovrMag1s struct {
	ID      uint      `gorm:"primaryKey"`
	TimeTag time.Time `gorm:"uniqueIndex;type:timestamp(0)"`
	Bt      float32   `gorm:"type:real"`
	BxGsm   float32   `gorm:"type:real"`
	ByGsm   float32   `gorm:"type:real"`
	BzGsm   float32   `gorm:"type:real"`
}

type Magnetometers1Day struct {
	ID        uint      `gorm:"primaryKey"`
	TimeTag   time.Time `gorm:"uniqueIndex:idx_mag_time_satellite;type:timestamp(0)"`
	Satellite *int8     `gorm:"uniqueIndex:idx_mag_time_satellite;type:varchar(20)"`
	Total     float32   `gorm:"type:real"`
}

type PlanetaryKIndex1m struct {
	ID          uint      `gorm:"primaryKey"`
	TimeTag     time.Time `gorm:"uniqueIndex;type:timestamp(0)"`
	KpIndex     int8      `gorm:"type:smallint;check:kp_index >= 0 AND kp_index <= 9"`
	EstimatedKp float32   `gorm:"type:real;check:estimated_kp >= 0 AND estimated_kp <= 9"`
	Kp          string    `gorm:"type:varchar(10)"`
}

type PrimaryIntegralProtons1Day struct {
	ID        uint      `gorm:"primaryKey"`
	TimeTag   time.Time `gorm:"uniqueIndex:idx_pip_time_satellite_energy;type:timestamp(0)"`
	Satellite *int8     `gorm:"uniqueIndex:idx_pip_time_satellite_energy;type:varchar(20)"`
	Flux      float32   `gorm:"type:real"`
	Energy    string    `gorm:"uniqueIndex:idx_pip_time_satellite_energy;type:varchar(15)"`
}

type PrimaryXray1Day struct {
	ID        uint      `gorm:"primaryKey"`
	TimeTag   time.Time `gorm:"uniqueIndex:idx_pxr_time_satellite;type:timestamp(0)"`
	Satellite *int8     `gorm:"uniqueIndex:idx_pxr_time_satellite;type:varchar(20)"`
	Flux      float32   `gorm:"type:real"`
}

type SecondaryIntegralProtons1Day struct {
	ID        uint      `gorm:"primaryKey"`
	TimeTag   time.Time `gorm:"uniqueIndex:idx_sip_time_satellite_energy;type:timestamp(0)"`
	Satellite *int8     `gorm:"uniqueIndex:idx_sip_time_satellite_energy;type:varchar(20)"`
	Flux      float32   `gorm:"type:real"`
	Energy    string    `gorm:"uniqueIndex:idx_sip_time_satellite_energy;type:varchar(15)"`
}

type SecondaryXray1Day struct {
	ID        uint      `gorm:"primaryKey"`
	TimeTag   time.Time `gorm:"uniqueIndex:idx_sxr_time_satellite;type:timestamp(0)"`
	Satellite *int8     `gorm:"uniqueIndex:idx_sxr_time_satellite;type:varchar(20)"`
	Flux      float32   `gorm:"type:real"`
}

type SolarRegions struct {
	ID                uint      `gorm:"primaryKey"`
	ObservedDate      time.Time `gorm:"uniqueIndex:idx_solar_date_region;type:date"`
	Region            int16     `gorm:"uniqueIndex:idx_solar_date_region;type:smallint"`
	Area              *int16    `gorm:"type:smallint"`
	MagClass          *string   `gorm:"type:varchar(15)"`
	MXrayEvents       *int8     `gorm:"type:smallint"`
	XXrayEvents       *int8     `gorm:"type:smallint"`
	MFlareProbability *int8     `gorm:"type:smallint;check:m_flare_probability >= 0 AND m_flare_probability <= 100"`
	XFlareProbability *int8     `gorm:"type:smallint;check:x_flare_probability >= 0 AND x_flare_probability <= 100"`
}

type ProcessingLog struct {
	ID          uint      `gorm:"primaryKey"`
	Date        string    `gorm:"uniqueIndex;type:varchar(10)"`
	FilesCount  int16     `gorm:"type:smallint"`
	ProcessedAt time.Time `gorm:"type:timestamp(0)"`
	Status      string    `gorm:"type:varchar(20)"`
}
