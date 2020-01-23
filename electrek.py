# from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import pandas as pd
# import subprocess
# import sys

articles_file = "/home/john/PycharmProjects/EVNews/electrek_articles.csv"

html = requests.get("https://electrek.co/page/52/").text
soup = BeautifulSoup(html, "lxml")

articles = soup.find_all("article", "post-content")

storiesdf = []

for article in articles:
    if article.find('h1', 'post-title') is None:
        continue
    article_title = article.find('h1', 'post-title').text

    article_title = article_title.encode('utf-8')
    article_title = article_title.decode("utf-8")

    article_link_tag = article.find('h1', 'post-title')
    article_link_step = article_link_tag.find('a', href=True)
    article_link = article_link_step.get('href')

    article_datetime = article.find('p', 'time-twitter').text.strip()
    article_datetime = article_datetime.replace('- ', '')
    article_datetime = article_datetime.replace(' ET', '')
    article_body = article.find('div', "post-body").text.strip()
    article_body = article_body.replace('expand full story', '', -1)
    article_body = article_body.replace('\n', '', -1)
    article_body = article_body.encode('utf-8')
    article_body = article_body.decode("utf-8")

    article_image_url_step = article.find('img')
    article_image_url_step, d = str(article_image_url_step).split('?', 1)
    article_image_url = article_image_url_step.replace('<img src="', '')

    article_byline = article.find('span', itemprop='name').text
    article_byline = str(article_byline)

    article_image_alt = "Image not found"

    weboutlet = 'Electrek'

    storiesdf.append((article_datetime, article_title, article_body, article_link, article_image_url,
                      article_byline, article_image_alt, weboutlet))

df = pd.DataFrame(storiesdf, columns=['date', 'title', 'short_description', 'article_link', 'image',
                                      'byline', 'alt', 'outlet'])
df['date'] = pd.to_datetime(df['date'])
df.to_csv(articles_file, index=False, encoding='utf-8')

# subprocess.call([sys.executable, 'ev_news_electrek.py'])
