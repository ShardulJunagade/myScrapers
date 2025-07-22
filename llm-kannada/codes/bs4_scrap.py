import requests
from bs4 import BeautifulSoup
import time
import random

# Karnataka news base URL
base_url = 'https://www.vijayavani.net/category/%e0%b2%b8%e0%b2%ae%e0%b2%b8%e0%b3%8d%e0%b2%a4-%e0%b2%95%e0%b2%b0%e0%b3%8d%e0%b2%a8%e0%b2%be%e0%b2%9f%e0%b2%95/'
start_page = 1
end_page = 4565

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_article_urls(page_url, retries = 3):
    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(page_url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            div1 = soup.find('div', class_='blog-content')
            if not div1:
                print(f"Unable to find blog grid on page: {page_url}")
                return []

            titles = div1.find_all('h2', class_='entry-title')
            if not titles:
                print(f"Unable to find article titles on page: {page_url}")
                return []

            article_urls = [title.find('a')['href'] for title in titles if title.find('a')]
            return article_urls
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {page_url} (Attempt {attempt+1}): {e}")
            attempt += 1
            if attempt < retries:
                time.sleep(random.randint(3, 7))
            else:
                print(f"Failed after {retries} attempts: {page_url}")
                return []

links = []
for i in range(start_page, end_page+1):
    print(f"Processing page: {i}")
    page_url = base_url + 'page/' + str(i)
    article_urls = get_article_urls(page_url)
    
    if article_urls:
        links.extend(article_urls)
    
    time.sleep(random.randint(2, 5))

print("Total links collected:", len(links))
