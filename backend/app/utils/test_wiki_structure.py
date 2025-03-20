# app/utils/test_wiki_structure.py

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
    
    # Find all headers that might indicate item size sections
    size_headers = []
    for header in soup.find_all(['h2', 'h3']):
        if any(size in header.text.lower() for size in ['small', 'medium', 'large']):
            size_headers.append(header)
    
    print("Item size headers found on page:")
    for header in size_headers:
        print(f"  - {header.text.strip()}")
    
    # Look for tables and their relationships to headers
    print("\nAnalyzing tables by section:")
    for header in size_headers:
        # Find the next table after this header
        table = header.find_next('table')
        if table:
            print(f"\nTable for {header.text.strip()}:")
            
            # Get table headers
            th_elements = table.find_all('th')
            if th_elements:
                header_texts = [th.text.strip() for th in th_elements]
                print(f"  Headers: {header_texts}")
            
            # Get sample rows (up to 2)
            rows = table.find_all('tr')
            data_rows = [row for row in rows if row.find('td')]  # Only rows with data cells
            
            for i, row in enumerate(data_rows[:2]):  # Get up to 2 sample rows
                cells = row.find_all('td')
                cell_texts = [cell.text.strip() for cell in cells]
                print(f"  Sample row {i+1}: {cell_texts}")
        else:
            print(f"No table found for {header.text.strip()}")

def main():
    # Test with one hero's item page
    url = "https://thebazaar.wiki.gg/wiki/Dooley_Items"
    html_content = get_page_content(url)
    
    if html_content:
        analyze_page_structure(html_content)
    else:
        print("Failed to fetch page content")

if __name__ == "__main__":
    main()