package utils

import (
	"os"
	"path/filepath"
	"testing"
	"time"
)

func TestRemoveDataDirectory_Success(t *testing.T) {
	tempDir := filepath.Join(os.TempDir(), "test_dir")
	err := os.MkdirAll(tempDir, 0755)
	if err != nil {
		t.Fatalf("Failed to create test directory: %v", err)
	}

	err = RemoveDataDirectory(tempDir)
	if err != nil {
		t.Errorf("Expected no error, got %v", err)
	}

	if _, err := os.Stat(tempDir); !os.IsNotExist(err) {
		t.Error("Expected directory to be removed")
	}
}

func TestRemoveDataDirectory_NonExistentDirectory(t *testing.T) {
	err := RemoveDataDirectory("/non/existent/path")
	if err != nil {
		t.Errorf("Expected no error for non-existent directory, got %v", err)
	}
}

func TestParseTime_RFC3339(t *testing.T) {
	timeStr := "2023-12-25T15:30:45Z"
	expected := time.Date(2023, 12, 25, 15, 30, 45, 0, time.UTC)

	result, err := ParseTime(timeStr)
	if err != nil {
		t.Errorf("Expected no error, got %v", err)
	}
	if !result.Equal(expected) {
		t.Errorf("Expected %v, got %v", expected, result)
	}
}

func TestParseTime_CustomFormat1(t *testing.T) {
	timeStr := "2023-12-25T15:30:45Z"
	expected := time.Date(2023, 12, 25, 15, 30, 45, 0, time.UTC)

	result, err := ParseTime(timeStr)
	if err != nil {
		t.Errorf("Expected no error, got %v", err)
	}
	if !result.Equal(expected) {
		t.Errorf("Expected %v, got %v", expected, result)
	}
}

func TestParseTime_CustomFormat2(t *testing.T) {
	timeStr := "2023-12-25T15:30:45"
	expected := time.Date(2023, 12, 25, 15, 30, 45, 0, time.UTC)

	result, err := ParseTime(timeStr)
	if err != nil {
		t.Errorf("Expected no error, got %v", err)
	}
	if !result.Equal(expected) {
		t.Errorf("Expected %v, got %v", expected, result)
	}
}

func TestParseTime_DateOnly(t *testing.T) {
	timeStr := "2023-12-25"
	expected := time.Date(2023, 12, 25, 0, 0, 0, 0, time.UTC)

	result, err := ParseTime(timeStr)
	if err != nil {
		t.Errorf("Expected no error, got %v", err)
	}
	if !result.Equal(expected) {
		t.Errorf("Expected %v, got %v", expected, result)
	}
}

func TestParseTime_InvalidFormat(t *testing.T) {
	timeStr := "invalid-time-format"

	_, err := ParseTime(timeStr)
	if err == nil {
		t.Error("Expected error for invalid time format")
	}
	if err.Error() != "unable to parse time: invalid-time-format" {
		t.Errorf("Expected specific error message, got: %s", err.Error())
	}
}

func TestParseStringPtr_EmptyString(t *testing.T) {
	result := ParseStringPtr("")
	if result != nil {
		t.Error("Expected nil for empty string")
	}
}

func TestParseStringPtr_NonEmptyString(t *testing.T) {
	input := "test"
	result := ParseStringPtr(input)
	if result == nil {
		t.Error("Expected non-nil pointer")
	}
	if *result != input {
		t.Errorf("Expected %s, got %s", input, *result)
	}
}

func TestParseInt16Ptr_EmptyString(t *testing.T) {
	result := ParseInt16Ptr("")
	if result != nil {
		t.Error("Expected nil for empty string")
	}
}

func TestParseInt16Ptr_ValidNumber(t *testing.T) {
	result := ParseInt16Ptr("123")
	if result == nil {
		t.Error("Expected non-nil pointer")
	}
	if *result != 123 {
		t.Errorf("Expected 123, got %d", *result)
	}
}

