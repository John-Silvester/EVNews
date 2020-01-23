from bs4 import BeautifulSoup
import requests
from dateutil.parser import parse
import pandas as pd

articles_file = 'evobsession_articles.csv'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}

source = requests.get('https://evobsession.com/category/electric-vehicles/100-electric-vehicles/page/2/',
                      headers=headers).text

soup = BeautifulSoup(source, 'lxml')

articles = soup.find_all("article", "item")
# print(articles)

storiesdf = []

for article in articles:
    if article.find('h2', "grid-title") is None:
        continue
    article_title = article.find('h2', "grid-title").text
    article_title = article_title.encode('utf-8')
    article_title = article_title.decode("utf-8")

    article_body = article_title

    article_image_url = article.find('a', 'penci-image-holder')
    article_image = article_image_url.get('data-src')
    article_image, *args = article_image.split('?', 1)

    article_date = article.find('div', 'grid-post-box-meta').text
    article_date = article_date.strip()
    article_byline, article_date = article_date.split('\n')
    article_date = parse(article_date)

    article_link = article.find('a', 'penci-image-holder')
    article_link = article_link.get('href')
    weboutlet = "EV Obsession"
    article_image_alt = "Image not found"

    storiesdf.append((article_date, article_title, article_body, article_link, article_image,
                      article_byline, article_image_alt, weboutlet))

    print()

    print(article_date)
    print(article_title)
    print(article_body)
    print(article_link)
    print(article_image)
    print(article_byline)
    print(article_image_alt)
    print(weboutlet)

df = pd.DataFrame(storiesdf, columns=['date', 'title', 'short_description', 'article_link', 'image',
                                      'byline', 'alt', 'outlet'])
# df['date'] = pd.to_datetime(df['date'])

df.to_csv(articles_file, index=False, encoding='utf-8')
