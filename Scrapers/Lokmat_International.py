import requests
from bs4 import BeautifulSoup
import re

base_url = 'https://www.lokmat.com/international/page/'


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

# page = 1
with open('Shardul/International/lokmat_international_article.txt', 'a+') as f:
  for _ in range(1, 2700):
    print("Page: " + str(_))
    article_urls = get_article_urls(base_url+str(_))
    for url in article_urls:
      # print(f'Scraping article: {url}')
      if "https://www.lokmat.com" in url:
        article_content = scrape_article(url)
      else:
        article_content = scrape_article("https://www.lokmat.com" + url)
      # print(article_content)
      if article_content!="":
        f.write(article_content + '\n\n')
    # page += 1

print('Scraping completed.')