package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"time"

	"github.com/joho/godotenv"
)

const (
	NASA_API_ENDPOINT = "https://api.nasa.gov/planetary/earth/imagery"
	KRAKOW_LATITUDE   = 50.049683
	KRAKOW_LONGITUDE  = 19.944544
	DEFAULT_DIM       = 0.1
	DATE_FORMAT       = "2006-01-02"
)

// Load NASA API key from environment variables
func getNASAAPIKey() string {
	err := godotenv.Load()
	if err != nil {
		fmt.Println("Error loading .env file")
		os.Exit(1)
	}

	apiKey, exists := os.LookupEnv("NASA_API_KEY")
	if !exists {
		fmt.Println("Error: NASA_API_KEY environment variable is not set.")
		os.Exit(1)
	}
	return apiKey
}

// Fetches a satellite image from NASA API
func getImage(lon, lat float64, targetDate string, imageDim float64, apiKey string) ([]byte, error) {
	url := fmt.Sprintf("%s?lon=%f&lat=%f&date=%s&dim=%f&api_key=%s",
		NASA_API_ENDPOINT, lon, lat, targetDate, imageDim, apiKey)

	resp, err := http.Get(url)
	if err != nil {
		return nil, fmt.Errorf("error fetching image: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("error: received status code %d", resp.StatusCode)
	}

	data, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("error reading response body: %v", err)
	}

	return data, nil
}

func saveImage(content []byte, targetDate string, targetDirectory string) error {
	err := os.MkdirAll(targetDirectory, os.ModePerm)
	if err != nil {
		return fmt.Errorf("error creating directory: %v", err)
	}

	dayDirectory := filepath.Join(targetDirectory, targetDate)
	if _, err := os.Stat(dayDirectory); err == nil {
		os.RemoveAll(dayDirectory)
	}
	err = os.MkdirAll(dayDirectory, os.ModePerm)
	if err != nil {
		return fmt.Errorf("error creating day directory: %v", err)
	}

	timestamp := time.Now().Format("2006-01-02_15-04-05")
	targetFile := filepath.Join(dayDirectory, fmt.Sprintf("%s_on_%s.png", targetDate, timestamp))
	err = os.WriteFile(targetFile, content, 0644)
	if err != nil {
		return fmt.Errorf("error writing file: %v", err)
	}

	fmt.Printf("Image saved at: %s\n", targetFile)
	return nil
}

func main() {
	apiKey := getNASAAPIKey()
	targetDate := time.Now().Format(DATE_FORMAT)
	targetDirectory := "images"

	image, err := getImage(KRAKOW_LONGITUDE, KRAKOW_LATITUDE, targetDate, DEFAULT_DIM, apiKey)
	if err != nil {
		fmt.Printf("Error fetching image: %v\n", err)
		return
	}

	err = saveImage(image, targetDate, targetDirectory)
	if err != nil {
		fmt.Printf("Error saving image: %v\n", err)
	}
}
