package extract

import (
	"archive/zip"
	"bytes"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestDownloadFromDropbox_DataDirectoryExists(t *testing.T) {
	tempDir := t.TempDir()

	err := os.MkdirAll(tempDir, 0755)
	if err != nil {
		t.Fatalf("Failed to create temp dir: %v", err)
	}

	content := strings.NewReader("test content")
	result, err := downloadFromDropboxWithDir(content, tempDir)

	if err != nil {
		t.Errorf("Expected nil error, got %v", err)
	}
	if result != AlreadyProcessedMessage {
		t.Errorf("Expected '%s', got '%s'", AlreadyProcessedMessage, result)
	}
}

func TestDownloadFromDropbox_DataDirectoryIsFile(t *testing.T) {
	tempDir := t.TempDir()
	filePath := filepath.Join(tempDir, "testfile")

	err := os.WriteFile(filePath, []byte("test"), 0644)
	if err != nil {
		t.Fatalf("Failed to create test file: %v", err)
	}

	content := strings.NewReader("test content")
	result, err := downloadFromDropboxWithDir(content, filePath)

	if err == nil {
		t.Error("Expected error when data directory is a file")
	}
	if result != "" {
		t.Errorf("Expected empty result, got '%s'", result)
	}
}

func TestDownloadFromDropbox_Success(t *testing.T) {
	tempDir := t.TempDir()
	nonExistentDir := filepath.Join(tempDir, "nonexistent")

	content := strings.NewReader("test zip content")
	result, err := downloadFromDropboxWithDir(content, nonExistentDir)

	if err != nil {
		t.Errorf("Expected nil error, got %v", err)
	}
	if result == "" {
		t.Error("Expected non-empty result")
	}
	if !strings.Contains(result, "dropbox_inzynierka_") {
		t.Errorf("Expected result to contain temp file name, got '%s'", result)
	}
}

func TestExtractZipContents_AlreadyProcessed(t *testing.T) {
	err := extractZipContentsWithDir(AlreadyProcessedMessage, "", "")
	if err != nil {
		t.Errorf("Expected nil error for already processed, got %v", err)
	}
}

func TestExtractZipContents_WithTargetDate(t *testing.T) {
	tempDir := t.TempDir()
	zipPath := createTestZip(t, tempDir)
	targetDate := "2024-01-01"

	err := extractZipContentsWithDir(zipPath, targetDate, tempDir)
	if err != nil {
		t.Errorf("Expected nil error, got %v", err)
	}

	expectedDir := filepath.Join(tempDir, targetDate)
	if _, err := os.Stat(expectedDir); os.IsNotExist(err) {
		t.Errorf("Expected directory %s to be created", expectedDir)
	}
}

func TestExtractZipContents_WithoutTargetDate(t *testing.T) {
	tempDir := t.TempDir()
	zipPath := createTestZip(t, tempDir)

	err := extractZipContentsWithDir(zipPath, "", tempDir)
	if err != nil {
		t.Errorf("Expected nil error, got %v", err)
	}

	if _, err := os.Stat(tempDir); os.IsNotExist(err) {
		t.Errorf("Expected directory %s to exist", tempDir)
	}
}

func TestExtractZipContents_InvalidZip(t *testing.T) {
	tempDir := t.TempDir()
	invalidZipPath := filepath.Join(tempDir, "invalid.zip")

	err := os.WriteFile(invalidZipPath, []byte("not a zip file"), 0644)
	if err != nil {
		t.Fatalf("Failed to create invalid zip file: %v", err)
	}

	err = extractZipContentsWithDir(invalidZipPath, "", tempDir)
	if err == nil {
		t.Error("Expected error for invalid zip file")
	}
}

func TestExtractNestedZip_Success(t *testing.T) {
	tempDir := t.TempDir()
	zipPath := createTestZip(t, tempDir)

	err := extractNestedZip(zipPath, tempDir, "")
	if err != nil {
		t.Errorf("Expected nil error, got %v", err)
	}
}

func TestExtractNestedZip_WithTargetDate(t *testing.T) {
	tempDir := t.TempDir()
	zipPath := createTestZip(t, tempDir)
	targetDate := "2024-01-01"

	err := extractNestedZip(zipPath, tempDir, targetDate)
	if err != nil {
		t.Errorf("Expected nil error, got %v", err)
	}
}

func TestExtractNestedZip_InvalidZip(t *testing.T) {
	tempDir := t.TempDir()
	invalidZipPath := filepath.Join(tempDir, "invalid.zip")

	err := os.WriteFile(invalidZipPath, []byte("not a zip file"), 0644)
	if err != nil {
		t.Fatalf("Failed to create invalid zip file: %v", err)
	}

	err = extractNestedZip(invalidZipPath, tempDir, "")
	if err == nil {
		t.Error("Expected error for invalid zip file")
	}
}

func downloadFromDropboxWithDir(r io.Reader, dataDir string) (string, error) {
	if stat, err := os.Stat(dataDir); err == nil {
		if !stat.IsDir() {
			return "", fmt.Errorf("path exists but is not a directory: %s", dataDir)
		}
		return AlreadyProcessedMessage, nil
	}

	if err := os.MkdirAll(dataDir, 0755); err != nil {
		return "", err
	}

	tempFile, err := os.CreateTemp(dataDir, "dropbox_inzynierka_*.zip")
	if err != nil {
		return "", err
	}
	defer tempFile.Close()

	_, err = io.Copy(tempFile, r)
	if err != nil {
		return "", err
	}

	return tempFile.Name(), nil
}

func extractZipContentsWithDir(zipPath, targetDate, dataDir string) error {
	if zipPath == AlreadyProcessedMessage {
		return nil
	}

	extractDir := dataDir
	if targetDate != "" {
		extractDir = filepath.Join(dataDir, targetDate)
	}

	return extractNestedZip(zipPath, extractDir, targetDate)
}

func createTestZip(t *testing.T, dir string) string {
	zipPath := filepath.Join(dir, "test.zip")
	zipFile, err := os.Create(zipPath)
	if err != nil {
		t.Fatalf("Failed to create zip file: %v", err)
	}
	defer zipFile.Close()

	zipWriter := zip.NewWriter(zipFile)
	defer zipWriter.Close()

	fileWriter, err := zipWriter.Create("test.txt")
	if err != nil {
		t.Fatalf("Failed to create file in zip: %v", err)
	}

	_, err = io.Copy(fileWriter, bytes.NewReader([]byte("test content")))
	if err != nil {
		t.Fatalf("Failed to write to zip file: %v", err)
	}

	return zipPath
}
