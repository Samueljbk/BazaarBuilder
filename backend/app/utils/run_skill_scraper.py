# app/utils/run_skill_scraper.py

import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

# Now use absolute imports
from app.utils.skill_scraper import SkillScraper
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Run the skill scraper."""
    logger.info("Starting skill scraper")
    
    scraper = SkillScraper(output_path="data/skills.json")
    success = scraper.run()
    
    if success:
        logger.info("Skill scraping completed successfully")
    else:
        logger.error("Skill scraping failed")

if __name__ == "__main__":
    main()