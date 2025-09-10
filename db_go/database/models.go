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

type PrimaryDifferentialElectrons1Day struct {
	ID        uint      `gorm:"primaryKey"`
	TimeTag   time.Time `gorm:"uniqueIndex:idx_pde_time_satellite_energy"`
	Satellite string    `gorm:"uniqueIndex:idx_pde_time_satellite_energy"`
	Flux      float64
	Energy    string `gorm:"uniqueIndex:idx_pde_time_satellite_energy"`
}

type PrimaryDifferentialProtons1Day struct {
	ID        uint      `gorm:"primaryKey"`
	TimeTag   time.Time `gorm:"uniqueIndex:idx_pdp_time_satellite_energy_channel"`
	Satellite string    `gorm:"uniqueIndex:idx_pdp_time_satellite_energy_channel"`
	Flux      float64
	Energy    string `gorm:"uniqueIndex:idx_pdp_time_satellite_energy_channel"`
	YawFlip   int
	Channel   string `gorm:"uniqueIndex:idx_pdp_time_satellite_energy_channel"`
}

type PrimaryIntegralElectrons1Day struct {
	ID        uint      `gorm:"primaryKey"`
	TimeTag   time.Time `gorm:"uniqueIndex:idx_pie_time_satellite_energy"`
	Satellite string    `gorm:"uniqueIndex:idx_pie_time_satellite_energy"`
	Flux      float64
	Energy    string `gorm:"uniqueIndex:idx_pie_time_satellite_energy"`
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

type SatelliteLongitudes struct {
	ID        uint   `gorm:"primaryKey"`
	Satellite string `gorm:"uniqueIndex"`
	Longitude *float64
	TimeTag   time.Time
}

type SecondaryDifferentialElectrons1Day struct {
	ID        uint      `gorm:"primaryKey"`
	TimeTag   time.Time `gorm:"uniqueIndex:idx_sde_time_satellite_energy"`
	Satellite string    `gorm:"uniqueIndex:idx_sde_time_satellite_energy"`
	Flux      float64
	Energy    string `gorm:"uniqueIndex:idx_sde_time_satellite_energy"`
}

type SecondaryDifferentialProtons1Day struct {
	ID        uint      `gorm:"primaryKey"`
	TimeTag   time.Time `gorm:"uniqueIndex:idx_sdp_time_satellite_energy_channel"`
	Satellite string    `gorm:"uniqueIndex:idx_sdp_time_satellite_energy_channel"`
	Flux      float64
	Energy    string `gorm:"uniqueIndex:idx_sdp_time_satellite_energy_channel"`
	YawFlip   int
	Channel   string `gorm:"uniqueIndex:idx_sdp_time_satellite_energy_channel"`
}

type SecondaryIntegralElectrons1Day struct {
	ID        uint      `gorm:"primaryKey"`
	TimeTag   time.Time `gorm:"uniqueIndex:idx_sie_time_satellite_energy"`
	Satellite string    `gorm:"uniqueIndex:idx_sie_time_satellite_energy"`
	Flux      float64
	Energy    string `gorm:"uniqueIndex:idx_sie_time_satellite_energy"`
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

type SolarRadioFlux struct {
	ID         uint      `gorm:"primaryKey"`
	TimeTag    time.Time `gorm:"uniqueIndex"`
	CommonName string
	Details    string `gorm:"type:text"`
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
