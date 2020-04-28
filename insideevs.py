# from bs4 import BeautifulSoup
# import pandas as pd
# from dateutil.parser import parse

import datetime
from my_functions import *


storieslist = []
storiesdf = []
pagenumber = 1
newrecord = True
articles_file = "insideevs_articles.csv"
article_setup = False
weboutlet = 'Inside EVs'


def main():
    global newrecord, pagenumber, storiesdf, storieslist, weboutlet, articles_file, article_setup
    df1 = pd.DataFrame(columns=['date', 'title', 'short_description', 'article_link', 'image',
                                'byline', 'alt', 'outlet'])
    if not article_setup:
        df1 = pd.read_csv(articles_file, encoding='utf-8')
        storieslist = df1["title"].head(10).tolist()

    while newrecord:
        print('Inside EVs pass ', pagenumber)
        url = 'https://insideevs.com'

        soup = make_soup("https://insideevs.com/news/?p=" + str(pagenumber))

        articles = soup.find_all("div", "item")

        for article in articles:
            if get_element(article, 'h3', clean_str=False) == 'Empty':
                continue
            article_title = get_element(article, 'h3', text=True)
            if any(article_title in x for x in storieslist):
                newrecord = False
                break

            article_link = get_tag_attribute(article, 'a', 'href')
            if not article_link.startswith('http'):
                article_link = url+article_link

            article_date = get_tag_attribute(article, 'span', 'data-time', tag_class='date')
            if article_date == 'not_found':
                continue

            ts = int(article_date)
            article_date = datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

            article_body = get_element(article, 'a', 'text', text=True)

            article_byline = get_element(article, 'span', 'name', text=True)

            article_image = get_tag_attribute(article, 'img', 'data-src')

            article_image_alt = get_tag_attribute(article, 'img', 'alt')

            # print()
            # print(article_title)
            # print(article_date)
            # print(article_image)

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
