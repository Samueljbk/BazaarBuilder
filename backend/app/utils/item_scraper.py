# app/utils/item_scraper.py

import json
import os
import re
from typing import Dict, List, Any, Optional
import logging
import requests
from bs4 import BeautifulSoup
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from app.models.item import ItemSize, ItemSource

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ItemScraper:
    """Specialized scraper for item data from The Bazaar wiki."""
    
    # Base URL for the wiki
    BASE_URL = "https://thebazaar.wiki.gg/wiki/"
    
    # Hero and monster item pages
    ITEM_PAGES = {
        "Dooley": "Dooley_Items",
        "Pygmalien": "Pygmalien_Items",
        "Vanessa": "Vanessa_Items",
        "Mak": "Mak_Items",
        "Stelle": "Stelle_Items",
        "Jules": "Jules_Items",
        "Monster": "Monster_Items",  # Special case for monster items
    }
    
    # Hero name to ID mapping (adjust based on your database)
    HERO_NAME_TO_ID = {
        "Dooley": 1,
        "Pygmalien": 2,
        "Vanessa": 3,
        "Mak": 4,
        "Stelle": 5,
        "Jules": 6
    }
    
    def __init__(self, output_path: str = "data/items.json"):
        """Initialize the item scraper.
        
        Args:
            output_path: Path where the scraped item data will be saved
        """
        self.output_path = output_path
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def get_page_content(self, page_name: str) -> Optional[BeautifulSoup]:
        """Get the HTML content of a wiki page.
        
        Args:
            page_name: The name of the page to scrape
            
        Returns:
            BeautifulSoup object or None if the request fails
        """
        url = f"{self.BASE_URL}{page_name}"
        
        try:
            logger.info(f"Fetching page: {url}")
            response = self.session.get(url, headers=self.headers)
            response.raise_for_status()
            
            return BeautifulSoup(response.text, 'html.parser')
            
        except Exception as e:
            logger.error(f"Error fetching page {url}: {e}")
            return None
    
    def extract_cooldown(self, effect_text: str) -> Optional[float]:
        """Extract cooldown value from effect text.
        
        Args:
            effect_text: Text containing effect description
            
        Returns:
            Cooldown as a float, or None if not found
        """
        # We won't use this as we're getting cooldown from its own column
        return None
    
    def parse_cooldown(self, cooldown_text: str) -> Optional[float]:
        """Parse cooldown value from cooldown text.
        
        Args:
            cooldown_text: Text containing cooldown information
            
        Returns:
            Cooldown as a float, or None if not found
        """
        if not cooldown_text or cooldown_text == '–':
            return None
            
        # Extract numbers from text using regex
        match = re.search(r'(\d+(?:\.\d+)?)', cooldown_text)
        if match:
            return float(match.group(1))
        
        return None
    
    def parse_item_table(self, table, size: ItemSize, source_type: ItemSource, hero_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Parse an item table from the page.
        
        Args:
            table: BeautifulSoup table element
            size: Size of the items in this table
            source_type: Source type of the items
            hero_id: ID of the hero if these are hero-specific items
            
        Returns:
            List of dictionaries containing item data
        """
        items = []
        
        # Get all data rows (skip header row)
        rows = table.find_all('tr')
        data_rows = [row for row in rows if row.find('td')]
        
        for row in data_rows:
            cells = row.find_all('td')
            
            if len(cells) >= 5:  # Ensure we have enough columns
                name = cells[0].text.strip()
                effect = cells[1].text.strip()
                cooldown_text = cells[2].text.strip()
                ammo_text = cells[3].text.strip()
                types_text = cells[4].text.strip()
                
                # Parse cooldown
                cooldown = self.parse_cooldown(cooldown_text)
                
                # Determine monster_id if this is a monster item
                monster_id = None
                if source_type == ItemSource.MONSTER:
                    # In a real implementation, we would look up or create the monster
                    # For now, we'll leave it as None
                    monster_id = None
                
                item_data = {
                    "name": name,
                    "description": effect,  # Using effect as description
                    "size": size.value,
                    "source": source_type.value,
                    "hero_id": hero_id,
                    "monster_id": monster_id,
                    "cooldown": cooldown,
                    "effect": effect,
                    "cost": None,  # Cost information isn't available in the table
                    "types": types_text  # Additional field for item types
                }
                
                items.append(item_data)
        
        return items
    
    def scrape_items_from_page(self, hero_name: str, page_name: str) -> List[Dict[str, Any]]:
        """Scrape items from a hero or monster page.
        
        Args:
            hero_name: Name of the hero or "Monster" for monster items
            page_name: Wiki page name for the items
            
        Returns:
            List of dictionaries containing item data
        """
        items = []
        soup = self.get_page_content(page_name)
        
        if not soup:
            logger.error(f"Failed to fetch page content for {page_name}")
            return items
        
        # Determine source type and hero_id
        source_type = ItemSource.HERO_SPECIFIC
        hero_id = None
        
        if hero_name == "Monster":
            source_type = ItemSource.MONSTER
        else:
            hero_id = self.HERO_NAME_TO_ID.get(hero_name)
            if not hero_id:
                logger.warning(f"Unknown hero: {hero_name}")
                return items
        
        # Find sections for Small, Medium, and Large items
        size_headers = []
        for header in soup.find_all(['h2', 'h3']):
            text = header.text.lower().strip()
            if "small items" in text:
                size_headers.append((header, ItemSize.SMALL))
            elif "medium items" in text:
                size_headers.append((header, ItemSize.MEDIUM))
            elif "large items" in text:
                size_headers.append((header, ItemSize.LARGE))
        
        # Process each section
        for header, size in size_headers:
            # Find the next table after this header
            table = header.find_next('table')
            if table:
                section_items = self.parse_item_table(table, size, source_type, hero_id)
                items.extend(section_items)
                logger.info(f"Found {len(section_items)} {size.value} items for {hero_name}")
            else:
                logger.warning(f"No table found for {size.value} items for {hero_name}")
        
        return items
    
    def scrape_all_items(self) -> List[Dict[str, Any]]:
        """Scrape data for all items from all pages.
        
        Returns:
            List of dictionaries containing item data
        """
        all_items = []
        
        for hero_name, page_name in self.ITEM_PAGES.items():
            logger.info(f"Scraping items for {hero_name}")
            items = self.scrape_items_from_page(hero_name, page_name)
            all_items.extend(items)
            logger.info(f"Found {len(items)} items for {hero_name}")
        
        return all_items
    
    def save_to_json(self, items: List[Dict[str, Any]]) -> bool:
        """Save the scraped item data to a JSON file.
        
        Args:
            items: List of dictionaries containing item data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
            
            with open(self.output_path, 'w', encoding='utf-8') as f:
                json.dump(items, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Successfully saved item data to {self.output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving item data to {self.output_path}: {e}")
            return False
    
    def run(self) -> bool:
        """Run the complete item scraping process.
        
        Returns:
            True if successful, False otherwise
        """
        items = self.scrape_all_items()
        
        if not items:
            logger.error("No item data was scraped")
            return False
        
        return self.save_to_json(items)