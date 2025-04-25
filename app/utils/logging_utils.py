"""
Logging utilities for the application
"""

import os
import logging
from datetime import datetime
from .config import LOGS_PATH

def setup_logging():
    """
    Configure logging for the application
    """
    # Create logs directory if it doesn't exist
    os.makedirs(LOGS_PATH, exist_ok=True)
    
    # Generate a log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(LOGS_PATH, f"app_{timestamp}.log")
    
    # Configure the logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    # Log the start of the application
    logging.info("Application logging initialized") 