package utils

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
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

func ParseBool(s string) bool { return strings.ToLower(s) == "true" }

func ParseIntPtr(s string) *int {
	if s == "" {
		return nil
	}
	if val, err := strconv.Atoi(s); err == nil {
		return &val
	}
	return nil
}

func ParseFloatPtr(s string) *float64 {
	if s == "" {
		return nil
	}
	if val, err := strconv.ParseFloat(s, 64); err == nil {
		return &val
	}
	return nil
}

func ParseStringPtr(s string) *string {
	if s == "" {
		return nil
	}
	return &s
}
