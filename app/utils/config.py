"""
Configuration module handling environment variables and application settings
"""

import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Paths
DATA_PATH = os.getenv("DATA_PATH", "data/")
VECTORSTORE_PATH = os.getenv("VECTORSTORE_PATH", "vectorstore/db_faiss")
LOGS_PATH = os.getenv("LOGS_PATH", "logs/")

# Models
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

# Create necessary directories if they don't exist
def ensure_directories():
    """Ensure that all necessary directories exist."""
    dirs = [DATA_PATH, os.path.dirname(VECTORSTORE_PATH), LOGS_PATH]
    for dir_path in dirs:
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path, exist_ok=True)
                logging.info(f"Created directory: {dir_path}")
            except Exception as e:
                logging.error(f"Failed to create directory {dir_path}: {e}") 