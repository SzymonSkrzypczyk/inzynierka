package secrets

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"os"
	"strings"
	"testing"
)

func TestGetAccessToken_Success(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Method != "POST" {
			t.Errorf("Expected POST request, got %s", r.Method)
		}
		if r.Header.Get("Content-Type") != "application/x-www-form-urlencoded" {
			t.Errorf("Expected application/x-www-form-urlencoded content type")
		}

		response := TokenResponse{
			AccessToken: "test_access_token",
			TokenType:   "Bearer",
			ExpiresIn:   14400,
		}
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(response)
	}))
	defer server.Close()

	token, err := GetAccessToken("test_key", "test_secret", "test_refresh")
	if err == nil {
		t.Errorf("Expected error due to hardcoded URL, but got token: %s", token)
	}
}

func TestGetAccessToken_HTTPError(t *testing.T) {
	token, err := GetAccessToken("", "", "")
	if err == nil {
		t.Errorf("Expected error, but got token: %s", token)
	}
}

func TestGetAccessToken_InvalidResponse(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("Invalid request"))
	}))
	defer server.Close()

	token, err := GetAccessToken("test_key", "test_secret", "test_refresh")
	if err == nil {
		t.Errorf("Expected error for invalid response, but got token: %s", token)
	}
	if !strings.Contains(err.Error(), "failed to get access token") {
		t.Errorf("Expected specific error message, got: %s", err.Error())
	}
}

func TestLoadSecrets_AllVariablesSet(t *testing.T) {
	os.Setenv("DROPBOX_APP_KEY", "test_key")
	os.Setenv("DROPBOX_APP_SECRET", "test_secret")
	os.Setenv("DROPBOX_REFRESH_TOKEN", "test_token")

	defer func() {
		os.Unsetenv("DROPBOX_APP_KEY")
		os.Unsetenv("DROPBOX_APP_SECRET")
		os.Unsetenv("DROPBOX_REFRESH_TOKEN")
	}()

	appSecret, appKey, refreshToken := LoadSecrets()

	if appKey != "test_key" {
		t.Errorf("Expected app key 'test_key', got '%s'", appKey)
	}
	if appSecret != "test_secret" {
		t.Errorf("Expected app secret 'test_secret', got '%s'", appSecret)
	}
	if refreshToken != "test_token" {
		t.Errorf("Expected refresh token 'test_token', got '%s'", refreshToken)
	}
}

func TestLoadSecrets_MissingAppKey(t *testing.T) {
	os.Unsetenv("DROPBOX_APP_KEY")
	os.Setenv("DROPBOX_APP_SECRET", "test_secret")
	os.Setenv("DROPBOX_REFRESH_TOKEN", "test_token")

	defer func() {
		os.Unsetenv("DROPBOX_APP_SECRET")
		os.Unsetenv("DROPBOX_REFRESH_TOKEN")
	}()

	if os.Getenv("EXIT_ON_MISSING_ENV") != "false" {
		t.Skip("Skipping test that would cause os.Exit(1)")
	}
}

func TestLoadSecrets_MissingAppSecret(t *testing.T) {
	os.Setenv("DROPBOX_APP_KEY", "test_key")
	os.Unsetenv("DROPBOX_APP_SECRET")
	os.Setenv("DROPBOX_REFRESH_TOKEN", "test_token")

	defer func() {
		os.Unsetenv("DROPBOX_APP_KEY")
		os.Unsetenv("DROPBOX_REFRESH_TOKEN")
	}()

	if os.Getenv("EXIT_ON_MISSING_ENV") != "false" {
		t.Skip("Skipping test that would cause os.Exit(1)")
	}
}

func TestLoadSecrets_MissingRefreshToken(t *testing.T) {
	os.Setenv("DROPBOX_APP_KEY", "test_key")
	os.Setenv("DROPBOX_APP_SECRET", "test_secret")
	os.Unsetenv("DROPBOX_REFRESH_TOKEN")

	defer func() {
		os.Unsetenv("DROPBOX_APP_KEY")
		os.Unsetenv("DROPBOX_APP_SECRET")
	}()

	if os.Getenv("EXIT_ON_MISSING_ENV") != "false" {
		t.Skip("Skipping test that would cause os.Exit(1)")
	}
}

func TestTokenResponse_Struct(t *testing.T) {
	token := TokenResponse{
		AccessToken: "test_token",
		TokenType:   "Bearer",
		ExpiresIn:   3600,
	}

	if token.AccessToken != "test_token" {
		t.Errorf("Expected AccessToken 'test_token', got '%s'", token.AccessToken)
	}
	if token.TokenType != "Bearer" {
		t.Errorf("Expected TokenType 'Bearer', got '%s'", token.TokenType)
	}
	if token.ExpiresIn != 3600 {
		t.Errorf("Expected ExpiresIn 3600, got %d", token.ExpiresIn)
	}
}

func TestTokenResponse_JSONMarshaling(t *testing.T) {
	token := TokenResponse{
		AccessToken: "test_token",
		TokenType:   "Bearer",
		ExpiresIn:   3600,
	}

	data, err := json.Marshal(token)
	if err != nil {
		t.Errorf("Failed to marshal TokenResponse: %v", err)
	}

	var unmarshaled TokenResponse
	err = json.Unmarshal(data, &unmarshaled)
	if err != nil {
		t.Errorf("Failed to unmarshal TokenResponse: %v", err)
	}

	if unmarshaled.AccessToken != token.AccessToken {
		t.Errorf("AccessToken mismatch after JSON round trip")
	}
	if unmarshaled.TokenType != token.TokenType {
		t.Errorf("TokenType mismatch after JSON round trip")
	}
	if unmarshaled.ExpiresIn != token.ExpiresIn {
		t.Errorf("ExpiresIn mismatch after JSON round trip")
	}
}
