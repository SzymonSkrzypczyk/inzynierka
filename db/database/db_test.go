package database

import (
	"github.com/DATA-DOG/go-sqlmock"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"testing"
)

func TestSaveDataToSpecificTable_EmptyRecords(t *testing.T) {
	db, _, _ := sqlmock.New()
	gdb, _ := gorm.Open(postgres.New(postgres.Config{
		Conn: db,
	}), &gorm.Config{})

	err := saveDataToSpecificTable(gdb, "boulder_k_index_1m", [][]string{})
	if err != nil {
		t.Errorf("Expected nil error for empty records, got %v", err)
	}
}

func TestSaveDataToSpecificTable_BoulderKIndex1m(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create sqlmock: %v", err)
	}
	defer db.Close()

	gdb, err := gorm.Open(postgres.New(postgres.Config{
		Conn: db,
	}), &gorm.Config{})
	if err != nil {
		t.Fatalf("failed to open gorm db: %v", err)
	}

	records := [][]string{
		{"TimeTag", "KIndex"},
		{"2024-06-01T00:00:00Z", "3.0"},
	}

	mock.ExpectBegin()
	mock.ExpectQuery(`INSERT INTO "boulder_k_index1ms"`).
		WithArgs(sqlmock.AnyArg(), float32(3.0)).
		WillReturnRows(sqlmock.NewRows([]string{"id"}))
	mock.ExpectCommit()

	err = saveDataToSpecificTable(gdb, "boulder_k_index_1m", records)
	if err != nil {
		t.Errorf("Expected nil error, got %v", err)
	}
}

func TestSaveDataToSpecificTable_DscovrMag1s(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create sqlmock: %v", err)
	}
	defer db.Close()

	gdb, err := gorm.Open(postgres.New(postgres.Config{
		Conn: db,
	}), &gorm.Config{})
	if err != nil {
		t.Fatalf("failed to open gorm db: %v", err)
	}

	records := [][]string{
		{"TimeTag", "Bt", "BxGse", "ByGse", "BzGse", "ThetaGse", "PhiGse", "BxGsm", "ByGsm", "BzGsm", "ThetaGsm", "PhiGsm"},
		{"2024-06-01T00:00:00Z", "5.0", "1.0", "2.0", "3.0", "45.0", "90.0", "1.5", "2.5", "3.5", "50.0", "95.0"},
	}

	mock.ExpectBegin()
	mock.ExpectQuery(`INSERT INTO "dscovr_mag1s"`).
		WithArgs(sqlmock.AnyArg(), float32(5.0), float32(1.5), float32(2.5), float32(3.5)).
		WillReturnRows(sqlmock.NewRows([]string{"id"}))
	mock.ExpectCommit()

	err = saveDataToSpecificTable(gdb, "dscovr_mag_1s", records)
	if err != nil {
		t.Errorf("Expected nil error, got %v", err)
	}
}

func TestSaveDataToSpecificTable_PlanetaryKIndex1m(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create sqlmock: %v", err)
	}
	defer db.Close()

	gdb, err := gorm.Open(postgres.New(postgres.Config{
		Conn: db,
	}), &gorm.Config{})
	if err != nil {
		t.Fatalf("failed to open gorm db: %v", err)
	}

	records := [][]string{
		{"TimeTag", "KpIndex", "EstimatedKp", "Kp"},
		{"2024-06-01T00:00:00Z", "3", "2.7", "2o"},
	}

	mock.ExpectBegin()
	mock.ExpectQuery(`INSERT INTO "planetary_k_index1ms"`).
		WithArgs(sqlmock.AnyArg(), int8(3), float32(2.7), "2o").
		WillReturnRows(sqlmock.NewRows([]string{"id"}))
	mock.ExpectCommit()

	err = saveDataToSpecificTable(gdb, "planetary_k_index_1m", records)
	if err != nil {
		t.Errorf("Expected nil error, got %v", err)
	}
}

