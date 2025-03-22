"""
Logging configuration for ImageHarvester
"""

import os
import logging
from datetime import datetime
from pathlib import Path

def setup_logging(level=logging.INFO):
    """
    Configure logging for the application
    
    Args:
        level: The logging level (default: logging.INFO)
    
    Returns:
        The configured logger instance
    """
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Generate a filename based on the current date and time
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"image_harvester_{timestamp}.log"
    
    # Configure the root logger
    logger = logging.getLogger("image_harvester")
    logger.setLevel(level)
    
    # Clear any existing handlers
    if logger.handlers:
        logger.handlers.clear()
    
    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # Create formatter and add it to the handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info("Logging initialized")
    return logger

def get_logger(name):
    """
    Get a named logger for a module
    
    Args:
        name: The name of the logger (usually __name__)
    
    Returns:
        A logger instance
    """
    return logging.getLogger(f"image_harvester.{name}")
