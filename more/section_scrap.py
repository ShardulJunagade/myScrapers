import requests
from bs4 import BeautifulSoup
import time
import random

base_urls=[
    'https://www.manogat.com/activity?page=',
    'https://www.manogat.com/prose?page=',
    'https://www.manogat.com/poetry?page=',
    'https://www.manogat.com/cooking?page=',
    'https://www.manogat.com/programs?page=',
    'https://www.manogat.com/discuss?page='
]
# base_urls=[
#     'https://www.manogat.com/activity?page='
# ]

start_page = 0
end_pages=[745,246,358,38,9,75]
# end_pages=[0]
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
            print("Error fetching article URLs:", e)
            # print(base_url)
            if attempt == retries - 1:
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
            # print(text)
            return article_title, text
        except requests.exceptions.RequestException as e:
            print(f"Error scraping article (attempt {attempt + 1}):", e)
            # print(url)
            if attempt == retries - 1:
                failed_articles.append(url)
            time.sleep(2 ** attempt + random.uniform(1, 3))
    return '', ''

# scrape_article('https://www.manogat.com/node/26885')


def scrape_section(base_url, end_page, section_name):
    all_urls = []
    for page_num in range(0, end_page + 1):
        print(f"Scraping page {page_num} of section {section_name}")
        page_urls = get_article_urls(base_url + str(page_num))
        all_urls += page_urls

    num = len(all_urls)
    print(f"Total URLs found in section {section_name}: {num}")

    file_name = f'Shardul/Manogat/{section_name}data.txt'

    with open(file_name, 'a+') as f:
        for i, url in enumerate(all_urls):
            article_title, article_content = scrape_article(url)
            if article_content:
                f.write(article_title + ":\n")
                f.write(article_content + '\n\n')
                print(f'extracted URL {url}, {num - i - 1} to go!')


def main():
    for i in range(len(base_urls)):
        base_url = base_urls[i]
        end_page = end_pages[i]
        section_name = base_url.split('/')[3][:-6]  # Adjust according to URL structure
        # print(section_name)
        scrape_section(base_url, end_page, section_name)

    print('Scraping completed.')
    print("Failed Base URLs:", failed_base_urls)
    print("Failed Articles:", failed_articles)

if __name__ == "__main__":
    main()