package database

import "time"

// defined models for Database tables

type BoulderKIndex1m struct {
	ID      uint      `gorm:"primaryKey"`
	TimeTag time.Time `gorm:"uniqueIndex"`
	KIndex  float64
}

type DscovrMag1s struct {
	ID       uint      `gorm:"primaryKey"`
	TimeTag  time.Time `gorm:"uniqueIndex"`
	Bt       float64
	BxGse    float64
	ByGse    float64
	BzGse    float64
	ThetaGse float64
	PhiGse   float64
	BxGsm    float64
	ByGsm    float64
	BzGsm    float64
	ThetaGsm float64
	PhiGsm   float64
}

type Magnetometers1Day struct {
	ID         uint      `gorm:"primaryKey"`
	TimeTag    time.Time `gorm:"uniqueIndex:idx_mag_time_satellite"`
	Satellite  string    `gorm:"uniqueIndex:idx_mag_time_satellite"`
	He         float64
	Hp         float64
	Hn         float64
	Total      float64
	ArcJetFlag bool
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
	ID                    uint      `gorm:"primaryKey"`
	TimeTag               time.Time `gorm:"uniqueIndex:idx_pxr_time_satellite_energy"`
	Satellite             string    `gorm:"uniqueIndex:idx_pxr_time_satellite_energy"`
	Flux                  float64
	ObservedFlux          float64
	ElectronCorrection    float64
	ElectronContamination bool
	Energy                string `gorm:"uniqueIndex:idx_pxr_time_satellite_energy"`
}

type SecondaryIntegralProtons1Day struct {
	ID        uint      `gorm:"primaryKey"`
	TimeTag   time.Time `gorm:"uniqueIndex:idx_sip_time_satellite_energy"`
	Satellite string    `gorm:"uniqueIndex:idx_sip_time_satellite_energy"`
	Flux      float64
	Energy    string `gorm:"uniqueIndex:idx_sip_time_satellite_energy"`
}

type SecondaryXray1Day struct {
	ID                    uint      `gorm:"primaryKey"`
	TimeTag               time.Time `gorm:"uniqueIndex:idx_sxr_time_satellite_energy"`
	Satellite             string    `gorm:"uniqueIndex:idx_sxr_time_satellite_energy"`
	Flux                  float64
	ObservedFlux          float64
	ElectronCorrection    float64
	ElectronContamination bool
	Energy                string `gorm:"uniqueIndex:idx_sxr_time_satellite_energy"`
}

type SolarRegions struct {
	ID                     uint      `gorm:"primaryKey"`
	ObservedDate           time.Time `gorm:"uniqueIndex:idx_solar_date_region"`
	Region                 int       `gorm:"uniqueIndex:idx_solar_date_region"`
	Latitude               *int
	Longitude              *int
	Location               *string
	CarringtonLongitude    *int
	OldCarringtonLongitude *int
	Area                   *int
	SpotClass              *string
	Extent                 *int
	NumberSpots            *int
	MagClass               *string
	MagString              *string
	Status                 *string
	CXrayEvents            *int
	MXrayEvents            *int
	XXrayEvents            *int
	ProtonEvents           *string
	SFlares                *int
	ImpulseFlares1         *int
	ImpulseFlares2         *int
	ImpulseFlares3         *int
	ImpulseFlares4         *int
	Protons                *string
	CFlareProbability      *int
	MFlareProbability      *int
	XFlareProbability      *int
	ProtonProbability      *int
	FirstDate              *time.Time
}

type ProcessingLog struct {
	ID          uint   `gorm:"primaryKey"`
	Date        string `gorm:"uniqueIndex"`
	FilesCount  int
	ProcessedAt time.Time
	Status      string
}
