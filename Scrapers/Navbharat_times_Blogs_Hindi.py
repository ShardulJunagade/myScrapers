import requests
from bs4 import BeautifulSoup
import re

base_url = 'https://blogs.navbharattimes.indiatimes.com/page/'

def get_article_urls(base_url):
  response = requests.get(base_url)
  soup = BeautifulSoup(response.text, 'html.parser')
  content_div = soup.find_all('div', class_='content')
  urls = [div.find('a')['href'] for div in content_div]
  return urls


def scrape_article(url):
  response = requests.get(url, allow_redirects=False)
  soup = BeautifulSoup(response.text, 'html.parser')
  content_div = soup.find('div', class_='content')  
  text = ''
  if content_div:
    for paragraph in content_div.find_all('p', recursive=False):
      text += paragraph.get_text().replace('\u00a0', '') + ' '
  return text

start_page=1
end_page=1000
file_name = f'Shardul/Navbharat Times Blogs/navbharat_times_blogs_page_{start_page}_to_{end_page}.txt'
print(file_name)
with open(file_name, 'a+', encoding='utf-8') as f:
  for _ in range(start_page, end_page+1):
    print(_)
    article_urls = get_article_urls(base_url+str(_))
    for url in article_urls:
      article_content = scrape_article(url)
      if article_content!="":
        f.write(article_content + '\n')

print('Scraping completed.')
