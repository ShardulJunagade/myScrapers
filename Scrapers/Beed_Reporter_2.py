import requests
from bs4 import BeautifulSoup

base_url = 'https://beedreporter.com/news/category/beed/page/'

def get_article_urls(base_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
        outer_div = soup.find('div', class_='jeg_inner_content')
        inner_div = outer_div.find_all('div', class_='jeg_thumb')
        articles = [k.find('a', href=True) for k in inner_div]
        urls = [article['href'] for article in articles]
        # print(len(urls))
        # print(urls)
        return urls
    except requests.exceptions.RequestException as e:
        print("Error fetching article URLs:", e)
        return []
    
# get_article_urls('https://beedreporter.com/news/category/gevrai/page/1')


def scrape_article(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, allow_redirects=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        article_title_tag = soup.find('h1', class_='jeg_post_title')
        article_title = article_title_tag.text.strip() if article_title_tag else "No Title"
        content_div = soup.find('div', class_='content-inner')

        # Remove <script> tags
        for script in soup.find_all('script'):
            script.decompose()

        # Remove specific <div> tags
        for div in soup.find_all('div', class_=['g g-2', 'g g-3', 'g g-1', 'g g-4']):
            div.decompose()

        for br in soup.find_all('br'):
            br.decompose()
            
        for figure in soup.find_all('figure'):
            figure.decompose()

        text = ''
        if content_div:
            paragraphs=content_div.find_all('p', recursive=False)
            # print(paragraphs)
            for paragraph in paragraphs:
                # print(paragraph.text)
                text+=paragraph.text.strip()
                # text += paragraph.get_text().replace('\u00a0', '') + ' '
            # print(text)
        # print(article_title)
        # print(text)
        return article_title, text
    except requests.exceptions.RequestException as e:
        print("Error scraping article:", e)
        return '', ''

# scrape_article('https://beedreporter.com/news/225/')

start_page = 1
end_page = 363
file_name = f'Shardul/Beed Reporter/beed_page_{start_page}_to_{end_page}.txt'

with open(file_name, 'a+') as f:
    for _ in range(start_page, end_page + 1):
        print(_)
        article_urls = get_article_urls(base_url + str(_))
        for url in article_urls:
            article_title, article_content = scrape_article(url)
            if article_content:
                f.write(article_title+":\n")
                f.write(article_content + '\n\n')

print('Scraping completed.')