func TestSaveDataToSpecificTable_SolarRegions(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create sqlmock: %v", err)
	}
	defer db.Close()

	gdb, err := gorm.Open(postgres.New(postgres.Config{
		Conn: db,
	}), &gorm.Config{})
	if err != nil {
		t.Fatalf("failed to open gorm db: %v", err)
	}

	records := [][]string{
		{"ObservedDate", "Region", "Latitude", "Longitude", "Location", "CarringtonLongitude", "OldCarringtonLongitude", "Area", "SpotClass", "Extent", "NumberSpots", "MagClass", "MagString", "Status", "CXrayEvents", "MXrayEvents", "XXrayEvents", "ProtonEvents", "SFlares", "ImpulseFlares1", "ImpulseFlares2", "ImpulseFlares3", "ImpulseFlares4", "Protons", "CFlareProbability", "MFlareProbability", "XFlareProbability", "ProtonProbability"},
		{"2024-06-01", "1", "10", "20", "N10W20", "300", "290", "100", "Dao", "05", "3", "Beta", "B", "New", "0", "1", "0", "", "0", "0", "0", "0", "0", "", "5", "10", "1", "1"},
	}

	mock.ExpectBegin()
	mock.ExpectQuery(`INSERT INTO "solar_regions"`).
		WithArgs(sqlmock.AnyArg(), int16(1), sqlmock.AnyArg(), sqlmock.AnyArg(), sqlmock.AnyArg(), sqlmock.AnyArg(), sqlmock.AnyArg(), sqlmock.AnyArg()).
		WillReturnRows(sqlmock.NewRows([]string{"id"}))
	mock.ExpectCommit()

	err = saveDataToSpecificTable(gdb, "solar_regions", records)
	if err != nil {
		t.Errorf("Expected nil error, got %v", err)
	}
}

func TestSaveDataToSpecificTable_UnknownType(t *testing.T) {
	db, _, _ := sqlmock.New()
	gdb, _ := gorm.Open(postgres.New(postgres.Config{
		Conn: db,
	}), &gorm.Config{})

	records := [][]string{
		{"header1", "header2"},
		{"val1", "val2"},
	}
	err := saveDataToSpecificTable(gdb, "unknown_type", records)
	if err != nil {
		t.Errorf("Expected nil error for unknown type, got %v", err)
	}
}

func TestSaveProtonData_Primary(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create sqlmock: %v", err)
	}
	defer db.Close()

	gdb, err := gorm.Open(postgres.New(postgres.Config{
		Conn: db,
	}), &gorm.Config{})
	if err != nil {
		t.Fatalf("failed to open gorm db: %v", err)
	}

	records := [][]string{
		{"TimeTag", "Satellite", "Flux", "Energy"},
		{"2024-06-01T00:00:00Z", "1", "100.5", ">10MeV"},
	}

	mock.ExpectBegin()
	mock.ExpectQuery(`INSERT INTO "primary_integral_protons1_days"`).
		WithArgs(sqlmock.AnyArg(), int8(1), float32(100.5), ">10MeV").
		WillReturnRows(sqlmock.NewRows([]string{"id"}))
	mock.ExpectCommit()

	err = saveProtonData(gdb, "primary-integral-protons", records)
	if err != nil {
		t.Errorf("Expected nil error, got %v", err)
	}
}

func TestSaveXrayData_Primary(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create sqlmock: %v", err)
	}
	defer db.Close()

	gdb, err := gorm.Open(postgres.New(postgres.Config{
		Conn: db,
	}), &gorm.Config{})
	if err != nil {
		t.Fatalf("failed to open gorm db: %v", err)
	}

	records := [][]string{
		{"TimeTag", "Satellite", "Flux"},
		{"2024-06-01T00:00:00Z", "1", "1.5e-06"},
	}

	mock.ExpectBegin()
	mock.ExpectQuery(`INSERT INTO "primary_xray1_days"`).
		WithArgs(sqlmock.AnyArg(), int8(1), sqlmock.AnyArg()).
		WillReturnRows(sqlmock.NewRows([]string{"id"}))
	mock.ExpectCommit()

	err = saveXrayData(gdb, "primary-xray", records)
	if err != nil {
		t.Errorf("Expected nil error, got %v", err)
	}
}
