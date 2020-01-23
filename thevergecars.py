from bs4 import BeautifulSoup
import requests
from dateutil.parser import parse
import pandas as pd

articles_file = 'thevergecars_articles.csv'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}

source = requests.get('https://www.theverge.com/cars/archives/10', headers=headers).text

soup = BeautifulSoup(source, 'lxml')

articles = soup.find_all("div", "c-compact-river__entry")
# print(articles)

storiesdf = []

for article in articles:
    if article.find('h2') is None:
        continue
    article_title = article.find('h2').text
    article_title = article_title.encode('utf-8')
    article_title = article_title.decode("utf-8")

    article_body = article_title

    article_image_url = article.find('noscript').img
    article_image = article_image_url.get('src')

    article_date = article.find('time', class_="c-byline__item")
    article_date = article_date.get('datetime')
    article_date = parse(article_date)

    if article.find('span', 'c-byline__author-name') is None:
        article_byline = ""
    else:
        article_byline = article.find('span', 'c-byline__author-name').text

    article_link = article.find('h2').a
    article_link = article_link.get('href')

    weboutlet = "The Verge - cars"
    article_image_alt = "Image not found"

    storiesdf.append((article_date, article_title, article_body, article_link, article_image,
                      article_byline, article_image_alt, weboutlet))

    # print()
    #
    # print(article_date)
    # print(article_title)
    # print(article_body)
    # print(article_link)
    # print(article_image)
    # print(article_byline)
    # print(article_image_alt)
    # print(weboutlet)


df = pd.DataFrame(storiesdf, columns=['date', 'title', 'short_description', 'article_link', 'image',
                                      'byline', 'alt', 'outlet'])

df.to_csv(articles_file, index=False, encoding='utf-8')
