import json
import os
from typing import Dict, List, Any, Optional
import logging
from .scraper import WikiScraper

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class HeroScraper:
    """Specialized scraper for hero data from The Bazaar wiki."""
    
    HERO_PAGES = [
        "Dooley",
        "Pygmalien",
        "Vanessa"
    ]
    
    def __init__(self, output_path: str = "data/heroes.json"):
        """Initialize the hero scraper.
        
        Args:
            output_path: Path where the scraped hero data will be saved
        """
        self.output_path = output_path
        self.scraper = WikiScraper()
    
    def scrape_all_heroes(self) -> List[Dict[str, Any]]:
        """Scrape data for all heroes.
        
        Returns:
            List of dictionaries containing hero data
        """
        heroes = []
        
        for hero_name in self.HERO_PAGES:
            logger.info(f"Scraping hero: {hero_name}")
            hero_data = self.scraper.parse_hero_page(hero_name)
            
            if hero_data:
                heroes.append(hero_data)
                logger.info(f"Successfully scraped data for {hero_name}")
            else:
                logger.error(f"Failed to scrape data for {hero_name}")
        
        return heroes
    
    def save_to_json(self, heroes: List[Dict[str, Any]]) -> bool:
        """Save the scraped hero data to a JSON file.
        
        Args:
            heroes: List of dictionaries containing hero data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
            
            with open(self.output_path, 'w', encoding='utf-8') as f:
                json.dump(heroes, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Successfully saved hero data to {self.output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving hero data to {self.output_path}: {e}")
            return False
    
    def run(self) -> bool:
        """Run the complete hero scraping process.
        
        Returns:
            True if successful, False otherwise
        """
        heroes = self.scrape_all_heroes()
        
        if not heroes:
            logger.error("No hero data was scraped")
            return False
        
        return self.save_to_json(heroes)