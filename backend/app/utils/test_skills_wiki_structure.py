# app/utils/test_skills_wiki_structure.py

import requests
from bs4 import BeautifulSoup

def get_page_content(url):
    """Get the HTML content of a wiki page."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        return response.text
    except Exception as e:
        print(f"Error fetching page {url}: {e}")
        return None

def analyze_page_structure(html_content):
    """Analyze the structure of the page."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all headers
    headers = []
    for header in soup.find_all(['h1', 'h2', 'h3', 'h4']):
        headers.append(header)
    
    print("Headers found on page:")
    for header in headers:
        print(f"  - {header.name}: {header.text.strip()}")
    
    # Look for tables
    print("\nAnalyzing tables:")
    tables = soup.find_all('table')
    for i, table in enumerate(tables):
        print(f"\nTable {i+1}:")
        
        # Get table headers
        th_elements = table.find_all('th')
        if th_elements:
            header_texts = [th.text.strip() for th in th_elements]
            print(f"  Headers: {header_texts}")
        
        # Get sample rows (up to 2)
        rows = table.find_all('tr')
        data_rows = [row for row in rows if row.find('td')]  # Only rows with data cells
        
        for j, row in enumerate(data_rows[:2]):  # Get up to 2 sample rows
            cells = row.find_all('td')
            cell_texts = [cell.text.strip() for cell in cells]
            print(f"  Sample row {j+1}: {cell_texts}")
        
        # Try to determine what the preceding header is
        preceding_header = None
        for header in headers:
            if header.find_next('table') == table:
                preceding_header = header
                break
        
        if preceding_header:
            print(f"  Preceding header: {preceding_header.text.strip()}")
        else:
            print("  No preceding header found")

def main():
    # Test with one hero's skill page
    url = "https://thebazaar.wiki.gg/wiki/Dooley_Skills"
    print(f"Analyzing page structure for: {url}")
    html_content = get_page_content(url)
    
    if html_content:
        analyze_page_structure(html_content)
    else:
        print("Failed to fetch page content")
    
    # You could add more URLs to test other pages
    # For example, monster skills or other heroes

if __name__ == "__main__":
    main()