from bs4 import BeautifulSoup
# from urllib.request import urlopen
import requests
from dateutil.parser import parse
import pandas as pd
from datetime import date, timedelta

articles_file = '/home/john/PycharmProjects/EVNews/electrive_articles.csv'

source = requests.get('https://www.electrive.com/category/automobile/page/3/').text

soup = BeautifulSoup(source, 'lxml')

articles = soup.find_all("article", "teaser row")
# print(article)

storiesdf = []

for article in articles:
    if article.find('h3') is None:
        continue
    article_title = article.find('h3').text
    article_title = article_title.encode('utf-8')
    article_title = article_title.decode("utf-8")

    article_body = article.find('p').text

    article_image_url = article.find('img')
    article_image = article_image_url.get('srcset')

    *_, article_image = article_image.split(',')
    article_image = article_image.strip()
    article_image, _ = article_image.split(' ')

    article_date = article.find('span', class_="meta").text
    article_date = parse(article_date)

    article_byline = ""

    article_link = article.find('a')
#     _, article_link, *args = article_link
    article_link = article_link.get('href')
    weboutlet = "electrive"
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
