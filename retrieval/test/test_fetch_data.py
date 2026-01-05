import pytest
from unittest.mock import patch, MagicMock, mock_open, AsyncMock
from pathlib import Path

from retrieval.fetch_data import retrieve_data, compress_data, retrieve_all_data


class TestFetchData:
    @pytest.mark.asyncio
    @patch("retrieval.fetch_data.aiohttp.ClientSession")
    async def test_retrieve_data_success(self, mock_session):
        mock_response = AsyncMock()
        mock_response.ok = True
        mock_response.json = AsyncMock(return_value=[{"key1": "value1", "key2": "value2"}])

        mock_context = AsyncMock()
        mock_context.__aenter__.return_value = mock_response

        session_instance = MagicMock()
        session_instance.get.return_value = mock_context

        mock_cm = AsyncMock()
        mock_cm.__aenter__.return_value = session_instance
        mock_session.return_value = mock_cm

        target_dir = Path("test_dir")

        with patch("retrieval.fetch_data.Path.mkdir"), \
                patch("builtins.open", mock_open()) as m:
            await retrieve_data("test", "http://example.com", target_dir)

        m.assert_called_once()
        mock_response.json.assert_called_once()

    @pytest.mark.asyncio
    @patch("retrieval.fetch_data.aiohttp.ClientSession")
    async def test_retrieve_data_http_error(self, mock_session):
        mock_response = AsyncMock()
        mock_response.ok = False
        mock_response.status = 403

        mock_context = AsyncMock()
        mock_context.__aenter__.return_value = mock_response

        session_instance = MagicMock()
        session_instance.get.return_value = mock_context

        mock_cm = AsyncMock()
        mock_cm.__aenter__.return_value = session_instance
        mock_session.return_value = mock_cm

        with patch("retrieval.fetch_data.Path.mkdir"), \
                patch("retrieval.fetch_data.asyncio.sleep", return_value=None), \
                pytest.raises(Exception, match="Failed to retrieve data from http://example.com after 3 retries"):
            await retrieve_data("test", "http://example.com")

    @pytest.mark.asyncio
    @patch("retrieval.fetch_data.aiohttp.ClientSession")
    async def test_retrieve_data_empty_response(self, mock_session):
        mock_response = AsyncMock()
        mock_response.ok = True
        mock_response.json = AsyncMock(return_value=[])

        mock_context = AsyncMock()
        mock_context.__aenter__.return_value = mock_response

        session_instance = MagicMock()
        session_instance.get.return_value = mock_context

        mock_cm = AsyncMock()
        mock_cm.__aenter__.return_value = session_instance
        mock_session.return_value = mock_cm

        with patch("retrieval.fetch_data.Path.mkdir"), \
                patch("retrieval.fetch_data.asyncio.sleep", return_value=None), \
                pytest.raises(Exception, match="Failed to retrieve data from http://example.com after 3 retries"):
            await retrieve_data("test", "http://example.com")

    @pytest.mark.asyncio
    @patch("retrieval.fetch_data.aiohttp.ClientSession")
    async def test_retrieve_data_nested_data(self, mock_session):
        mock_response = AsyncMock()
        mock_response.ok = True
        mock_response.json = AsyncMock(return_value=[
            {"key1": "value1", "nested": {"key2": "value2"}}
        ])

        mock_context = AsyncMock()
        mock_context.__aenter__.return_value = mock_response

        session_instance = MagicMock()
        session_instance.get.return_value = mock_context

        mock_cm = AsyncMock()
        mock_cm.__aenter__.return_value = session_instance
        mock_session.return_value = mock_cm

        target_dir = Path("test_dir")

        with patch("retrieval.fetch_data.Path.mkdir"), \
                patch("builtins.open", mock_open()) as m:
            await retrieve_data("test", "http://example.com", target_dir)

        m.assert_called_once()
        mock_response.json.assert_called_once()

    @patch("retrieval.fetch_data.make_archive")
    @patch("retrieval.fetch_data.rmtree")
    @patch("retrieval.fetch_data.Path.mkdir")
    def test_compress_data(self, mock_mkdir, mock_rmtree, mock_make_archive):
        compress_data("test", Path("test_dir"))

        mock_mkdir.assert_called_once()
        mock_make_archive.assert_called_once()
        mock_rmtree.assert_called_once()

    @patch("retrieval.fetch_data.compress_data")
    @patch("retrieval.fetch_data.send_to_dropbox")
    @patch("retrieval.fetch_data.retrieve_data")
    @patch("retrieval.fetch_data.NAME2URL", {"test1": "url1", "test2": "url2"})
    @pytest.mark.asyncio
    async def test_retrieve_all_data(self, mock_retrieve_data, mock_send_to_dropbox, mock_compress_data):
        mock_retrieve_data.return_value = None

        with patch("retrieval.fetch_data.datetime") as mock_datetime:
            mock_datetime.today.return_value.date.return_value = "2023-01-01"
            await retrieve_all_data()

        assert mock_retrieve_data.call_count == 2
        mock_compress_data.assert_called_once()
        mock_send_to_dropbox.assert_called_once()

    @pytest.mark.asyncio
    @patch("retrieval.fetch_data.asyncio.gather")
    @patch("retrieval.fetch_data.compress_data")
    @patch("retrieval.fetch_data.send_to_dropbox")
    @pytest.mark.asyncio
    async def test_retrieve_all_data_exception(self, mock_send_to_dropbox, mock_compress_data, mock_gather):
        mock_gather.side_effect = Exception("Test error")

        with pytest.raises(Exception, match="Test error"):
            await retrieve_all_data()

        mock_compress_data.assert_not_called()
        mock_send_to_dropbox.assert_not_called()
