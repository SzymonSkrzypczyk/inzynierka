package utils

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"time"
)

// RemoveDataDirectory deletes the specified directory and all its contents.
func RemoveDataDirectory(directoryPath string) error {
	err := os.RemoveAll(directoryPath)

	if err != nil {
		log.Fatalf("Failed to remove directory %s: %v", directoryPath, err)
		return err
	}

	log.Printf("Successfully removed directory: %s", directoryPath)
	return nil
}

// ParseTime attempts to parse a time string in multiple formats and returns the first successful parse.
func ParseTime(timeStr string) (time.Time, error) {
	formats := []string{time.RFC3339, "2006-01-02T15:04:05Z", "2006-01-02T15:04:05", "2006-01-02"}
	for _, format := range formats {
		if t, err := time.Parse(format, timeStr); err == nil {
			return t, nil
		}
	}
	return time.Time{}, fmt.Errorf("unable to parse time: %s", timeStr)
}

// ParseStringPtr returns a pointer to the string if it's not empty, otherwise returns nil.
func ParseStringPtr(s string) *string {
	if s == "" {
		return nil
	}
	return &s
}

// ParseInt16Ptr attempts to parse a string into an int16 pointer. Returns nil if parsing fails or string is empty.
func ParseInt16Ptr(s string) *int16 {
	if s == "" {
		return nil
	}
	if val, err := strconv.Atoi(s); err == nil {
		result := int16(val)
		return &result
	}
	return nil
}

// ParseInt8Ptr attempts to parse a string into an int8. Returns 0 if parsing fails or string is empty.
func ParseInt8Ptr(s string) *int8 {
	if s == "" {
		return nil
	}
	if val, err := strconv.Atoi(s); err == nil && val >= -128 && val <= 127 {
		result := int8(val)
		return &result
	}
	return nil
}

// ParseInt8 attempts to parse a string into an int8. Returns 0 if parsing fails or string is empty.
func ParseInt8(s string) int8 {
	if s == "" {
		return 0
	}
	if val, err := strconv.Atoi(s); err == nil && val >= -128 && val <= 127 {
		return int8(val)
	}
	return 0
}
