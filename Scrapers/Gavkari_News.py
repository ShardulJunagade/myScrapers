import requests
from bs4 import BeautifulSoup
import time
import random

base_urls=[
    'https://gavkarinews.com/category/maharashtra/page/',
    'https://gavkarinews.com/category/north-maharashtra/page/',
    'https://gavkarinews.com/category/sports/page/',
    'https://gavkarinews.com/category/nashik-city/page/',
    'https://gavkarinews.com/category/territorial/page/',
    'https://gavkarinews.com/category/national-international/page/',
    'https://gavkarinews.com/category/sampadakiya/page/',
    'https://gavkarinews.com/category/lifestyle/page/',
    'https://gavkarinews.com/category/lifestyle/health/page/',
    'https://gavkarinews.com/category/lifestyle/entertainment/page/',
    'https://gavkarinews.com/category/lifestyle/horoscope/page/'
]

start_page = 1
end_page=[170,144,1,18,2,4,10,25,4,3,14]
# print(len(base_url_1), len(end_page_1))


failed_base_urls, failed_articles=[],[]   

def get_article_urls(base_url):
    global failed_base_urls
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
        outer_div = soup.find('div', class_='content-area')
        inner_h2s=outer_div.find_all('h2', class_='entry-title')
        # print(inner_h2s)
        urls = [h2.find('a', href=True)['href'] for h2 in inner_h2s]
        # print(len(urls))
        # print(urls)
        return urls
    except requests.exceptions.RequestException as e:
        print("Error fetching article URLs:", e)
        print(base_url)
        failed_base_urls.append(base_url)
        return []

# get_article_urls('https://gavkarinews.com/category/maharashtra/')

def scrape_article(url):
    global failed_articles
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

            for span in soup.find_all('span'):
                span.decompose()


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
            print(f"Error scraping article (attempt {attempt + 1}):", e)
            print(url)
            failed_articles.append(url)
            time.sleep(random.uniform(1, 3))
    return '', ''

# scrape_article('https://gavkarinews.com/satvapariksha-of-the-parties-and-the-people/')


all_urls=[]

for i in range(len(base_urls)):
    # section_urls=[]
    base_url=base_urls[i]
    print(base_url) 
    for page_num in range(start_page, end_page[i]+1):
        print(page_num)
        page_urls= get_article_urls(base_url + str(page_num) + '/')
        all_urls+=page_urls
    #     section_urls+=page_urls
    # section_urls-=all_urls
    # all_urls+=section_urls


all_urls=list(set(all_urls))
num=len(all_urls)
print(num)


file_name = 'Shardul/Gavkari News/gavkari_news_all_sections.txt'

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