func TestParseInt16Ptr_NegativeNumber(t *testing.T) {
	result := ParseInt16Ptr("-456")
	if result == nil {
		t.Error("Expected non-nil pointer")
	}
	if *result != -456 {
		t.Errorf("Expected -456, got %d", *result)
	}
}

func TestParseInt16Ptr_InvalidString(t *testing.T) {
	result := ParseInt16Ptr("abc")
	if result != nil {
		t.Error("Expected nil for invalid string")
	}
}

func TestParseInt8Ptr_EmptyString(t *testing.T) {
	result := ParseInt8Ptr("")
	if result != nil {
		t.Error("Expected nil for empty string")
	}
}

func TestParseInt8Ptr_ValidNumber(t *testing.T) {
	result := ParseInt8Ptr("42")
	if result == nil {
		t.Error("Expected non-nil pointer")
	}
	if *result != 42 {
		t.Errorf("Expected 42, got %d", *result)
	}
}

func TestParseInt8Ptr_NegativeNumber(t *testing.T) {
	result := ParseInt8Ptr("-50")
	if result == nil {
		t.Error("Expected non-nil pointer")
	}
	if *result != -50 {
		t.Errorf("Expected -50, got %d", *result)
	}
}

func TestParseInt8Ptr_MinValue(t *testing.T) {
	result := ParseInt8Ptr("-128")
	if result == nil {
		t.Error("Expected non-nil pointer")
	}
	if *result != -128 {
		t.Errorf("Expected -128, got %d", *result)
	}
}

func TestParseInt8Ptr_MaxValue(t *testing.T) {
	result := ParseInt8Ptr("127")
	if result == nil {
		t.Error("Expected non-nil pointer")
	}
	if *result != 127 {
		t.Errorf("Expected 127, got %d", *result)
	}
}

func TestParseInt8Ptr_OutOfRangePositive(t *testing.T) {
	result := ParseInt8Ptr("200")
	if result != nil {
		t.Error("Expected nil for out of range value")
	}
}

func TestParseInt8Ptr_OutOfRangeNegative(t *testing.T) {
	result := ParseInt8Ptr("-200")
	if result != nil {
		t.Error("Expected nil for out of range value")
	}
}

func TestParseInt8Ptr_InvalidString(t *testing.T) {
	result := ParseInt8Ptr("xyz")
	if result != nil {
		t.Error("Expected nil for invalid string")
	}
}

func TestParseInt8_EmptyString(t *testing.T) {
	result := ParseInt8("")
	if result != 0 {
		t.Errorf("Expected 0 for empty string, got %d", result)
	}
}

func TestParseInt8_ValidNumber(t *testing.T) {
	result := ParseInt8("75")
	if result != 75 {
		t.Errorf("Expected 75, got %d", result)
	}
}

func TestParseInt8_NegativeNumber(t *testing.T) {
	result := ParseInt8("-30")
	if result != -30 {
		t.Errorf("Expected -30, got %d", result)
	}
}

func TestParseInt8_MinValue(t *testing.T) {
	result := ParseInt8("-128")
	if result != -128 {
		t.Errorf("Expected -128, got %d", result)
	}
}

func TestParseInt8_MaxValue(t *testing.T) {
	result := ParseInt8("127")
	if result != 127 {
		t.Errorf("Expected 127, got %d", result)
	}
}

func TestParseInt8_OutOfRangePositive(t *testing.T) {
	result := ParseInt8("300")
	if result != 0 {
		t.Errorf("Expected 0 for out of range value, got %d", result)
	}
}

func TestParseInt8_OutOfRangeNegative(t *testing.T) {
	result := ParseInt8("-300")
	if result != 0 {
		t.Errorf("Expected 0 for out of range value, got %d", result)
	}
}

func TestParseInt8_InvalidString(t *testing.T) {
	result := ParseInt8("invalid")
	if result != 0 {
		t.Errorf("Expected 0 for invalid string, got %d", result)
	}
}
