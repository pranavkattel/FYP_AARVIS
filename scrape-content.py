import requests
from bs4 import BeautifulSoup

# Send a GET request to the website
with open('links.txt', 'r') as f:
    urls = [url.strip() for url in f.readlines()]
    total_urls = len(urls)
    print(f"Found {total_urls} URLs to scrape")
    
    for i, url in enumerate(urls, 1):
        print(f"Scraping {i}/{total_urls}: {url}")
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises an exception for bad status codes
            
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the content within the class 'entry-content'
            entry_content = soup.find('div', class_='entry-content')
            
            if entry_content is None:
                print(f"  ❌ No 'entry-content' div found for {url}")
                continue

            # Open a text file to save the content (append mode for multiple URLs)
            with open('content.md', 'a', encoding='utf-8') as file:
                file.write(f"\n\n--- Content from {url} ---\n\n")
                
                # Loop through each paragraph, heading, and list item to preserve formatting in Markdown
                elements_found = 0
                for element in entry_content.find_all(['p', 'h2', 'ul', 'ol', 'li']):
                    elements_found += 1
                    if element.name == 'p':
                        file.write(element.get_text(strip=True) + '\n\n')
                    elif element.name == 'h2':
                        file.write('\n## ' + element.get_text(strip=True) + '\n\n')
                    elif element.name == 'li':
                        file.write('- ' + element.get_text(strip=True) + '\n')
                    elif element.name in ['ul', 'ol']:
                        file.write('\n'.join([li.get_text(strip=True) for li in element.find_all('li')]) + '\n\n')
                
                print(f"  ✅ Successfully scraped {elements_found} elements")
                
        except requests.exceptions.RequestException as e:
            print(f"  ❌ Failed to fetch {url}: {e}")
        except Exception as e:
            print(f"  ❌ Error processing {url}: {e}")

print("\nScraping completed. Content saved to content.md")
