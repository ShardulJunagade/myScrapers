import requests
from bs4 import BeautifulSoup
import time
import random

base_urls=[
    'https://inmarathi.com/categories/infotainment/',
    'https://inmarathi.com/categories/health/',
    'https://inmarathi.com/categories/inspirational/',
    'https://inmarathi.com/categories/history/',
    'https://inmarathi.com/categories/travel/',
    'https://inmarathi.com/categories/politics/',
    'https://inmarathi.com/categories/blog/'
]

start_page = 1
end_pages=[197,109,91,1,26,1,1,1,7,1,1]
# print(len(base_urls), len(end_page))

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
            a_tags = soup.find_all('a', href=True, class_="more-link")
            urls=[a_tag['href'] for a_tag in a_tags]
            # print(len(urls))
            # print(urls)
            return urls
        except requests.exceptions.RequestException as e:
            print("Error fetching article URLs:", e)
            # print(base_url)
            if attempt == retries - 1:
                failed_base_urls.append(base_url)
            time.sleep(2 ** attempt + random.uniform(0, 1))
    return []

# get_article_urls('https://inmarathi.com/categories/politics/')

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

            # Remove empty <p> tags
            for p in soup.find_all('p'):
                if not p.get_text(strip=True):
                    p.decompose()

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
            # print(url)
            if attempt == retries - 1:
                failed_articles.append(url)
            time.sleep(2 ** attempt + random.uniform(1, 3))
    return '', ''

# scrape_article('https://inmarathi.com/13034/weird-incident-fish-rain-in-the-world/')


def main():
    for i in range(len(base_urls)):
        base_url = base_urls[i]
        section_name = base_url.split('/')[4]  # Adjust according to URL structure
        # print(section_name)
        urls=get_article_urls(base_url)
        num=len(urls)
        print(f"Total URLs found in section {section_name}: {num}")

        file_name = f'Shardul/in marathi/{section_name}_articles.txt'

        with open(file_name, 'a+') as f:
            for i, url in enumerate(urls):
                article_title, article_content = scrape_article(url)
                if article_content:
                    f.write(article_title + ":\n")
                    f.write(article_content + '\n\n')
                    print(f'extracted URL {url}, {num - i - 1} to go!')

    print('Scraping completed.')
    print("Failed Base URLs:", failed_base_urls)
    print("Failed Articles:", failed_articles)

if __name__ == "__main__":
    main()