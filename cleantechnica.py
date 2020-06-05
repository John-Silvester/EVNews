# from bs4 import BeautifulSoup
# import requests
# import pandas as pd
from dateutil.parser import parse
from my_functions import *

storieslist = []
storiesdf = []
pagenumber = 1
newrecord = True
articles_file = "cleantechnica_articles.csv"
article_setup = False
weboutlet = 'CleanTechnica'


def main():
    global newrecord, pagenumber, storiesdf, storieslist, weboutlet, articles_file, article_setup
    article_counter = 0
    df1 = pd.DataFrame(columns=['date', 'title', 'short_description', 'article_link', 'image',
                                'byline', 'alt', 'outlet'])
    if not article_setup:
        df1 = pd.read_csv(articles_file, encoding='utf-8')
        storieslist = df1["title"].head(10).tolist()

    while newrecord:
        print(weboutlet, ' page ', pagenumber, '\n')

        soup = make_soup('https://cleantechnica.com/category/clean-transport-2/page/' + str(pagenumber) + "/")

        articles = soup.find_all("article", "omc-blog-two omc-half-width-category")

        for article in articles:
            if get_element(article, 'h2', clean_str=False) == 'Empty':
                continue
            article_title = get_element(article, 'h2', text=True)
            if any(article_title in x for x in storieslist):
                newrecord = False
                break

            article_link = get_element(article, 'div', 'omc-blog-two-text', clean_str=False)
            article_link = get_tag_attribute(article_link, 'a', 'href')

            article_body = get_element(article, 'p', "omc-blog-two-exceprt", text=True)

            article_image = get_tag_attribute(article, 'img', 'src')
            article_image = article_image.replace("-290x166", "")

            article_date = get_element(article, 'p', "omc-blog-two-date", text=True)
            article_date, article_byline = article_date.split('|')
            article_date = parse(article_date.strip())

            article_byline = article_byline.strip()

            article_image_alt = "Image not found"

            # print(article_title)
            # print(weboutlet)

            storiesdf.append((article_date, article_title, article_body, article_link, article_image,
                              article_byline, article_image_alt, weboutlet))
            article_counter += 1

        if article_setup:
            newrecord = False
            break
        pagenumber += 1

    if article_setup:
        setup_articles(storiesdf, weboutlet, articles_file, article_counter)
    else:
        update_articles(df1, storiesdf, weboutlet, articles_file, article_counter)


if __name__ == '__main__':
    main()
