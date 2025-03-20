import logging
import sys
import os

# Add the parent directory to the path so we can import modules properly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.utils.bazaar_scraper import BazaarScraper

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Run the data scraping process."""
    logger.info("Starting the Bazaar scraping process")
    
    # Create a scraper instance
    scraper = BazaarScraper()
    
    try:
        # Run the scraper
        success = scraper.run()
        
        if success:
            logger.info("Bazaar scraping completed successfully")
        else:
            logger.error("Bazaar scraping failed")
            return 1
            
        logger.info("All scraping tasks completed")
        return 0
    except KeyboardInterrupt:
        logger.info("Process terminated by user")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1
    finally:
        # Ensure we clean up properly
        logger.info("Cleaning up resources...")
        scraper.close()

if __name__ == "__main__":
    sys.exit(main())