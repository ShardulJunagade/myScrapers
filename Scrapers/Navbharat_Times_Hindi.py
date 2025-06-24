import requests
from bs4 import BeautifulSoup


def scrape_article(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')


    article_title = soup.find('h1').text.strip()

    # Extract article content
    article_content = soup.find('div', class_='story-content').find_all('div', recursive=False)[0].text.strip()
    # print(article_title)
    # print(article_content)
    return article_title, article_content




# Base URL of the website
base_url = "https://navbharattimes.indiatimes.com/india/articlelist/1564454.cms"
params = {'curpg': 1}

# Set to store unique article URLs
article_urls = set()


while True:
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for any HTTP error
    except requests.RequestException as e:
        print("Error fetching page:", e)
        break

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all article links
    articles = soup.find_all('a', href=True)
    new_urls = {article['href'] for article in articles if '/articleshow/' in article['href']}

    # Remove already collected URLs to avoid duplicates
    new_urls -= article_urls

    # Log newly collected URLs
    # print("Collected {} new URLs on page {}".format(len(new_urls), params['curpg']))

    # Break if no new articles are found
    if not new_urls:
        break

    article_urls.update(new_urls)

    # Increment page number for the next request
    params['curpg'] += 1
    last_page_number = params['curpg'] 

# Output the total count of collected URLs
print("Total number of article URLs:", len(article_urls))
# print("Last page number:", last_page_number)

article_urls=list(article_urls)
# url_file="Shardul/Navbharat Times/India-URLs"
# with open(url_file, 'w') as f:
#     i=1
#     for url in article_urls:
#         # print(url)
#         print(i)
#         i+=1
#         f.write(url+'\n')

file_name="Shardul/Navbharat Times/navbharat_times_india_page_1_to_100.txt"
with open(file_name, 'a+', encoding='utf-8') as f:
        for _ in range(len(article_urls)):
            url=article_urls[_]
            print(_)
            try:
                article_title, article_content = scrape_article(url)
                if article_title and article_content:
                    f.write(article_title + ": ")
                    f.write(article_content + '\n')
            except Exception as e:
                print(f"An error occurred while processing the URL {url}: {e}")
                pass

print('Scraping completed.')