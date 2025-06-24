import requests
from bs4 import BeautifulSoup
import time

base_url = 'https://www.lokmat.com'
sections = [
    'https://www.lokmat.com/latestnews/',
    'https://www.lokmat.com/maharashtra/',
    'https://www.lokmat.com/city/',
    'https://www.lokmat.com/national/',
    'https://www.lokmat.com/international/',
    'https://www.lokmat.com/sports/',
    'https://www.lokmat.com/cricket/',
    'https://www.lokmat.com/entertainment/',
    'https://www.lokmat.com/editorial/',
    'https://www.lokmat.com/crime/',
    'https://www.lokmat.com/business/',
    'https://www.lokmat.com/bhakti/',
    'https://www.lokmat.com/agriculture/'
]

def fetch_page(url, params=None):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        time.sleep(1)  # Throttle requests
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_articles(content):
    soup = BeautifulSoup(content, 'html.parser')
    articles = []
    for article in soup.find_all('div', class_='listing'):
        title = article.find('h2').text.strip()
        link = base_url + article.find('a')['href']
        date = article.find('span', class_='posted-on').text.strip()
        articles.append({
            'title': title,
            'link': link,
            'date': date
        })
    return articles

def get_articles_from_section(section_url, max_articles=1000):
    all_articles = []
    offset = 0
    while len(all_articles) < max_articles:
        params = {'offset': offset}
        content = fetch_page(section_url, params=params)
        if content:
            new_articles = parse_articles(content)
            if not new_articles:
                break
            all_articles.extend(new_articles)
            offset += len(new_articles)
        else:
            break
    return all_articles

all_articles = []
for section in sections:
    print(f"Scraping section: {section}")
    articles = get_articles_from_section(section, max_articles=100)
    all_articles.extend(articles)

with open('lokmat_articles.txt', 'w', encoding='utf-8') as file:
    for article in all_articles:
        file.write(f"Title: {article['title']}\n")
        file.write(f"Link: {article['link']}\n")
        file.write(f"Date: {article['date']}\n")
        file.write("\n")  # Add a newline for separation between articles

print("Scraping completed and data saved to lokmat_articles.txt")
