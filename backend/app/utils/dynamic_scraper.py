import json
import logging
import os
from typing import Dict, List, Any, Optional

from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DynamicWebScraper:
    """Base class for scraping dynamic websites using Playwright."""
    
    def __init__(self, base_url: str, output_dir: str = "data", headless: bool = True):
        """Initialize the dynamic web scraper.
        
        Args:
            base_url: The base URL of the website to scrape
            output_dir: Directory where scraped data will be saved
            headless: Whether to run the browser in headless mode
        """
        self.base_url = base_url
        self.output_dir = output_dir
        self.headless = headless
        self.browser = None
        self.context = None
        self.playwright = None
        
    def initialize(self):
        """Initialize the browser and context."""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.context = self.browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        
    def close(self):
        """Close the browser and context properly."""
        try:
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
        except Exception as e:
            logger.error(f"Error during browser cleanup: {e}")
            
    def new_page(self) -> Page:
        """Create a new browser page.
        
        Returns:
            A new browser page
        """
        if not self.context:
            self.initialize()
        return self.context.new_page()
    
    def navigate(self, page: Page, path: str, wait_selector: str = None):
        """Navigate to a URL and wait for a selector if provided.
        
        Args:
            page: The browser page
            path: The path to navigate to (will be appended to base_url)
            wait_selector: CSS selector to wait for after navigation
            
        Returns:
            True if navigation was successful, False otherwise
        """
        url = f"{self.base_url}/{path.lstrip('/')}"
        try:
            # Use a less strict wait condition and shorter timeout
            page.goto(url, wait_until="domcontentloaded", timeout=15000)
            
            # Manual wait to allow some JavaScript to load
            page.wait_for_timeout(2000)
            
            if wait_selector:
                try:
                    page.wait_for_selector(wait_selector, timeout=5000)
                except:
                    logger.warning(f"Selector '{wait_selector}' not found, but continuing anyway")
                
            return True
        except Exception as e:
            logger.error(f"Error navigating to {url}: {e}")
            return False
    
    def extract_json_from_script(self, page: Page, script_id: str = None, contains: str = None) -> Optional[Dict]:
        """Extract JSON data from a <script> tag.
        
        Args:
            page: The browser page
            script_id: ID attribute of the script tag
            contains: String that the script content should contain
            
        Returns:
            Parsed JSON data if found, None otherwise
        """
        if script_id:
            script = page.evaluate(f'document.getElementById("{script_id}")?.textContent')
        elif contains:
            script = page.evaluate(f'''
                Array.from(document.getElementsByTagName('script'))
                    .find(s => s.textContent.includes('{contains}'))?.textContent
            ''')
        else:
            return None
            
        if not script:
            return None
            
        try:
            # Find JSON-like content inside the script
            start_idx = script.find('{')
            if start_idx == -1:
                return None
                
            # Try to balance brackets to find the end of the JSON
            open_brackets = 0
            for i in range(start_idx, len(script)):
                if script[i] == '{':
                    open_brackets += 1
                elif script[i] == '}':
                    open_brackets -= 1
                    if open_brackets == 0:
                        json_str = script[start_idx:i+1]
                        return json.loads(json_str)
                        
            return None
        except Exception as e:
            logger.error(f"Error extracting JSON: {e}")
            return None
            
    def save_to_json(self, data: Any, filename: str) -> bool:
        """Save data to a JSON file.
        
        Args:
            data: Data to save
            filename: Name of the file (will be saved in output_dir)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure the directory exists
            os.makedirs(self.output_dir, exist_ok=True)
            
            filepath = os.path.join(self.output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            logger.info(f"Successfully saved data to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error saving data to {filename}: {e}")
            return False