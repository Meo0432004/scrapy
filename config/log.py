"""
This module configures logging for the application.

It provides utility functions for logging messages and errors to a log file.
The log file is named 'scraper.log' and contains timestamps, log levels, and messages.
"""

import logging

# Basic logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="scraper.log",  # Log output to this file
    filemode="a",  # Append to file
)

# Get the logger
logger = logging.getLogger(__name__)


def log_message(message):
    """
    Logs an informational message.

    :param message: The message to log.
    """
    logger.info(message)


def log_error(message, error=None):
    """
    Logs an error message and optionally logs an exception traceback.

    :param message: The error message to log.
    :param error: An optional exception object for traceback logging.
    """
    logger.error(message)
    if error:
        logger.exception(error)
