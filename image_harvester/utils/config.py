"""
Configuration management for ImageHarvester
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from image_harvester.utils.logging import get_logger

logger = get_logger(__name__)

# Load environment variables from .env file if it exists
env_path = Path('.env')
if env_path.exists():
    logger.info(f"Loading environment from {env_path.absolute()}")
    load_dotenv(dotenv_path=env_path)
else:
    logger.warning(f"No .env file found at {env_path.absolute()}, using default environment")

# API Configuration
BING_SEARCH_API_KEY = os.getenv('BING_SEARCH_API_KEY')
BING_SEARCH_ENDPOINT = os.getenv('BING_SEARCH_ENDPOINT', 'https://api.bing.microsoft.com/v7.0/images/search')

# Application Configuration
MAX_IMAGES_PER_SEARCH = int(os.getenv('MAX_IMAGES_PER_SEARCH', 100))
DEFAULT_IMAGE_MIN_WIDTH = int(os.getenv('DEFAULT_IMAGE_MIN_WIDTH', 400))
DEFAULT_IMAGE_MIN_HEIGHT = int(os.getenv('DEFAULT_IMAGE_MIN_HEIGHT', 400))
DEFAULT_REQUEST_DELAY = float(os.getenv('DEFAULT_REQUEST_DELAY', 1.0))
MAX_RETRY_ATTEMPTS = int(os.getenv('MAX_RETRY_ATTEMPTS', 3))

def validate_config():
    """
    Validate that the configuration is valid
    
    Returns:
        bool: True if config is valid, False otherwise
    """
    if BING_SEARCH_API_KEY is None:
        logger.error("BING_SEARCH_API_KEY is not set in environment or .env file")
        return False
    
    if not BING_SEARCH_ENDPOINT:
        logger.error("BING_SEARCH_ENDPOINT is not set in environment or .env file")
        return False
    
    return True
