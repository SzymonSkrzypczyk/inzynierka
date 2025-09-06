package database

import "time"

type SpaceWeatherData struct {
	ID        uint      `gorm:"primaryKey"`
	Date      time.Time `gorm:"index"`
	DataType  string    `gorm:"index"`
	TimeTag   time.Time
	Data      string `gorm:"type:jsonb"` // Store CSV data as JSON
	CreatedAt time.Time
}

type ProcessingLog struct {
	ID          uint   `gorm:"primaryKey"`
	Date        string `gorm:"uniqueIndex"`
	FilesCount  int
	ProcessedAt time.Time
	Status      string
}
