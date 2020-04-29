# from bs4 import BeautifulSoup
# import requests
# import pandas as pd
from dateutil.parser import parse
from my_functions import *
import json

storieslist = []
storiesdf = []
pagenumber = 1
newrecord = True
articles_file = "autoblog_articles.csv"
article_setup = False
weboutlet = 'Autoblog'


def main():
    global newrecord, pagenumber, storiesdf, storieslist, weboutlet, articles_file, article_setup
    df1 = pd.DataFrame(columns=['date', 'title', 'short_description', 'article_link', 'image',
                                'byline', 'alt', 'outlet'])
    if not article_setup:
        df1 = pd.read_csv(articles_file, encoding='utf-8')
        storieslist = df1["title"].head(10).tolist()

    while newrecord:
        print(weboutlet, ' page ', pagenumber, '\n')

        soup = make_soup('https://www.autoblog.com/green/pg-' + str(pagenumber) + '/#')

        articles = soup.find_all("div", "list_record")
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
            # weboutlet = 'Autoblog'
            article_image_alt = "image not found"

            # print()
            # print(article_date)
            # print(article_byline)
            # print(article_title)
            # print(article_body)
            # print(article_link)
            # print(article_image)
            # print(article_image_alt)
            # print(weboutlet)

            storiesdf.append((article_date, article_title, article_body, article_link, article_image,
                              article_byline, article_image_alt, weboutlet))

        if article_setup:
            newrecord = False
            break
        pagenumber += 1

    if article_setup:
        setup_articles(storiesdf, weboutlet, articles_file)
    else:
        update_articles(df1, storiesdf, weboutlet, articles_file)


if __name__ == '__main__':
    main()
