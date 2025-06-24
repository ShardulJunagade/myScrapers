import requests
from bs4 import BeautifulSoup
import time
import random

# base_urls=[
#             'https://www.tarunbharat.com/category/editions/महाराष्ट्र/page/',
#             'https://www.tarunbharat.com/category/editions/कर्नाटक/page/',
#             'https://tarunbharatlive.sortd.pro/category/editions/goa/page/',
#             'https://www.tarunbharat.com/category/horoscope/page/',
#             'https://tarunbharatlive.sortd.pro/category/national/page/',
#             'https://tarunbharatlive.sortd.pro/category/international/page/',
#             'https://tarunbharatlive.sortd.pro/category/sport/page/',
#             'https://tarunbharatlive.sortd.pro/category/agralekh/page/',
#             'https://tarunbharatlive.sortd.pro/category/व्यापार-उद्योगधंदे/page/',
#             'https://tarunbharatlive.sortd.pro/category/lifestyle/page/',
#             'https://tarunbharatlive.sortd.pro/category/टेक-गॅजेट/page/',
#             'https://tarunbharatlive.sortd.pro/category/फूड/page/',
#             'https://tarunbharatlive.sortd.pro/category/ऑटोमोबाईल/page/',
#             'https://tarunbharatlive.sortd.pro/category/vividha/page/',
#             'https://tarunbharatlive.sortd.pro/category/sanwad/page/',
#             'https://tarunbharatlive.sortd.pro/category/कृषी/page/',
#             'https://tarunbharatlive.sortd.pro/category/फॅशन/page/',
#             'https://tarunbharatlive.sortd.pro/category/विनोद/page/',
#             'https://tarunbharatlive.sortd.pro/category/अस्मिता/page/',
#             'https://tarunbharatlive.sortd.pro/category/नोकरी-करियर/page/',
#             'https://tarunbharatlive.sortd.pro/category/टुरिझम/page/',
#             'https://tarunbharatlive.sortd.pro/category/आरोग्य/page/'
#             ]

base_url='https://www.tarunbharat.com/category/editions/महाराष्ट्र/page/'

# section_names=['maharashtra', 'karnataka', 'goa', 'horoscope', 'national', 
#                'international', 'sports', 'agralekh', 'business', 'lifestyle', 
#                'tech', 'food', 'automobile', 'vividha', 'sanwad',
#                'krushi', 'fashion', 'vinod', 'asmita', 'career', 'tourism', 'aarogya']
section_name='maharashtra'
start_page = 1510
# end_pages=[5402, 3725, 1696, 146, 2676, 914, 1407, 555, 711, 300, 47, 37, 73, 31, 20, 12, 11, 5, 26, 5, 9, 55]
end_page=2000
# print(len(base_url_1), len(end_page_1))


failed_base_urls, failed_articles=[],[]   

def get_article_urls(base_url):
    global failed_base_urls
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    retries = 5
    for attempt in range(retries):
        try:
            response = requests.get(base_url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            soup = BeautifulSoup(response.text, 'html.parser')
            outer_div = soup.find('div', class_='main-content')
            inner_h2s=outer_div.find_all('h2', class_='post-title')
            # print(inner_h2s)
            urls = [h2.find('a', href=True)['href'] for h2 in inner_h2s]
            # print(len(urls))
            # print(urls)
            return urls
        except requests.exceptions.RequestException as e:
            if attempt==retries-1:
                print(f"Error fetching article URLs from {base_url}:", e)
                # print(base_url)
                failed_base_urls.append(base_url)
    return []

# get_article_urls_1('https://www.tarunbharat.com/category/editions/महाराष्ट्र/page/5402/')

def scrape_article(url):
    global failed_articles
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    retries=5
    for attempt in range(retries):  # Retry logic
        try:
            response = requests.get(url, headers=headers, allow_redirects=False)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            article_title_tag = soup.find('h1', class_='post-title')
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
            print(f"Error scraping article {url} (attempt {attempt + 1}):", e)
            # print(url)
            if attempt==retries-1:
                failed_articles.append(url)
            time.sleep(random.uniform(1, 3))
    return '', ''

# scrape_article('https://www.tarunbharat.com/porsche-car-accident-case-accuseds-grandfather-arrested/')



file_name = f'Shardul/Tarun Bharat/{section_name}_articles.txt'
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