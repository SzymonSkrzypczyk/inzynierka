import pytest
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path
from dropbox.exceptions import ApiError, AuthError

from send2dropbox import send_to_dropbox, MAX_RETRIES, SEND_RETRY_SLEEP_TIME


class TestSendToDropbox:
    @patch('send2dropbox.dropbox.Dropbox')
    @patch('send2dropbox.sleep')
    def test_send_to_dropbox_success(self, mock_sleep, mock_dropbox_class):
        mock_dbx = MagicMock()
        mock_dropbox_class.return_value = mock_dbx
        mock_logger = MagicMock()
        file_path = Path("test_file.zip")
        dropbox_path = "/backup/test_file.zip"

        with patch('builtins.open', mock_open(read_data=b'file_content')) as m:
            send_to_dropbox(file_path, dropbox_path, mock_logger)

        mock_dropbox_class.assert_called_once()
        mock_dbx.files_upload.assert_called_once()
        mock_logger.log.assert_called_with(f"Successfully uploaded {file_path} to Dropbox at {dropbox_path}")
        mock_sleep.assert_not_called()

    @patch('send2dropbox.dropbox.Dropbox')
    @patch('send2dropbox.sleep')
    def test_send_to_dropbox_api_error_with_retry_success(self, mock_sleep, mock_dropbox_class):
        mock_dbx = MagicMock()
        api_error = ApiError(
            error={"error_summary": "Test API error"},
            user_message_text="Test user message",
            user_message_locale="en",
            request_id="test_request_id"
        )
        mock_dbx.files_upload.side_effect = [api_error, None]
        mock_dropbox_class.return_value = mock_dbx
        mock_logger = MagicMock()
        file_path = Path("test_file.zip")
        dropbox_path = "/backup/test_file.zip"

        with patch('builtins.open', mock_open(read_data=b'file_content')):
            send_to_dropbox(file_path, dropbox_path, mock_logger)

        assert mock_dbx.files_upload.call_count == 2
        mock_sleep.assert_called_once_with(SEND_RETRY_SLEEP_TIME)
        mock_logger.log_exception.assert_called_once()

    @patch('send2dropbox.dropbox.Dropbox')
    @patch('send2dropbox.sleep')
    def test_send_to_dropbox_auth_error_with_retry_success(self, mock_sleep, mock_dropbox_class):
        mock_dbx = MagicMock()
        auth_error = AuthError(
            error="Test Auth error",
            request_id="test_request_id"
        )
        mock_dbx.files_upload.side_effect = [auth_error, None]
        mock_dropbox_class.return_value = mock_dbx
        mock_logger = MagicMock()
        file_path = "test_file.zip"
        dropbox_path = "/backup/test_file.zip"

        with patch('builtins.open', mock_open(read_data=b'file_content')):
            send_to_dropbox(file_path, dropbox_path, mock_logger)

        assert mock_dbx.files_upload.call_count == 2
        mock_sleep.assert_called_once_with(SEND_RETRY_SLEEP_TIME)
        mock_logger.log_exception.assert_called_once()

    @patch('send2dropbox.dropbox.Dropbox')
    @patch('send2dropbox.sleep')
    def test_send_to_dropbox_max_retries_exceeded(self, mock_sleep, mock_dropbox_class):
        mock_dbx = MagicMock()
        api_error = ApiError(
            error={"error_summary": "Test API error"},
            user_message_text="Test user message",
            user_message_locale="en",
            request_id="test_request_id"
        )
        mock_dbx.files_upload.side_effect = [api_error] * MAX_RETRIES
        mock_dropbox_class.return_value = mock_dbx
        mock_logger = MagicMock()
        file_path = "test_file.zip"
        dropbox_path = "/backup/test_file.zip"

        with patch('builtins.open', mock_open(read_data=b'file_content')):
            with pytest.raises(Exception, match=f"Failed to upload {file_path} to Dropbox after {MAX_RETRIES} retries"):
                send_to_dropbox(file_path, dropbox_path, mock_logger)

        assert mock_dbx.files_upload.call_count == MAX_RETRIES
        assert mock_sleep.call_count == MAX_RETRIES
        assert mock_logger.log_error.called

    @patch('send2dropbox.dropbox.Dropbox')
    def test_send_to_dropbox_file_handling(self, mock_dropbox_class):
        mock_dbx = MagicMock()
        mock_dropbox_class.return_value = mock_dbx
        mock_logger = MagicMock()
        file_path = Path("test_file.zip")
        dropbox_path = "/backup/test_file.zip"
        file_content = b'test file content'

        with patch('builtins.open', mock_open(read_data=file_content)) as m:
            send_to_dropbox(file_path, dropbox_path, mock_logger)

        m.assert_called_once_with(file_path, 'rb')
        mock_dbx.files_upload.assert_called_once()
        args, kwargs = mock_dbx.files_upload.call_args
        assert args[0] == file_content
