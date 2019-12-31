from bs4 import BeautifulSoup
# from urllib.request import urlopen
import requests
from dateutil.parser import parse
import pandas as pd
from datetime import date, timedelta

articles_file = '/home/john/PycharmProjects/EVNews/greencarguide_articles.csv'

source = requests.get('https://www.greencarguide.co.uk/green-car-news/page/5/').text

soup = BeautifulSoup(source, 'lxml')

articles = soup.find_all("card", "news")
# print(articles)

storiesdf = []

for article in articles:
    if article.find("span", "title") is None:
        continue
    article_title = article.find("span", "title").text
    article_title = article_title.encode('utf-8')
    article_title = article_title.decode("utf-8")

    article_body = article.find('span', "description").p.text
#
    article_image_url = article.find('img')
    article_image = article_image_url.get('data-lazy-srcset')
    *_, article_image = article_image.split(',')
    article_image = article_image.strip()
    article_image, *_ = article_image.split(" ")

    article_date = article.find('span', "post-date").text
#     article_date, article_byline = article_date.split('|')
#     article_date = article_date.strip()
    article_date = parse(article_date)
    article_byline = ""
#
    article_link = article.find('a')
#     _, article_link, *args = article_link
    article_link = article_link.get('href')
    weboutlet = "greencarguide"
    article_image_alt = article.find('img')
    article_image_alt = article_image_alt.get("alt")

    storiesdf.append((article_date, article_title, article_body, article_link, article_image,
                      article_byline, article_image_alt, weboutlet))
#     print(articles)
#     print()
#
#     print(article_date)
#     print(article_title)
#     print(article_body)
#     print(article_link)
#     print(article_image)
#     print(article_byline)
#     print(article_image_alt)
#     print(weboutlet)
    #




df = pd.DataFrame(storiesdf, columns=['date', 'title', 'short_description', 'article_link', 'image',
                                      'byline', 'alt', 'outlet'])
# df['date'] = pd.to_datetime(df['date'])

df.to_csv(articles_file, index=False, encoding='utf-8')
