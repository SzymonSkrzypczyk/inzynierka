from pathlib import Path
from typing import Union
import logging
from logging.handlers import RotatingFileHandler

LOGGING_PATH = Path(__file__).parent / "logs.log"


class Logger:
    def __init__(self, logging_path: Union[str, Path] = LOGGING_PATH):
        self.logging_path = Path(logging_path)
        self.logger = self.setup_logger()

    def setup_logger(self):
        """
        Set up logging configuration
        """
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            file_handler = RotatingFileHandler(self.logging_path, maxBytes=5 * 1024 * 1024, backupCount=5)
            file_handler.setLevel(logging.INFO)

            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

        logger.propagate = False

        return logger

    def log(self, message: str):
        """
        Log a message
        """
        self.logger.info(message)

    def log_error(self, message: str):
        """
        Log an error message
        """
        self.logger.error(message)

    def log_warning(self, message: str):
        """
        Log a warning message
        """
        self.logger.warning(message)

    def log_debug(self, message: str):
        """
        Log a debug message
        """
        self.logger.debug(message)

    def log_exception(self, message: str):
        """
        Log an exception message
        """
        self.logger.exception(message)
