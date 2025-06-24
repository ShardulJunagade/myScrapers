import requests
from bs4 import BeautifulSoup
import time
import random

base_urls=[
    'https://www.mahasatta.com/page/',
    'https://www.mahasatta.com/archives/category/%ताज़ातरीन/page/',
    'https://www.mahasatta.com/archives/category/headline-news/page/',
    'https://www.mahasatta.com/archives/category/national-news/page/',
    'https://www.mahasatta.com/archives/category/maza-district/page/',
    'https://www.mahasatta.com/archives/category/maharashtra-news/page/',
    'https://www.mahasatta.com/archives/category/technology/page/'
]

failed_base_urls, failed_articles=[],[]

start_page = 1
end_page=[123,16,34,4,3,69,2]
# print(len(base_url_1), len(end_page_1))
    

def get_article_urls(base_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
        a_tags=soup.find_all('a', rel='bookmark')
        urls=[]
        # print(a_tags)
        for a_tag in a_tags:
            url=a_tag['href']
            if 'https://www.mahasatta.com/' in url:
                urls.append(url)
        # print(len(urls))
        # print(urls)
        return urls
    except requests.exceptions.RequestException as e:
        print("Error fetching article URLs:", e)
        print(base_url)
        failed_base_urls.append(base_url)
        return []

# get_article_urls('https://www.mahasatta.com/archives/category/maharashtra-news')

def scrape_article(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    for attempt in range(5):  # Retry logic
        try:
            response = requests.get(url, headers=headers, allow_redirects=False)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            article_title_tag = soup.find('h1', class_='post-title')
            article_title = article_title_tag.text.strip() if article_title_tag else "No Title"
            # print(article_title)
            
            content_div = soup.find('div', class_='post-cont-in')
            text = ''
            if content_div:
                paragraphs=content_div.find_all('p')
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
            failed_articles.append(url)
            time.sleep(random.uniform(1, 3))
    return '', ''

# scrape_article('https://www.mahasatta.com/archives/5950')


all_urls=[]

for i in range(len(base_urls)):
    base_url=base_urls[i]
    print(base_url) 
    for page_num in range(start_page, end_page[i]+1):
        print(page_num)
        page_urls= get_article_urls(base_url + str(page_num) + '/')
        all_urls+=page_urls


all_urls=list(set(all_urls))
num=len(all_urls)
print(num)



file_name = 'Shardul/Mahasatta/mahasatta_all_sections.txt'

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