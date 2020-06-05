# from bs4 import BeautifulSoup
# import requests
# import pandas as pd
from dateutil.parser import parse
from my_functions import *

storieslist = []
storiesdf = []
pagenumber = 1
newrecord = True
articles_file = "evobsession_articles.csv"
article_setup = False
weboutlet = 'EV Obsession'


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

        soup = make_soup('https://evobsession.com/category/electric-vehicles/100-electric-vehicles/page/'
                         + str(pagenumber) + "/")

        articles = soup.find_all("article", "item")

        for article in articles:
            if get_element(article, 'h2', "grid-title") is None:
                continue
            article_title = get_element(article, 'h2', "grid-title", text=True)
            if any(article_title in x for x in storieslist):
                newrecord = False
                break

            article_link = get_tag_attribute(article, 'a', 'href', tag_class='penci-image-holder')

            article_body = article_title

            article_image = get_tag_attribute(article, 'a', 'data-src', tag_class='penci-image-holder')
            article_image, *args = article_image.split('?', 1)

            article_date = get_element(article, 'div', 'grid-post-box-meta', text=True, clean_str=False)
            article_date = article_date.strip()
            article_byline, article_date = article_date.split('\n')
            article_date = parse(article_date)

            article_byline = make_utf8(article_byline)

            article_image_alt = "Image not found"

            # print(article_title)
            # print(article_link)

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
