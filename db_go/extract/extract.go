package extract

import (
	"archive/zip"
	"fmt"
	"io"
	"log"
	"os"
	"path/filepath"
	"strings"
	"time"
)

const (
	DataDirectory           = "./data"
	AlreadyProcessedMessage = "Already Processed Skipping..." // Message indicating already processed data
)

func DownloadFromDropbox(content io.Reader) (string, error) {
	// Create a temporary directory holding the daily reports

	fileInfo, err := os.Stat(DataDirectory)
	if err == nil && !fileInfo.IsDir() {
		return "", fmt.Errorf("data directory %s exists and is not a directory", DataDirectory)
	} else if err == nil {
		fmt.Printf("Data directory %s already exists, skipping extraction\n", DataDirectory)
		return AlreadyProcessedMessage, nil
	}

	tempDir := os.TempDir()
	timestamp := time.Now().Format("20060102_150405")
	tempFileName := fmt.Sprintf("dropbox_inzynierka_%s.zip", timestamp)
	tempFilePath := filepath.Join(tempDir, tempFileName)

	tempFile, err := os.Create(tempFilePath)
	if err != nil {
		log.Fatalf("Failed to create temp file: %v", err)
		return "", err
	}

	// extra defer to ensure file is closed
	defer func(tempFile *os.File) {
		err := tempFile.Close()
		if err != nil {
			log.Fatalf("Failed to close temp file: %v", err)
		}
	}(tempFile)

	bytesWritten, err := io.Copy(tempFile, content)
	if err != nil {
		log.Fatalf("Failed to write zip content to temp file: %v", err)
		return "", err
	}

	fmt.Println("Download successful!")
	fmt.Printf("Zip file saved to: %s\n", tempFilePath)
	fmt.Printf("File size: %d bytes\n", bytesWritten)

	return tempFilePath, nil
}

func ExtractZipContents(zipFilePath string) error {
	if zipFilePath == AlreadyProcessedMessage {
		fmt.Println("Data already processed, skipping zip extraction")
		return nil
	}
	err := os.MkdirAll(DataDirectory, 0755)
	if err != nil {
		return fmt.Errorf("failed to create data directory: %v", err)
	}

	reader, err := zip.OpenReader(zipFilePath)
	if err != nil {
		return err
	}
	defer reader.Close()

	fmt.Println("\n=== EXTRACTING ZIP CONTENTS ===")
	fmt.Printf("Total files: %d\n", len(reader.File))
	fmt.Printf("Extracting to: %s\n\n", DataDirectory)

	for _, file := range reader.File {
		if file.FileInfo().IsDir() {
			continue
		}

		fmt.Printf("Extracting: %s\n", file.Name)

		rc, err := file.Open()
		if err != nil {
			return fmt.Errorf("failed to open file %s in zip: %v", file.Name, err)
		}

		fileName := filepath.Base(file.Name)
		destPath := filepath.Join(DataDirectory, fileName)

		destFile, err := os.Create(destPath)
		if err != nil {
			rc.Close()
			return fmt.Errorf("failed to create destination file %s: %v", destPath, err)
		}

		_, err = io.Copy(destFile, rc)
		rc.Close()
		destFile.Close()

		if err != nil {
			return fmt.Errorf("failed to copy file %s: %v", file.Name, err)
		}

		fmt.Printf("  → Saved as: %s\n", destPath)

		if strings.HasSuffix(strings.ToLower(fileName), ".zip") {
			fmt.Printf("  → Detected nested zip, extracting contents...\n")
			err = extractNestedZip(destPath, DataDirectory)
			if err != nil {
				log.Printf("Warning: failed to extract nested zip %s: %v", fileName, err)
			}
		}
	}

	fmt.Println("\n=== EXTRACTION COMPLETE ===")
	return nil
}

func extractNestedZip(zipPath, baseDataDir string) error {
	reader, err := zip.OpenReader(zipPath)
	if err != nil {
		return err
	}
	defer reader.Close()

	zipName := strings.TrimSuffix(filepath.Base(zipPath), ".zip")
	subDir := filepath.Join(baseDataDir, zipName)
	err = os.MkdirAll(subDir, 0755)
	if err != nil {
		return fmt.Errorf("failed to create subdirectory %s: %v", subDir, err)
	}

	fmt.Printf("    → Extracting %d files to: %s\n", len(reader.File), subDir)

	for _, file := range reader.File {
		// Skip directories
		if file.FileInfo().IsDir() {
			continue
		}

		rc, err := file.Open()
		if err != nil {
			return fmt.Errorf("failed to open nested file %s: %v", file.Name, err)
		}

		fileName := filepath.Base(file.Name)
		destPath := filepath.Join(subDir, fileName)
		destFile, err := os.Create(destPath)
		if err != nil {
			rc.Close()
			return fmt.Errorf("failed to create nested file %s: %v", destPath, err)
		}

		_, err = io.Copy(destFile, rc)
		rc.Close()
		destFile.Close()

		if err != nil {
			return fmt.Errorf("failed to copy nested file %s: %v", file.Name, err)
		}

		fmt.Printf("    → %s\n", destPath)
	}

	return nil
}
