import requests
from bs4 import BeautifulSoup
import time
import random

# base_urls=[
#     'https://www.manogat.com/activity?page=',
#     'https://www.manogat.com/prose?page=',
#     'https://www.manogat.com/poetry?page=',
#     'https://www.manogat.com/cooking?page=',
#     'https://www.manogat.com/programs?page=',
#     'https://www.manogat.com/discuss?page='
# ]
base_url='https://www.manogat.com/discuss?page='

start_page = 1
# end_pages=[745,246,358,38,9,75]
end_page=75
# print(len(base_urls), len(end_page))
section_name='rest'

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
            table =soup.find('tbody')
            a_tags=table.find_all('a', href=True)
            urls=[]
            for a_tag in a_tags:
                url= "https://www.manogat.com" + a_tag['href']
                urls.append(url)
            # print(len(urls))
            # print(urls)
            return urls
        except requests.exceptions.RequestException as e:
            # print(base_url)
            if attempt == retries - 1:
                print(f"Error fetching article URLs from {base_url}:", e)
                failed_base_urls.append(base_url)
            time.sleep(2 ** attempt + random.uniform(0, 1))
    return []

# get_article_urls('https://www.manogat.com/activity?page=1')

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
            article_title_tag = soup.find('h1', class_='page-title')
            article_title = article_title_tag.text.strip() if article_title_tag else "No Title"
            # print(article_title)
            
            outer_div = soup.find('div', class_='node__content')
            if not outer_div:
                raise ValueError("No content found in the HTML")
            # inner_div=outer_div.select('.w3-row.field.field--name-body.field--type-text-with-summary.field--label-hidden.w3-bar-item.field__item')
            # print(inner_div)
            # print(inner_div.get_text().strip())

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
            for p in outer_div.find_all('p'):
                if not p.get_text(strip=True):
                    p.decompose()

            text = ''
            if outer_div:
                paragraphs=outer_div.find_all('p', recursive=True)
                # print(paragraphs)
                # print("-----------------------------------------------------")
                for paragraph in paragraphs:
                    # print(paragraph.text)
                    text+=(paragraph.text.strip()+"\n")
            #     print("-----------------------------------------------------")
                divs=outer_div.find_all('div', recursive=True)
                for div in divs:
                    text+=(div.text.strip()+'\n')
            # print(text)
            return article_title, text
        except requests.exceptions.RequestException as e:
            print(f"Error scraping article {url} (attempt {attempt + 1}):", e)
            # print(url)
            if attempt == retries - 1:
                failed_articles.append(url)
            time.sleep(2 ** attempt + random.uniform(1, 3))
    return '', ''

# scrape_article('https://www.manogat.com/node/26862')


file_name = f'Shardul/Manogat/{section_name}_data.txt'
# file_name = f'Manogat/{section_name}_data.txt'
with open(file_name, 'a+', encoding='utf-8') as f:
    for i in range(start_page,end_page+1):
        print(f'Scraping page {i}...')
        article_urls = get_article_urls(base_url + str(i))
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