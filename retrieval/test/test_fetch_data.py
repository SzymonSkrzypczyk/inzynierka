"""Tests for the fetch_data module."""

import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, mock_open, patch

from retrieval.fetch_data import compress_data, retrieve_all_data, retrieve_data


def _make_session_mock(mock_response):
    """Create a properly configured session mock for ``session.get()``.

    The production code calls ``async with session.get(url) as response``,
    which means ``session.get(url)`` must return an async context manager
    whose ``__aenter__`` yields ``mock_response``.
    """
    mock_ctx = AsyncMock()
    mock_ctx.__aenter__.return_value = mock_response
    mock_ctx.__aexit__.return_value = False

    session = MagicMock()
    session.get.return_value = mock_ctx
    return session


class TestRetrieveData:
    """Tests for the retrieve_data function."""

    @pytest.mark.asyncio
    async def test_retrieve_data_success(self):
        """Successful fetch returns a Path to the saved CSV."""
        mock_response = AsyncMock()
        mock_response.ok = True
        mock_response.json = AsyncMock(
            return_value=[{"key1": "value1", "key2": "value2"}]
        )

        session = _make_session_mock(mock_response)

        target_dir = Path("test_dir")

        with (
            patch("retrieval.fetch_data.Path.mkdir"),
            patch("builtins.open", mock_open()) as mocked_file,
        ):
            result = await retrieve_data(
                session, "test", "http://example.com", target_dir
            )

        mocked_file.assert_called_once()
        mock_response.json.assert_called_once()
        assert result is not None
        assert isinstance(result, Path)

    @pytest.mark.asyncio
    async def test_retrieve_data_http_error_returns_none(self):
        """HTTP error after MAX_RETRIES returns None (no exception)."""
        mock_response = AsyncMock()
        mock_response.ok = False
        mock_response.status = 403
        mock_response.request_info = MagicMock()
        mock_response.history = ()

        session = _make_session_mock(mock_response)

        with (
            patch("retrieval.fetch_data.Path.mkdir"),
            patch(
                "retrieval.fetch_data.asyncio.sleep",
                new_callable=AsyncMock,
            ),
        ):
            result = await retrieve_data(
                session, "test", "http://example.com"
            )

        assert result is None

    @pytest.mark.asyncio
    async def test_retrieve_data_empty_response_returns_none(self):
        """Empty JSON response after MAX_RETRIES returns None."""
        mock_response = AsyncMock()
        mock_response.ok = True
        mock_response.json = AsyncMock(return_value=[])

        session = _make_session_mock(mock_response)

        with (
            patch("retrieval.fetch_data.Path.mkdir"),
            patch(
                "retrieval.fetch_data.asyncio.sleep",
                new_callable=AsyncMock,
            ),
        ):
            result = await retrieve_data(
                session, "test", "http://example.com"
            )

        assert result is None

    @pytest.mark.asyncio
    async def test_retrieve_data_nested_data(self):
        """Data with nested dicts is flattened and saved successfully."""
        mock_response = AsyncMock()
        mock_response.ok = True
        mock_response.json = AsyncMock(
            return_value=[
                {"key1": "value1", "nested": {"key2": "value2"}}
            ]
        )

        session = _make_session_mock(mock_response)

        target_dir = Path("test_dir")

        with (
            patch("retrieval.fetch_data.Path.mkdir"),
            patch("builtins.open", mock_open()) as mocked_file,
        ):
            result = await retrieve_data(
                session, "test", "http://example.com", target_dir
            )

        mocked_file.assert_called_once()
        mock_response.json.assert_called_once()
        assert result is not None

    @pytest.mark.asyncio
    async def test_retrieve_data_retries_with_fresh_requests(self):
        """Each retry attempt makes a new HTTP request."""
        call_count = 0

        mock_response_fail = AsyncMock()
        mock_response_fail.ok = False
        mock_response_fail.status = 500
        mock_response_fail.request_info = MagicMock()
        mock_response_fail.history = ()

        mock_response_success = AsyncMock()
        mock_response_success.ok = True
        mock_response_success.json = AsyncMock(
            return_value=[{"key": "value"}]
        )

        def mock_get(url):
            nonlocal call_count
            call_count += 1
            ctx = MagicMock()
            if call_count < 3:
                ctx.__aenter__ = AsyncMock(
                    return_value=mock_response_fail
                )
            else:
                ctx.__aenter__ = AsyncMock(
                    return_value=mock_response_success
                )
            ctx.__aexit__ = AsyncMock(return_value=False)
            return ctx

        session = MagicMock()
        session.get = mock_get

        with (
            patch("retrieval.fetch_data.Path.mkdir"),
            patch("builtins.open", mock_open()),
            patch(
                "retrieval.fetch_data.asyncio.sleep",
                new_callable=AsyncMock,
            ),
        ):
            result = await retrieve_data(
                session, "test", "http://example.com"
            )

        assert call_count == 3
        assert result is not None


