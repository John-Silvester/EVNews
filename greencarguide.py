# from bs4 import BeautifulSoup
# import requests
# import pandas as pd
from dateutil.parser import parse
from my_functions import *

storieslist = []
storiesdf = []
pagenumber = 1
newrecord = True
articles_file = "greencarguide_articles.csv"
article_setup = False
weboutlet = 'greencarguide'


def main():
    global newrecord, pagenumber, storiesdf, storieslist, weboutlet, articles_file, article_setup
    df1 = pd.DataFrame(columns=['date', 'title', 'short_description', 'article_link', 'image',
                                'byline', 'alt', 'outlet'])
    if not article_setup:
        df1 = pd.read_csv(articles_file, encoding='utf-8')
        storieslist = df1["title"].head(10).tolist()

    while newrecord:
        print(weboutlet, ' page ', pagenumber, '\n')

        soup = make_soup('https://www.greencarguide.co.uk/green-car-news/page/' + str(pagenumber) + "/")

        articles = soup.find_all("card", "news")

        for article in articles:
            if article.find("span", "title") is None:
                continue
            article_title = get_element(article, "span", "title", text=True)
            if any(article_title in x for x in storieslist):
                newrecord = False
                break

            article_body = get_element(article, 'span', "description", clean_str=False)
            article_body = get_element(article_body, 'p', text=True)

            article_image = get_element(article, 'img', clean_str=False)
            article_image = article_image.get('data-lazy-src')
            article_image = article_image.replace('-600x400', '')

            article_date = get_element(article, 'span', "post-date", text=True)
            article_date = parse(article_date)

            article_byline = "by line: unknown"

            article_link = get_tag_attribute(article, 'a', 'href')

            article_image_alt = "Image not found"

            # print(article_title)
            # print(article_link)

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
