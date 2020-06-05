# from bs4 import BeautifulSoup
# import requests
# import pandas as pd
from dateutil.parser import parse
from my_functions import *

storieslist = []
storiesdf = []
pagenumber = 1
newrecord = True
articles_file = "electrive_articles.csv"
article_setup = False
weboutlet = 'electrive'


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
        if pagenumber == 1:
            soup = make_soup('https://www.electrive.com/category/automobile/')
        else:
            soup = make_soup('https://www.electrive.com/category/automobile/page/' + str(pagenumber) + "/")

        articles = soup.find_all("article", "teaser row")

        for article in articles:
            if get_element(article, 'h3', clean_str=False) is None:
                continue
            article_title = get_element(article, 'h3', text=True)
            if any(article_title in x for x in storieslist):
                newrecord = False
                break

            article_link = get_tag_attribute(article, 'a', 'href')

            article_body = get_element(article, 'p', text=True)

            article_image = get_tag_attribute(article, 'img', 'src')
            article_image = article_image.replace('-300x150', '')

            article_date = parse(get_element(article, 'span', "meta", text=True))

            temp_soup = make_soup(article_link)
            article_byline = get_element(temp_soup, "span", "author", text=True)

            article_image_alt = "Image not found"

            # print()
            # print(article_title)
            print(article_byline)
            # print(article_body)

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
