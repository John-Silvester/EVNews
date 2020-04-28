# from bs4 import BeautifulSoup
# import requests
# import pandas as pd
from dateutil.parser import parse
from my_functions import *

storieslist = []
storiesdf = []
pagenumber = 1
newrecord = True
articles_file = "reneweconomy_articles.csv"
article_setup = False
weboutlet = "RenewEconomy"


def main():
    global newrecord, pagenumber, storiesdf, storieslist, weboutlet, articles_file, article_setup
    df1 = pd.DataFrame(columns=['date', 'title', 'short_description', 'article_link', 'image',
                                'byline', 'alt', 'outlet'])
    if not article_setup:
        df1 = pd.read_csv(articles_file, encoding='utf-8')
        storieslist = df1["title"].head(10).tolist()

    while newrecord:
        print(weboutlet, ' page ', pagenumber, '\n')

        soup = make_soup('https://reneweconomy.com.au/category/smart-transport/page/' + str(pagenumber) + "/")

        articles = soup.find_all("article", "post-item")

        for article in articles:
            if get_element(article, 'h3', clean_str=False) == 'Empty':
                continue
            article_title = get_element(article, 'h3', text=True)
            if any(article_title in x for x in storieslist):
                newrecord = False
                break

            article_body = get_element(article, 'div', 'entry-content', text=True)

            if article.find('span', 'lazy') is None:
                article_image = str(get_element(article, 'div', 'post-image lazy'))
            else:
                article_image = str(get_element(article, 'span', 'lazy'))

            try:
                article_image = article_image[article_image.find("(") + 1:article_image.find(")")]
                article_image = article_image.replace("'", "", 2)
            except RuntimeError:
                article_image = ""

            if article.find('time', "entry-date published updated") is None:
                article_date = parse(get_element(article, 'time', "entry-date published", text=True))
            else:
                article_date = parse(get_element(article, 'time', "entry-date published updated", text=True))

            article_byline = get_element(article, "a", "url fn n", text=True)

            article_link = get_element(article, 'h3', 'entry-title', clean_str=False)
            article_link = get_tag_attribute(article_link, 'a', 'href')

            article_image_alt = "Post Image"

            storiesdf.append((article_date, article_title, article_body, article_link, article_image,
                              article_byline, article_image_alt, weboutlet))

            # print()
            # print(article_title)
            # print(article_body)
            # #
            # print(article_date)
            # print(article_byline)
            # print(article_link)
            # print(article_image)
            # print(article_image_alt)
            # print(weboutlet)

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
