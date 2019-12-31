from bs4 import BeautifulSoup
# from urllib.request import urlopen
import requests
from dateutil.parser import parse
import pandas as pd
# from datetime import date, timedelta

articles_file = '/home/john/PycharmProjects/EVNews/greencarreports_articles.csv'

source = requests.get('https://www.greencarreports.com/news/page-2').text

soup = BeautifulSoup(source, 'lxml')

articles = soup.find_all("li")
# print(article)

storiesdf = []

for article in articles:
    if article.find('a', 'title') is None:
        continue
    article_title = article.find('a', 'title').text
    article_title = article_title.encode('utf-8')
    article_title = article_title.decode("utf-8")

    article_body = article.find('p').text

    article_image_url = article.find('img')
    article_image = article_image_url.get('data-src')

    article_date = article.find('time').text
    article_date = parse(article_date)

    article_byline = article.find('a', 'by-line').text

    article_link = article.find('a', 'title')
    article_link = article_link.get('href')
    article_link = "https://www.greencarreports.com" + article_link

    weboutlet = "Green Car Reports"
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
