package main

import (
	"fmt"
	"github.com/dropbox/dropbox-sdk-go-unofficial/v6/dropbox"
	_ "github.com/dropbox/dropbox-sdk-go-unofficial/v6/dropbox"
	"github.com/dropbox/dropbox-sdk-go-unofficial/v6/dropbox/files"
	_ "github.com/dropbox/dropbox-sdk-go-unofficial/v6/dropbox/files"
	"os"
)

func loadSecrets() (DropboxAppSecret, DropboxAppKey string) {
	DropboxAppKey = os.Getenv("DROPBOX_APP_KEY")
	if DropboxAppKey == "" {
		fmt.Println("DROPBOX_APP_KEY environment variable not set")
		os.Exit(1)
	}
	DropboxAppSecret = os.Getenv("DROPBOX_APP_SECRET")
	if DropboxAppSecret == "" {
		fmt.Println("DROPBOX_APP_KEY environment variable not set")
		os.Exit(1)
	}

	return
}

func main() {
	dropboxAppKey, DropboxAppSecret := loadSecrets()
	fmt.Println("Dropbox app secret:", DropboxAppSecret)
	fmt.Printf("app key: %s\n", dropboxAppKey)

	download_directory := files.DownloadZipArg{
		"inzynierka",
	}

	config := dropbox.Config{
		Token:    dropboxAppKey,
		LogLevel: dropbox.LogInfo,
	}
	client := files.New(config)
	fmt.Println("Downloading files...", client, download_directory)

	/*res, content, err := client.DownloadZip(&download_directory)

	if err != nil {
		log.Fatal(err)
	}
	*/
}
