# app/utils/run_item_scraper.py

# Change from relative import to direct import
from item_scraper import ItemScraper
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Run the item scraper."""
    logger.info("Starting item scraper")
    
    scraper = ItemScraper(output_path="data/items.json")
    success = scraper.run()
    
    if success:
        logger.info("Item scraping completed successfully")
    else:
        logger.error("Item scraping failed")

if __name__ == "__main__":
    main()