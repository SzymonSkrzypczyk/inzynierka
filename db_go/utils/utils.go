package utils

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"time"
)

func RemoveDataDirectory(directoryPath string) error {
	err := os.RemoveAll(directoryPath)

	if err != nil {
		log.Fatalf("Failed to remove directory %s: %v", directoryPath, err)
		return err
	}

	log.Printf("Successfully removed directory: %s", directoryPath)
	return nil
}

func ParseTime(timeStr string) (time.Time, error) {
	formats := []string{time.RFC3339, "2006-01-02T15:04:05Z", "2006-01-02T15:04:05", "2006-01-02"}
	for _, format := range formats {
		if t, err := time.Parse(format, timeStr); err == nil {
			return t, nil
		}
	}
	return time.Time{}, fmt.Errorf("unable to parse time: %s", timeStr)
}

func ParseStringPtr(s string) *string {
	if s == "" {
		return nil
	}
	return &s
}

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

func ParseInt8Ptr(s string) *int8 {
	if s == "" {
		return nil
	}
	if val, err := strconv.Atoi(s); err == nil {
		result := int8(val)
		return &result
	}
	return nil
}
