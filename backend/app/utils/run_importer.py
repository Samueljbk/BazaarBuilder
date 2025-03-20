# app/utils/run_importer.py

import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

# Use absolute import
from app.utils.data_importer import DataImporter
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Run the data importer."""
    logger.info("Starting data import")
    
    importer = DataImporter()
    success = importer.run()
    
    if success:
        logger.info("Data import completed successfully")
    else:
        logger.error("Data import failed")

if __name__ == "__main__":
    main()