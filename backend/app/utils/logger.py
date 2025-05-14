import logging
from logging.handlers import RotatingFileHandler
import os
from flask import current_app

def setup_logger():
    """Configure and return a logger instance."""
    logger = logging.getLogger('trade_monitor')
    logger.setLevel(logging.INFO)

    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )

    # File handler
    file_handler = RotatingFileHandler(
        current_app.config['LOG_FILE'],
        maxBytes=1024 * 1024,  # 1MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

def log_info(message):
    """Log an info message."""
    logger = logging.getLogger('trade_monitor')
    logger.info(message)

def log_warning(message):
    """Log a warning message."""
    logger = logging.getLogger('trade_monitor')
    logger.warning(message)

def log_error(message):
    """Log an error message."""
    logger = logging.getLogger('trade_monitor')
    logger.error(message)

def log_success(message):
    """Log a success message."""
    logger = logging.getLogger('trade_monitor')
    logger.info(f"SUCCESS: {message}") 