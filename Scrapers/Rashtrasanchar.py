import requests
from bs4 import BeautifulSoup
import time
import random

base_urls=['https://rashtrasanchar.com/category/ताज्या-बातम्या/page/',
           'https://rashtrasanchar.com/category/देश-विदेश/page/',
           'https://rashtrasanchar.com/category/maharashtra/page/',
           'https://rashtrasanchar.com/category/सिटी-अपडेट्स/page/',
           'https://rashtrasanchar.com/category/रणधुमाळी/page/',
           'https://rashtrasanchar.com/category/विश्लेषण/page/',
           'https://rashtrasanchar.com/category/फिचर/page/',
           'https://rashtrasanchar.com/category/संपादकीय/page/',
           'https://rashtrasanchar.com/category/संडे-फिचर-2/page/',
           'https://rashtrasanchar.com/category/इतर/page/']

base_url='https://rashtrasanchar.com/category/ताज्या-बातम्या/page/'

start_page = 270
# end_pages=[761, 240, 371, 242, 409, 11, 22, 121, 14, 232]
end_page=761
# print(len(base_urls), len(end_page))
section_name='latest_news'
file_name= f'Shardul/Rashtrasanchar/{section_name}_articles.txt'

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
            outer_div = soup.find('div', class_='main-content')
            a_tags = outer_div.find_all('a', href=True, class_='more-link button')
            # print(a_tags)
            urls=[a_tag['href'] for a_tag in a_tags]
            print(len(urls))
            # print(urls)
            return urls
        except requests.exceptions.RequestException as e:
            print(f"Error fetching article URLs from {base_url}:", e)
            # print(base_url)
            if attempt == retries - 1:
                failed_base_urls.append(base_url)
            time.sleep(2 ** attempt + random.uniform(0, 1))
    return []

# get_article_urls('https://rashtrasanchar.com/category/%e0%a4%a4%e0%a4%be%e0%a4%9c%e0%a5%8d%e0%a4%af%e0%a4%be-%e0%a4%ac%e0%a4%be%e0%a4%a4%e0%a4%ae%e0%a5%8d%e0%a4%af%e0%a4%be/page/2/')

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
            for p in content_div.find_all('p'):
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

# scrape_article('https://rashtrasanchar.com/today-rahul-gandhis-sabha-in-pune-congress-leaders-will-be-present-57452/')

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
