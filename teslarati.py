from bs4 import BeautifulSoup
# from urllib.request import urlopen
import requests
import pandas as pd
from datetime import date, timedelta

articles_file = '/home/john/PycharmProjects/EVNews/teslarati_articles.csv'

source = requests.get('https://www.teslarati.com/category/news/page/20/').text

soup = BeautifulSoup(source, 'lxml')

articles = soup.find_all('li', class_='infinite-post')
# print(articles)
storiesdf = []

for article in articles:
    if article.find('h2') is None:
        continue
    article_title = article.find('h2').text
    article_title = article_title.encode('utf-8')
    article_title = article_title.decode("utf-8")

    article_body = article.find('p').text

    article_image_url = article.find('div', class_="archive-list-out").div.img
    article_image = article_image_url.get('src')

    article_link = article.find('a')
    article_link = article_link.get('href')

    weboutlet = "Teslarati"
    article_image_alt = "Image not found"

    article_date = date.today() - timedelta(62)
    article_byline = ""

    storiesdf.append((article_date, article_title, article_body, article_link, article_image,
                      article_byline, article_image_alt, weboutlet))
    #
    # print(article_date)
    # print(article_byline)
    #
    # print(article_title)
    # print(article_body)
    # print(article_link)
    # print(article_image_url)
    # print(article_image_alt)
    # print(weboutlet)

df = pd.DataFrame(storiesdf, columns=['date', 'title', 'short_description', 'article_link', 'image',
                                      'byline', 'alt', 'outlet'])
# df['date'] = pd.to_datetime(df['date'])

df.to_csv(articles_file, index=False, encoding='utf-8')
