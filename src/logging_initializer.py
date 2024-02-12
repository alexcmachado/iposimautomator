"""Initialize logging module."""

import logging
import os
import platform
import sys
from logging.handlers import RotatingFileHandler

from constants import MAX_LOG_FILE_SIZE, LOG_FILE_NAME


def get_log_dir():
    """Get the log directory for the current platform."""
    if platform.system() == "Windows":
        try:
            log_dir = os.environ["TMP"]
        except KeyError:
            log_dir = os.getcwd()
    else:
        log_dir = "/tmp"
    return log_dir


def logger_init():
    """Initialize logging module and return a logger."""
    log_dir = get_log_dir()
    log_file_path = os.path.join(log_dir, LOG_FILE_NAME)

    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)

    # create logger from root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = RotatingFileHandler(log_file_path, maxBytes=MAX_LOG_FILE_SIZE, backupCount=4)
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    # create formatter and add it to the handlers
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_formatter = logging.Formatter("%(message)s")
    fh.setFormatter(file_formatter)
    ch.setFormatter(console_formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger
