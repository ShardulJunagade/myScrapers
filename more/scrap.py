import requests
from bs4 import BeautifulSoup
import time
import random

# base_urls=[
#     'https://www.navakal.in/category/news/page/',
#     'https://www.navakal.in/category/maharashtra/page/',
#     'https://www.navakal.in/category/desh-videsh/page/',
#     'https://www.navakal.in/category/krida/page/',
#     'https://www.navakal.in/category/rajkiya/page/',
#     'https://www.navakal.in/category/jayashri-khadilkar-pande/page/',
#     'https://www.navakal.in/category/other-sampadakiya/page/',
#     'https://www.navakal.in/category/lekh/page/',
#     'https://www.navakal.in/category/economics/page/',
#     'https://www.navakal.in/category/आरोग्य/page/',
#     'https://www.navakal.in/category/manoranjan/page/'
# ]

base_url='https://www.navakal.in/category/manoranjan/page/'

start_page = 1
# end_pages=[197,109,91,1,26,1,1,1,7,1,1]
end_page=1
# print(len(base_urls), len(end_page))
section_name='other'

failed_base_urls, failed_articles=[],[]

def get_article_urls(base_url):
    global failed_base_urls
    headers = {
        'User-Agent': random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0'
        ])
    }
    retries = 5
    for attempt in range(retries):
        try:
            response = requests.get(base_url, headers=headers, timeout=10)
            response.raise_for_status()  # Raise an exception for HTTP errors
            soup = BeautifulSoup(response.text, 'html.parser')
            outer_div = soup.find('main', class_='site-main')
            inner_h2s=outer_div.find_all('h2', class_='entry-title')
            # print(inner_h2s)
            urls = [h2.find('a', href=True)['href'] for h2 in inner_h2s]
            # print(len(urls))
            # print(urls)
            return urls
        except requests.exceptions.RequestException as e:
            print(f"Error fetching article URLs from {base_url}:", e)
            # print(base_url)
            if attempt == retries - 1:
                failed_base_urls.append(base_url)
            time.sleep(2 ** attempt + random.uniform(0, 1))
    return []

# get_article_urls('https://www.navakal.in/category/maharashtra/page/1/')

def scrape_article(url):
    global failed_articles
    headers = {
        'User-Agent': random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0'
        ])
    }
    retries=5
    for attempt in range(retries):  # Retry logic
        try:
            response = requests.get(url, headers=headers, allow_redirects=False, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            article_title_tag = soup.find('h1', class_='entry-title')
            article_title = article_title_tag.text.strip() if article_title_tag else "No Title"
            # print(article_title)
            
            content_div = soup.find('div', class_='entry-content')

            # # Remove <script> tags
            # for script in soup.find_all('script'):
            #     script.decompose()

            # # Remove specific <div> tags
            # for div in soup.find_all('div', class_=['g g-2', 'g g-3', 'g g-1', 'g g-4']):
            #     div.decompose()

            # for br in soup.find_all('br'):
            #     br.decompose()

            # for figure in soup.find_all('figure'):
            #     figure.decompose()

            # for span in soup.find_all('span'):
            #     span.decompose()


            # Remove empty <p> tags
            for p in soup.find_all('p'):
                if not p.get_text(strip=True):
                    p.decompose()

            text = ''
            if content_div:
                paragraphs=content_div.find_all('p', recursive=False)
                # print(paragraphs)
                # print("-----------------------------------------------------")
                for paragraph in paragraphs:
                    # print(paragraph.text)
                    text+=(paragraph.text.strip()+"\n")
            #     print("-----------------------------------------------------")
            # print(text)
            return article_title, text
        except requests.exceptions.RequestException as e:
            print(f"Error scraping article {url} (attempt {attempt + 1}):", e)
            # print(url)
            if attempt == retries - 1:
                failed_articles.append(url)
            time.sleep(2 ** attempt + random.uniform(1, 3))
    return '', ''

# scrape_article('https://www.navakal.in/economics/%e0%a4%ae%e0%a5%8d%e0%a4%af%e0%a5%81%e0%a4%9a%e0%a5%8d%e0%a4%af%e0%a5%81%e0%a4%85%e0%a4%b2-%e0%a4%ab%e0%a4%82%e0%a4%a1%e0%a4%be%e0%a4%82%e0%a4%b5%e0%a4%b0-%e0%a4%97%e0%a5%81%e0%a4%82%e0%a4%a4%e0%a4%b5/')

file_name= f'Nava Kaal/{section_name}_articles.txt'
with open(file_name, 'a+', encoding='utf-8') as f:
    for i in range(start_page,end_page+1):
        print(f'Scraping page {i}...')
        article_urls = get_article_urls(base_url + str(i)+'/')
        for url in article_urls:
            print(f'Scraping article: {url}')
            article_title, article_content = scrape_article(url)
            if article_content!="":
                f.write(article_title + ':\n')
                f.write(article_content + '\n\n')
            else:
                print(f"No article content for {url}")


print('Scraping completed.')
print("Failed Base URLs:", failed_base_urls)
print("Failed Articles:", failed_articles)
