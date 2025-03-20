import logging
import sys
import os

# Add the parent directory to the path so we can import modules properly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.utils.hero_scraper import HeroScraper

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Run the data scraping process."""
    logger.info("Starting the hero scraping process")
    
    # Scrape hero data
    hero_scraper = HeroScraper()
    success = hero_scraper.run()
    
    if success:
        logger.info("Hero scraping completed successfully")
    else:
        logger.error("Hero scraping failed")
        return 1
    
    logger.info("All scraping tasks completed")
    return 0

if __name__ == "__main__":
    sys.exit(main())