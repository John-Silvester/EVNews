# from bs4 import BeautifulSoup
# import requests
# import pandas as pd
from dateutil.parser import parse
from my_functions import *

storieslist = []
storiesdf = []
pagenumber = 1
newrecord = True
articles_file = "thedriven_articles.csv"
article_setup = False
weboutlet = 'The Driven'


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

        soup = make_soup('https://thedriven.io/category/ev-news/page/' + str(pagenumber) + "/")

        articles = soup.find_all("article")

        for article in articles:
            if get_element(article, 'h2', "entry-title", clean_str=False) == 'Empty':
                continue
            article_title = get_element(article, 'h2', "entry-title", text=True)
            if any(article_title in x for x in storieslist):
                newrecord = False
                break

            article_body = get_element(article, 'div', "post-excerpt", text=True)

            image_element = get_element(article, 'div', "post-thumbnail", clean_str=False)
            if image_element == "Empty":
                image_element = get_element(article, 'section', "post-media", clean_str=False)
            article_image = get_tag_attribute(image_element, 'img', 'data-src')
            article_image = article_image.replace("-560x420", "")

            article_date = get_element(article, 'li', "meta-date", text=True)
            article_date = parse(article_date.strip())

            article_byline = get_element(article, 'li', "meta-author", text=True).strip()

            article_link = get_element(article, 'h2', 'entry-title', clean_str=False)
            article_link = get_tag_attribute(article_link, 'a', 'href')

            article_image_alt = get_tag_attribute(image_element, 'img', 'alt')

            # print(article_title)
            # print(article_body)
            # print(article_image)
            # print(article_date)
            # print(article_byline)
            # print(article_link)
            # print(article_image_alt)
            # print()

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
