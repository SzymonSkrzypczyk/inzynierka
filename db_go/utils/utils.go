package utils

import (
	"log"
	"os"
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
