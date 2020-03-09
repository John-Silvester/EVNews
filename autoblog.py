from bs4 import BeautifulSoup
import requests
from dateutil.parser import parse
import pandas as pd
import json

articles_file = 'autoblog_articles.csv'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}

source = requests.get('https://www.autoblog.com/green/pg-19/#', headers=headers).text

soup = BeautifulSoup(source, 'lxml')

articles = soup.find_all("div", "list_record")
# print(article)

storiesdf = []

for article in articles:
    if article.find('script', type="application/ld+json") is None:
        continue
    scriptjson = article.find('script', type="application/ld+json").text
    scriptjson = json.loads(scriptjson)
    # print(scriptjson)

    article_title = scriptjson['headline']
    article_date = scriptjson['datePublished']
    article_date = parse(article_date)
    article_link = scriptjson['url']
    article_byline = scriptjson['author']['name']
    article_image = scriptjson['image']['url']
    *_, article_image = article_image.split('http')
    article_image = "http" + article_image
    article_body = scriptjson['alternativeHeadline']
    weboutlet = scriptjson['publisher']['name']
    article_image_alt = "image not found"

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
df.to_csv(articles_file, index=False, encoding='utf-8')
