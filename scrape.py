import requests
from bs4 import BeautifulSoup

# Send a GET request to the website
for i in range(21):
    url = f'https://meroadalat.com/page/{i}/'
    response = requests.get(url)

# Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the 'Read More' buttons and extract the links
    buttons = soup.find_all('a', class_='read-more button')

    # Print the links
    for button in buttons:
        link = button.get('href')
        print(link)
        with open('links.txt', 'a') as f:
            f.write(link + '\n')    
