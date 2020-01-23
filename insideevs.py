
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import datetime
# import time
# import subprocess
# import sys

articles_file = "/home/john/PycharmProjects/EVNews/insideevs_articles.csv"
url = 'https://insideevs.com'
html = urlopen("https://insideevs.com/news/?p=50")
soup = BeautifulSoup(html, "lxml")

articles = soup.find_all("div", "item")

storiesdf = []
# print(articles)
for article in articles:
    if article.find('h3') is None:
        continue
    article_title = article.find('h3').text
    article_title = article_title.encode('utf-8')
    article_title = article_title.decode("utf-8")

    article_link_tag = article.find('h3')
    article_link_step = article_link_tag.find('a', href=True)
    article_link = article_link_step.get('href')
    if not article_link.startswith('http'):
        article_link = url+article_link
    article_date_tag = article.find('span', 'date')
    if article_date_tag is None:
        continue
    article_date_step = str(article_date_tag).split('=')[2]

    article_date_step = str(article_date_step).split('>')[0]

    article_date_step = article_date_step.replace('"', '')
    ts = int(article_date_step)
    article_date = datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    article_body = article.find('a', 'text').text
    article_body = article_body.encode('utf-8')
    article_body = article_body.decode("utf-8")

    article_byline = article.find('span', 'name').text
    article_image_link = article.find('img', src=True)
    article_image = article_image_link.get('data-src')
    article_image_alt = article_image_link.get('alt')

    weboutlet = "Inside EVs"

    storiesdf.append((article_date, article_title, article_body, article_link, article_image,
                      article_byline, article_image_alt, weboutlet))


df = pd.DataFrame(storiesdf, columns=['date', 'title', 'short_description', 'article_link', 'image',
                                      'byline', 'alt', 'outlet'])
# df['date'] = pd.to_datetime(df['date'])
df.to_csv(articles_file, index=False, encoding='utf-8')


# subprocess.call([sys.executable, 'ev_news_insideev.py'])

#
# time.sleep(2)
#
# print("I hope I waited")
