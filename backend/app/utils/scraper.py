# app/utils/scraper.py

import requests
from bs4 import BeautifulSoup
import logging
from typing import Dict, Any, Optional, List

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WikiScraper:
    """Base scraper for The Bazaar wiki."""
    
    BASE_URL = "https://thebazaar.wiki.gg/wiki/"
    
    def __init__(self):
        """Initialize the wiki scraper."""
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