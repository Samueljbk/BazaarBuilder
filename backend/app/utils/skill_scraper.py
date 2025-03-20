# app/utils/skill_scraper.py

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

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SkillScraper:
    """Specialized scraper for skill data from The Bazaar wiki."""
    
    # Base URL for the wiki
    BASE_URL = "https://thebazaar.wiki.gg/wiki/"
    
    # Hero and monster skill pages
    SKILL_PAGES = {
        "Dooley": "Dooley_Skills",
        "Pygmalien": "Pygmalien_Skills",
        "Vanessa": "Vanessa_Skills", 
        "Mak": "Mak_Skills",
        "Stelle": "Stelle_Skills",
        "Jules": "Jules_Skills",
        "Monster": "Monster_Skills",  # Special case for monster skills
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
    
    def __init__(self, output_path: str = "data/skills.json"):
        """Initialize the skill scraper.
        
        Args:
            output_path: Path where the scraped skill data will be saved
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
    
    def parse_skill_table(self, table, source_type: str, hero_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Parse a skill table from the page.
        
        Args:
            table: BeautifulSoup table element
            source_type: Source type of the skills
            hero_id: ID of the hero if these are hero-specific skills
            
        Returns:
            List of dictionaries containing skill data
        """
        skills = []
        
        # Get all data rows (skip header row)
        rows = table.find_all('tr')
        data_rows = [row for row in rows if row.find('td')]
        
        for row in data_rows:
            cells = row.find_all('td')
            
            if len(cells) >= 5:  # Ensure we have enough columns
                # Sprite is at index 0 (we'll ignore it)
                name = cells[1].text.strip()
                effect = cells[2].text.strip()
                tier = cells[3].text.strip()
                types = cells[4].text.strip()
                
                # Determine monster_id if this is a monster skill
                monster_id = None
                if source_type == "monster":
                    # In a real implementation, we would look up or create the monster
                    # For now, we'll leave it as None
                    monster_id = None
                
                skill_data = {
                    "name": name,
                    "description": effect,
                    "source": source_type,
                    "hero_id": hero_id,
                    "monster_id": monster_id,
                    "tier": tier,
                    "effect": effect,
                    "types": types
                }
                
                skills.append(skill_data)
        
        return skills
    
    def scrape_skills_from_page(self, hero_name: str, page_name: str) -> List[Dict[str, Any]]:
        """Scrape skills from a hero or monster page.
        
        Args:
            hero_name: Name of the hero or "Monster" for monster skills
            page_name: Wiki page name for the skills
            
        Returns:
            List of dictionaries containing skill data
        """
        skills = []
        soup = self.get_page_content(page_name)
        
        if not soup:
            logger.error(f"Failed to fetch page content for {page_name}")
            return skills
        
        # Determine source type and hero_id
        source_type = "hero_specific"
        hero_id = None
        
        if hero_name == "Monster":
            source_type = "monster"
        else:
            hero_id = self.HERO_NAME_TO_ID.get(hero_name)
            if not hero_id:
                logger.warning(f"Unknown hero: {hero_name}")
                return skills
        
        # Find the main content area
        content_div = soup.find('div', {'id': 'mw-content-text'})
        if not content_div:
            logger.warning(f"Could not find main content area for {hero_name}")
            return skills
            
        # Find tables in the content area
        tables = content_div.find_all('table', class_='wikitable')
        
        if not tables:
            logger.warning(f"No skill tables found for {hero_name}")
            return skills
        
        # Process each table
        for table in tables:
            section_skills = self.parse_skill_table(table, source_type, hero_id)
            skills.extend(section_skills)
            logger.info(f"Found {len(section_skills)} skills in table for {hero_name}")
        
        return skills
    
    def scrape_all_skills(self) -> List[Dict[str, Any]]:
        """Scrape data for all skills from all pages.
        
        Returns:
            List of dictionaries containing skill data
        """
        all_skills = []
        
        for hero_name, page_name in self.SKILL_PAGES.items():
            logger.info(f"Scraping skills for {hero_name}")
            skills = self.scrape_skills_from_page(hero_name, page_name)
            all_skills.extend(skills)
            logger.info(f"Found {len(skills)} skills for {hero_name}")
        
        return all_skills
    
    def save_to_json(self, skills: List[Dict[str, Any]]) -> bool:
        """Save the scraped skill data to a JSON file.
        
        Args:
            skills: List of dictionaries containing skill data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
            
            with open(self.output_path, 'w', encoding='utf-8') as f:
                json.dump(skills, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Successfully saved skill data to {self.output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving skill data to {self.output_path}: {e}")
            return False
    
    def run(self) -> bool:
        """Run the complete skill scraping process.
        
        Returns:
            True if successful, False otherwise
        """
        skills = self.scrape_all_skills()
        
        if not skills:
            logger.error("No skill data was scraped")
            return False
        
        return self.save_to_json(skills)