class TestCompressData:
    """Tests for the compress_data function."""

    @patch("retrieval.fetch_data.make_archive")
    @patch("retrieval.fetch_data.rmtree")
    @patch("retrieval.fetch_data.Path.mkdir")
    def test_compress_data(
        self, mock_mkdir, mock_rmtree, mock_make_archive
    ):
        """Compression creates archive and removes source directory."""
        compress_data("test", Path("test_dir"))

        mock_mkdir.assert_called_once()
        mock_make_archive.assert_called_once()
        mock_rmtree.assert_called_once()


class TestRetrieveAllData:
    """Tests for the retrieve_all_data function."""

    @patch("retrieval.fetch_data.compress_data")
    @patch("retrieval.fetch_data.send_to_dropbox")
    @patch("retrieval.fetch_data.retrieve_data")
    @patch(
        "retrieval.fetch_data.NAME2URL",
        {"test1": "url1", "test2": "url2"},
    )
    @pytest.mark.asyncio
    async def test_retrieve_all_data_success(
        self,
        mock_retrieve_data,
        mock_send_to_dropbox,
        mock_compress_data,
    ):
        """All sources succeed — archive is created and uploaded."""
        mock_retrieve_data.return_value = Path("some_file.csv")

        with patch("retrieval.fetch_data.datetime") as mock_dt:
            mock_dt.today.return_value.date.return_value = "2023-01-01"
            await retrieve_all_data()

        assert mock_retrieve_data.call_count == 2
        mock_compress_data.assert_called_once()
        mock_send_to_dropbox.assert_called_once()

    @patch("retrieval.fetch_data.compress_data")
    @patch("retrieval.fetch_data.send_to_dropbox")
    @patch("retrieval.fetch_data.retrieve_data")
    @patch(
        "retrieval.fetch_data.NAME2URL",
        {"test1": "url1", "test2": "url2", "test3": "url3"},
    )
    @pytest.mark.asyncio
    async def test_retrieve_all_data_partial_failure(
        self,
        mock_retrieve_data,
        mock_send_to_dropbox,
        mock_compress_data,
    ):
        """Some sources fail — archive is still created with successes."""
        mock_retrieve_data.side_effect = [
            Path("file1.csv"),
            None,
            Path("file3.csv"),
        ]

        with patch("retrieval.fetch_data.datetime") as mock_dt:
            mock_dt.today.return_value.date.return_value = "2023-01-01"
            await retrieve_all_data()

        assert mock_retrieve_data.call_count == 3
        mock_compress_data.assert_called_once()
        mock_send_to_dropbox.assert_called_once()

    @patch("retrieval.fetch_data.compress_data")
    @patch("retrieval.fetch_data.send_to_dropbox")
    @patch("retrieval.fetch_data.retrieve_data")
    @patch(
        "retrieval.fetch_data.NAME2URL",
        {"test1": "url1", "test2": "url2"},
    )
    @pytest.mark.asyncio
    async def test_retrieve_all_data_all_failures(
        self,
        mock_retrieve_data,
        mock_send_to_dropbox,
        mock_compress_data,
    ):
        """All sources fail — no archive is created or uploaded."""
        mock_retrieve_data.return_value = None

        with (
            patch("retrieval.fetch_data.datetime") as mock_dt,
            patch("retrieval.fetch_data.rmtree"),
            patch("pathlib.Path.exists", return_value=True),
        ):
            mock_dt.today.return_value.date.return_value = "2023-01-01"
            await retrieve_all_data()

        assert mock_retrieve_data.call_count == 2
        mock_compress_data.assert_not_called()
        mock_send_to_dropbox.assert_not_called()

    @pytest.mark.asyncio
    @patch("retrieval.fetch_data.asyncio.gather")
    @patch("retrieval.fetch_data.compress_data")
    @patch("retrieval.fetch_data.send_to_dropbox")
    async def test_retrieve_all_data_gather_exception(
        self,
        mock_send_to_dropbox,
        mock_compress_data,
        mock_gather,
    ):
        """Unexpected gather exception propagates correctly."""
        mock_gather.side_effect = Exception("Test error")

        with pytest.raises(Exception, match="Test error"):
            await retrieve_all_data()

        mock_compress_data.assert_not_called()
        mock_send_to_dropbox.assert_not_called()
