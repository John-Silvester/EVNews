# from bs4 import BeautifulSoup
# import requests
# import pandas as pd
from dateutil.parser import parse
from my_functions import *

storieslist = []
storiesdf = []
pagenumber = 1
newrecord = True
articles_file = "electrek_articles.csv"
article_setup = False
weboutlet = "Electrek"


def main():
    global newrecord, pagenumber, storiesdf, storieslist, weboutlet, articles_file, article_setup
    df1 = pd.DataFrame(columns=['date', 'title', 'short_description', 'article_link', 'image',
                                'byline', 'alt', 'outlet'])
    if not article_setup:
        df1 = pd.read_csv(articles_file, encoding='utf-8')
        storieslist = df1["title"].head(10).tolist()

    while newrecord:
        print(weboutlet, ' page ', pagenumber, '\n')
        soup = make_soup("https://electrek.co/page/" + str(pagenumber) + "/")

        articles = soup.find_all("article", "post-content")

        for article in articles:
            if get_element(article, 'h1', 'post-title', clean_str=False) == 'Empty':
                continue
            article_title = get_element(article, 'h1', 'post-title', text=True)
            if any(article_title in x for x in storieslist):
                newrecord = False
                break

            article_link = get_element(article, 'h1', 'post-title', clean_str=False)
            article_link = get_tag_attribute(article_link, 'a', 'href')

            article_datetime = get_element(article, 'p', 'time-twitter', text=True)
            article_datetime = article_datetime.replace('- ', '')
            article_datetime = parse(article_datetime.replace(' ET', ''))

            article_body = get_element(article, 'div', "post-body", text=True)
            article_body = article_body.replace('expand full story', '', -1)

            article_image_url = get_tag_attribute(article, 'img', 'src')
            article_image_url, _ = article_image_url.split('?')

            article_byline = article.find('span', itemprop='name').text
            article_byline = str(make_utf8(article_byline))

            article_image_alt = "Image not found"

            # print(article_title)
            # print(article_link)

            storiesdf.append((article_datetime, article_title, article_body, article_link, article_image_url,
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
