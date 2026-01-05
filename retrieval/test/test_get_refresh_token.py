import pytest
from unittest.mock import patch, MagicMock
from retrieval.get_refresh_token import get_refresh_token


class TestGetRefreshToken:
    @patch('retrieval.get_refresh_token.DropboxOAuth2FlowNoRedirect')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_get_refresh_token(self, mock_print, mock_input, mock_flow_class):
        app_key = "test_app_key"
        app_secret = "test_app_secret"
        auth_code = "test_auth_code"

        mock_flow = MagicMock()
        mock_flow_class.return_value = mock_flow

        mock_flow.start.return_value = "https://dropbox.com/authorize"

        mock_result = MagicMock()
        mock_result.refresh_token = "test_refresh_token"
        mock_result.access_token = "test_access_token"
        mock_result.expires_at = "2023-01-01"

        mock_flow.finish.return_value = mock_result
        mock_input.return_value = auth_code

        result = get_refresh_token(app_key, app_secret)

        mock_flow_class.assert_called_once_with(
            consumer_key=app_key,
            consumer_secret=app_secret,
            token_access_type='offline'
        )

        mock_flow.start.assert_called_once()
        mock_flow.finish.assert_called_once_with(auth_code)

        assert result == "test_refresh_token"
        assert mock_print.call_count == 6