# from bs4 import BeautifulSoup
# import requests
# import pandas as pd
from dateutil.parser import parse
from my_functions import *

storieslist = []
storiesdf = []
pagenumber = 1
newrecord = True
articles_file = "thevergecars_articles.csv"
article_setup = False
weboutlet = 'The Verge - cars'


def main():
    global newrecord, pagenumber, storiesdf, storieslist, weboutlet, articles_file, article_setup
    df1 = pd.DataFrame(columns=['date', 'title', 'short_description', 'article_link', 'image',
                                'byline', 'alt', 'outlet'])
    if not article_setup:
        df1 = pd.read_csv(articles_file, encoding='utf-8')
        storieslist = df1["title"].head(10).tolist()

    while newrecord:
        print(weboutlet, ' page ', pagenumber, '\n')

        soup = make_soup('https://www.theverge.com/cars/archives/' + str(pagenumber) + "/")

        articles = soup.find_all("div", "c-compact-river__entry")

        for article in articles:
            if get_element(article, 'h2', clean_str=False) == 'Empty':
                continue
            article_title = get_element(article, 'h2', text=True)
            if any(article_title in x for x in storieslist):
                newrecord = False
                break

            article_body = article_title

            article_image = get_element(article, 'noscript', clean_str=False)
            article_image = get_tag_attribute(article_image, 'img', 'src')

            article_date = get_tag_attribute(article, 'time', 'datetime', tag_class='c-byline__item')
            article_date = parse(article_date)

            if get_element(article, 'span', 'c-byline__author-name') == 'Empty':
                article_byline = "by line unknown"
            else:
                article_byline = get_element(article, 'span', 'c-byline__author-name', text=True)

            article_link = get_element(article, 'h2', 'c-entry-box--compact__title', clean_str=False)
            article_link = get_tag_attribute(article_link, 'a', 'href')

            article_image_alt = "Image not found"

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
