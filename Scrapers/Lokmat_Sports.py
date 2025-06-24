import requests
from bs4 import BeautifulSoup
import re

base_url = 'https://www.lokmat.com/sports/page/'

def get_article_urls(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('a', class_='imgwrap')
    urls = [article['href'] for article in articles if 'href' in article.attrs]
    return urls

def scrape_article(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tag = soup.find('blockquote', class_='twitter-tweet')
    if tag:
        tag.decompose()
    content_div = soup.find('div', class_='article-contentText')  
    text = ''
    if content_div:
        for paragraph in content_div.find_all('p', recursive=False):
            text += paragraph.get_text().replace('\u00a0', '') + ' '
    text = re.sub(r'Web Title.*', '', text)
    return text

for i in range(1, 5002, 1000):
    start_page = i
    end_page = i + 999
    file_name = f'Shardul/Lokmat Sports/lokmat_sports_page_{start_page}_to_{end_page}.txt'
    if i == 5001:
        end_page = 6500
        file_name = f'Shardul/Lokmat Sports/lokmat_sports_page_{i}_to_end.txt'
    print(file_name)
    with open(file_name, 'a+', encoding='utf-8') as f:
        for page_num in range(start_page, end_page + 1):
            print(page_num)
            article_urls = get_article_urls(base_url + str(page_num))
            for url in article_urls:
                try:
                    if "https://www.lokmat.com" not in url:
                        url = "https://www.lokmat.com" + url
                    article_content = scrape_article(url)
                    if article_content:
                        f.write(article_content + '\n')
                except Exception as e:
                    print(f"An error occurred while processing the URL {url}: {e}")
                    pass

print('Scraping completed.')