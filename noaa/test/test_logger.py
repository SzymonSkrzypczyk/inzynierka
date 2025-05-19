from pathlib import Path
import pytest

from noaa.logger import Logger

LOG_FILE_PATH = Path(__file__).parent / "test_logs.log"


@pytest.fixture(scope="session", autouse=True)
def cleanup_logs():
    yield  # This runs your tests
    if LOG_FILE_PATH.exists():
        LOG_FILE_PATH.unlink()


@pytest.fixture
def logger():
    """
    Fixture to create a Logger instance for testing.
    """
    return Logger(logging_path=LOG_FILE_PATH)


def test_logger_initialization(logger):
    """
    Test the initialization of the Logger class.
    """
    assert logger is not None
    assert isinstance(logger, Logger)
    assert logger.logging_path.exists()
    assert logger.logging_path.is_file()
    assert logger.logging_path.stat().st_size == 0


def test_log_message(logger):
    """
    Test logging a message.
    """
    logger.log("Test log message")
    with open(logger.logging_path, "r") as f:
        logs = f.readlines()
        assert len(logs) == 1
        assert "Test log message" in logs[0]


def test_log_error(logger):
    """
    Test logging an error message.
    """
    logger.log_error("Test error message")
    with open(logger.logging_path, "r") as f:
        logs = f.readlines()
        assert len(logs) == 2
        assert "Test error message" in logs[1]


def test_log_warning(logger):
    """
    Test logging a warning message.
    """
    logger.log_warning("Test warning message")
    with open(logger.logging_path, "r") as f:
        logs = f.readlines()
        assert len(logs) == 3
        assert "Test warning message" in logs[2]


def test_log_exception(logger):
    """
    Test logging an exception message.
    """
    try:
        raise ValueError("Test exception")
    except Exception as e:
        logger.log_exception(e)

    with open(logger.logging_path, "r") as f:
        logs = f.readlines()
        assert len(logs) == 8
        assert "Test exception" in logs[3]


def test_log_file_size(logger):
    """
    Test the size of the log file.
    """
    logger.log("Test log message")
    assert logger.logging_path.stat().st_size > 0
