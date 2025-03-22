"""
Main module for the ImageHarvester application.
This is where the application is initialized and started.
"""

import os
import sys
from image_harvester import __version__
from image_harvester.utils.logging import setup_logging, get_logger

# Set up logging
logger = setup_logging()
module_logger = get_logger(__name__)

def main():
    """
    Main entry point for the application.
    Initializes the UI and starts the application.
    """
    module_logger.info(f"Starting ImageHarvester version {__version__}")
    
    # TODO: Initialize UI and start the application
    module_logger.info("Application initialized")
    
    # Placeholder for actual application startup
    module_logger.warning("Application not yet implemented!")

if __name__ == "__main__":
    main()
