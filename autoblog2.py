from bs4 import BeautifulSoup
import requests
from dateutil.parser import parse
import pandas as pd
import json

storiesdf = []
pagenumber = 1
newrecord = True
articles_file = "autoblog_articles.csv"

df1 = pd.read_csv(articles_file, encoding='utf-8')
storieslist = df1["title"].head(5).tolist()
# print(df1)

while newrecord:
    print('autoblog pass ', pagenumber)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
    }

    source = requests.get('https://www.autoblog.com/green/pg-' + str(pagenumber) + '/#', headers=headers).text

    soup = BeautifulSoup(source, 'lxml')

    articles = soup.find_all("div", "list_record")
    # print(article)
    for article in articles:
        if article.find('script', type="application/ld+json") is None:
            continue
        scriptjson = article.find('script', type="application/ld+json").text
        scriptjson = json.loads(scriptjson)
        # print(scriptjson)
        article_title = scriptjson['headline']
        if any(article_title in x for x in storieslist):
            newrecord = False
            break
        article_date = scriptjson['datePublished']
        article_date = parse(article_date)
        article_link = scriptjson['url']
        article_byline = scriptjson['author']['name']
        article_image = scriptjson['image']['url']
        *_, article_image = article_image.split('http')
        article_image = "http" + article_image
        try:
            article_body = scriptjson['alternativeHeadline']
        except KeyError:
            article_body = 'empty'
        weboutlet = scriptjson['publisher']['name']
        article_image_alt = "image not found"

        storiesdf.append((article_date, article_title, article_body, article_link, article_image,
                          article_byline, article_image_alt, weboutlet))

        # print()
        # print(article_date)
        # print(article_byline)
        #
        # print(article_title)
        # print(article_body)
        # print(article_link)
        # print(article_image)
        # print(article_image_alt)
        # print(weboutlet)

    pagenumber = pagenumber + 1


df2 = pd.DataFrame(storiesdf, columns=['date', 'title', 'short_description', 'article_link', 'image',
                                       'byline', 'alt', 'outlet'])

frames = [df2, df1]
df_final = pd.concat(frames, sort=False)

df_final.to_csv(articles_file, index=False, encoding='utf-8')
