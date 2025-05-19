from pathlib import Path
from typing import Union
import logging


class Logger:
    def __init__(self, logger_path: Union[str, Path]):
        self.logger_path = logger_path
        self.logger = self._setup_logger()


    def _setup_logger(self):
        """
        Setup the logger with a file handler and formatter.
        """
        logger = logging.getLogger(__name__)
        # Create a file handler
        file_handler = logging.FileHandler(self.logger_path)

        # Create a formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Set the formatter for the handler
        file_handler.setFormatter(formatter)

        # Add the handler to the logger
        logger.addHandler(file_handler)

        return logger

    def log(self, message: str, level: str = "info"):
        """
        Log a message with the specified level.

        :param message: The message to log
        :param level: The logging level (default is "info")
        """
        if level == "info":
            self.logger.info(message)
        elif level == "warning":
            self.logger.warning(message)
        elif level == "error":
            self.logger.error(message)
        elif level == "debug":
            self.logger.debug(message)
        else:
            raise ValueError(f"Invalid logging level: {level}")

    def log_info(self, message: str):
        """
        Log an info message.

        :param message: The message to log
        """
        self.log(message, level="info")

    def log_error(self, message: str):
        """
        Log an error message.

        :param message: The message to log
        """
        self.log(message, level="error")

    def log_warning(self, message: str):
        """
        Log a warning message.

        :param message: The message to log
        """
        self.log(message, level="warning")

    def log_exception(self, exception: Exception):
        """
        Log an exception with traceback.

        :param exception: The exception to log
        """
        self.logger.exception("An error occurred", exc_info=exception)
