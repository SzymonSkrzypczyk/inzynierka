package database

import "time"

// defined models for Database tables

type BoulderKIndex1m struct {
	ID      uint      `gorm:"primaryKey"`
	TimeTag time.Time `gorm:"index"`
	KIndex  float64
}

type DscovrMag1s struct {
	ID       uint      `gorm:"primaryKey"`
	TimeTag  time.Time `gorm:"index"`
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
	TimeTag    time.Time `gorm:"index"`
	Satellite  string    `gorm:"index"`
	He         float64
	Hp         float64
	Hn         float64
	Total      float64
	ArcJetFlag bool
}

type PlanetaryKIndex1m struct {
	ID          uint      `gorm:"primaryKey"`
	TimeTag     time.Time `gorm:"index"`
	KpIndex     int
	EstimatedKp float64
	Kp          string
}

type PrimaryDifferentialElectrons1Day struct {
	ID        uint      `gorm:"primaryKey"`
	TimeTag   time.Time `gorm:"index"`
	Satellite string    `gorm:"index"`
	Flux      float64
	Energy    string
}

type PrimaryDifferentialProtons1Day struct {
	ID        uint      `gorm:"primaryKey"`
	TimeTag   time.Time `gorm:"index"`
	Satellite string    `gorm:"index"`
	Flux      float64
	Energy    string
	YawFlip   int
	Channel   string
}

type PrimaryIntegralElectrons1Day struct {
	ID        uint      `gorm:"primaryKey"`
	TimeTag   time.Time `gorm:"index"`
	Satellite string    `gorm:"index"`
	Flux      float64
	Energy    string
}

type PrimaryIntegralProtons1Day struct {
	ID        uint      `gorm:"primaryKey"`
	TimeTag   time.Time `gorm:"index"`
	Satellite string    `gorm:"index"`
	Flux      float64
	Energy    string
}

type PrimaryXray1Day struct {
	ID                    uint      `gorm:"primaryKey"`
	TimeTag               time.Time `gorm:"index"`
	Satellite             string    `gorm:"index"`
	Flux                  float64
	ObservedFlux          float64
	ElectronCorrection    float64
	ElectronContamination bool
	Energy                string
}

type SatelliteLongitudes struct {
	ID        uint     `gorm:"primaryKey"`
	Satellite string   `gorm:"uniqueIndex"`
	Longitude *float64 // Nullable
}

type SecondaryDifferentialElectrons1Day struct {
	ID        uint      `gorm:"primaryKey"`
	TimeTag   time.Time `gorm:"index"`
	Satellite string    `gorm:"index"`
	Flux      float64
	Energy    string
}

type SecondaryDifferentialProtons1Day struct {
	ID        uint      `gorm:"primaryKey"`
	TimeTag   time.Time `gorm:"index"`
	Satellite string    `gorm:"index"`
	Flux      float64
	Energy    string
	YawFlip   int
	Channel   string
}

type SecondaryIntegralElectrons1Day struct {
	ID        uint      `gorm:"primaryKey"`
	TimeTag   time.Time `gorm:"index"`
	Satellite string    `gorm:"index"`
	Flux      float64
	Energy    string
}

type SecondaryIntegralProtons1Day struct {
	ID        uint      `gorm:"primaryKey"`
	TimeTag   time.Time `gorm:"index"`
	Satellite string    `gorm:"index"`
	Flux      float64
	Energy    string
}

type SecondaryXray1Day struct {
	ID                    uint      `gorm:"primaryKey"`
	TimeTag               time.Time `gorm:"index"`
	Satellite             string    `gorm:"index"`
	Flux                  float64
	ObservedFlux          float64
	ElectronCorrection    float64
	ElectronContamination bool
	Energy                string
}

type SolarRadioFlux struct {
	ID         uint      `gorm:"primaryKey"`
	TimeTag    time.Time `gorm:"index"`
	CommonName string
	Details    string `gorm:"type:text"` // nested data
}

type SolarRegions struct {
	ID                     uint      `gorm:"primaryKey"`
	ObservedDate           time.Time `gorm:"index"`
	Region                 int
	Latitude               *int    // Nullable
	Longitude              *int    // Nullable
	Location               *string // Nullable
	CarringtonLongitude    *int
	OldCarringtonLongitude *int
	Area                   *int    // Nullable
	SpotClass              *string // Nullable
	Extent                 *int    // Nullable
	NumberSpots            *int    // Nullable
	MagClass               *string // Nullable
	MagString              *string // Nullable
	Status                 *string // Nullable
	CXrayEvents            *int
	MXrayEvents            *int
	XXrayEvents            *int
	ProtonEvents           *string // Nullable
	SFlares                *int
	ImpulseFlares1         *int
	ImpulseFlares2         *int
	ImpulseFlares3         *int
	ImpulseFlares4         *int
	Protons                *string // Nullable
	CFlareProbability      *int
	MFlareProbability      *int
	XFlareProbability      *int
	ProtonProbability      *int
	FirstDate              *time.Time // Nullable
}

type ProcessingLog struct {
	ID          uint   `gorm:"primaryKey"`
	Date        string `gorm:"uniqueIndex"` // YYYY-MM-DD
	FilesCount  int
	ProcessedAt time.Time
	Status      string // either "completed", "failed" or "partial"
}
