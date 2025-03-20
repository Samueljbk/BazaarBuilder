import argparse
import logging
import sys
import os

# Add the parent directory to the path so we can import modules properly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.utils.bazaar_scraper import BazaarScraper

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def scrape_with_cleanup(scrape_func, output_filename):
    """Run a scrape function with proper cleanup."""
    scraper = BazaarScraper()
    try:
        scraper.initialize()
        data = scrape_func(scraper)
        if data:
            scraper.save_to_json(data, output_filename)
            return len(data) > 0
        return False
    except Exception as e:
        logger.error(f"Error during scraping: {e}")
        return False
    finally:
        scraper.close()

def main():
    parser = argparse.ArgumentParser(description='Scrape data from The Bazaar game websites')
    parser.add_argument('--all', action='store_true', help='Scrape all data types')
    parser.add_argument('--heroes', action='store_true', help='Scrape hero data')
    parser.add_argument('--items', action='store_true', help='Scrape item data')
    parser.add_argument('--skills', action='store_true', help='Scrape skill data')
    parser.add_argument('--monsters', action='store_true', help='Scrape monster data')
    parser.add_argument('--merchants', action='store_true', help='Scrape merchant data')
    
    args = parser.parse_args()
    
    # If no arguments provided, default to --all
    if not any(vars(args).values()):
        args.all = True
    
    success = True
    
    if args.all:
        scraper = BazaarScraper()
        try:
            scraper.initialize()
            success = scraper.run()
        finally:
            scraper.close()
    else:
        if args.heroes:
            heroes_success = scrape_with_cleanup(
                lambda s: s.scrape_heroes(), 
                "heroes.json"
            )
            success = success and heroes_success
            
        if args.items:
            items_success = scrape_with_cleanup(
                lambda s: s.scrape_items(),
                "items.json"
            )
            success = success and items_success
            
        if args.skills:
            skills_success = scrape_with_cleanup(
                lambda s: s.scrape_skills(),
                "skills.json"
            )
            success = success and skills_success
            
        if args.monsters:
            monsters_success = scrape_with_cleanup(
                lambda s: s.scrape_monsters(),
                "monsters.json"
            )
            success = success and monsters_success
            
        if args.merchants:
            merchants_success = scrape_with_cleanup(
                lambda s: s.scrape_merchants(),
                "merchants.json"
            )
            success = success and merchants_success
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())