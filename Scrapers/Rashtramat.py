import requests
from bs4 import BeautifulSoup
import time
import random

base_url_1= ['https://rashtramat.com/category/tie-goa/page/',
             'https://rashtramat.com/category/tie-world/page/',
             'https://rashtramat.com/category/tie-maharashtra/page/',
             'https://rashtramat.com/category/tie-sports/page/',
             'https://rashtramat.com/category/tie-articles/page/']

base_url_2 = ['https://rashtramat.com/category/tie-business/page/',
              'https://rashtramat.com/category/tie-entertainment/page/']

start_page = 1
end_page_1=[74,52,73,8,6]
end_page_2=[22,28]

def get_article_urls_1(base_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
        outer_div = soup.find('div', class_='main-content')
        a_tags = outer_div.find_all('a', href=True, class_='more-link button')
        # print(a_tags)
        urls=[a_tag['href'] for a_tag in a_tags]
        # print(len(urls))
        # print(urls)
        return urls
    except requests.exceptions.RequestException as e:
        print("Error fetching article URLs:", e)
        print(base_url)
        return []
    

def get_article_urls_2(base_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
        outer_div = soup.find('div', class_='main-content')
        if 'https://rashtramat.com/category/tie-business/' in base_url:
            inner_h2s=outer_div.find_all('h2', class_='thumb-title')
        if 'https://rashtramat.com/category/tie-entertainment/' in base_url:
            inner_h2s=outer_div.find_all('h2', class_='post-title')
        # print(inner_h2s)
        urls = [h2.find('a', href=True)['href'] for h2 in inner_h2s]
        # print(len(urls))
        # print(urls)
        return urls
    except requests.exceptions.RequestException as e:
        print("Error fetching article URLs:", e)
        print(base_url)
        return []


def scrape_article(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    for attempt in range(5):  # Retry logic
        try:
            response = requests.get(url, headers=headers, allow_redirects=False)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            article_title_tag = soup.find('h1', class_='entry-title')
            article_title = article_title_tag.text.strip() if article_title_tag else "No Title"
            # print(article_title)
            
            content_div = soup.find('div', class_='entry-content')
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
            print(f"Error scraping article (attempt {attempt + 1}):", e)
            print(url)
            time.sleep(random.uniform(1, 3))
    return '', ''

# scrape_article('https://rashtramat.com/indoco-encube-had-notified-vacancies-on-the-employment-exchange-portal/')


all_urls=[]

for i in range(len(base_url_1)):
    base_url=base_url_1[i]
    print(base_url)
    for page_num in range(start_page, end_page_1[i]+1):
        print(page_num)
        page_urls= get_article_urls_1(base_url + str(page_num) + '/')
        all_urls+=page_urls

for i in range(len(base_url_2)):
    base_url=base_url_2[i]
    print(base_url)
    for page_num in range(start_page, end_page_2[i]+1):
        print(page_num)
        page_urls= get_article_urls_2(base_url + str(page_num) + '/')
        all_urls+=page_urls

all_urls=list(set(all_urls))
print(len(all_urls))



file_name = 'Shardul/Rashtramat/rashtramat_all_sections.txt'

with open(file_name, 'a+') as f:
    for url in all_urls:
        print(url)
        article_title, article_content = scrape_article(url)
        if article_content:
            f.write(article_title+":\n")
            f.write(article_content + '\n\n')

print('Scraping completed.')