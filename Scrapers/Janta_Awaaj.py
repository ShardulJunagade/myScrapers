import requests
from bs4 import BeautifulSoup
import time
import random

base_url='https://jantaawaj.in/page/'

failed_base_urls, failed_articles=[],[]

start_page = 1
end_page = 473
    

def get_article_urls(base_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
        # outer_div = soup.find('div', class_='main-content')
        # inner_h2s=outer_div.find_all('h2', class_='post-title')
        # # print(inner_h2s)
        # urls = [h2.find('a', href=True)['href'] for h2 in inner_h2s]
        a_tags=soup.find_all('a', href=True, class_='td-image-wrap')
        urls=[]
        # print(a_tags)
        for a_tag in a_tags:
            url=a_tag['href']
            if 'https://jantaawaj.in/' in url:
                urls.append(url)
        # print(len(urls))
        # print(urls)
        return urls
    except requests.exceptions.RequestException as e:
        print("Error fetching article URLs:", e)
        print(base_url)
        failed_base_urls.append(base_url)
        return []

# get_article_urls_1('https://www.tarunbharat.com/category/editions/महाराष्ट्र/page/5402/')


def extract_text_from_tags(tag):
    text = ''
    if isinstance(tag, str):
        return tag.strip()
    elif tag.name in ['div', 'p']:
        for child in tag.children:
            text += extract_text_from_tags(child)
        return text.strip()
    else:
        return ''
    


def scrape_article(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    for attempt in range(5):  # Retry logic
        try:
            response = requests.get(url, headers=headers, allow_redirects=False)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            article_title_tag = soup.find('h1', class_='tdb-title-text')
            article_title = article_title_tag.text.strip() if article_title_tag else "No Title"
            print(article_title)
            
            outer_div = soup.find('div', class_='td-post-content')
            content_div = outer_div.find('div', class_='tdb-block-inner')

            all_text = ''
            # print(content_div)
            # print(content_div.find_all(['div', 'p']))

            for div in content_div.find_all('div'):
                if not div.get_text(strip=True):
                    div.decompose()

            for tag in content_div.find_all(['div', 'p']):
                # print(tag)
                # print(extract_text_from_tags(tag))
                # print("-----------------------------------------")
                all_text += extract_text_from_tags(tag) + '\n'
            print(all_text)
            return article_title, all_text
        except requests.exceptions.RequestException as e:
            print(f"Error scraping article (attempt {attempt + 1}):", e)
            print(url)
            failed_articles.append(url)
            time.sleep(random.uniform(1, 3))
    return '', ''

# scrape_article('https://jantaawaj.in/5978/')


all_urls=[]

for page_num in range(start_page, end_page+1):
    print(page_num)
    page_urls= get_article_urls(base_url + str(page_num) + '/')
    all_urls+=page_urls


all_urls=list(set(all_urls))
num=len(all_urls)
print(num)


file_name = 'Shardul/Janta Awaaj News/janta_awaaj.txt'

with open(file_name, 'a+') as f:
    for i in range(len(all_urls)):
        url=all_urls[i]
        # print(url)
        article_title, article_content = scrape_article(url)
        if article_content:
            f.write(article_title+":\n")
            f.write(article_content + '\n\n')
            print(f'extracted URL {url}, {num-i-1} to go!')

print('Scraping completed.')

print(failed_base_urls)
print(failed_articles)