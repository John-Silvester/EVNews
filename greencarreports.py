# from bs4 import BeautifulSoup
# import requests
# import pandas as pd
from dateutil.parser import parse
from my_functions import *

storieslist = []
storiesdf = []
pagenumber = 1
newrecord = True
articles_file = "greencarreports_articles.csv"
article_setup = False
weboutlet = "Green Car Reports"


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

        soup = make_soup('https://www.greencarreports.com/news/page-' + str(pagenumber))

        articles = soup.find_all("li")

        for article in articles:
            if get_element(article, 'a', 'title', clean_str=False) == 'Empty':
                continue
            article_title = get_element(article, 'a', 'title', text=True)
            if any(article_title in x for x in storieslist):
                newrecord = False
                break

            article_link = get_tag_attribute(article, 'a', 'href', tag_class='title')
            article_link = "https://www.greencarreports.com" + article_link

            article_body = get_element(article, 'p', text=True)

            img_wraper = get_element(article, "a", "img-wrap", clean_str=False)
            if get_tag_attribute(img_wraper, 'img', 'data-src') is not None:
                article_image = get_tag_attribute(img_wraper, 'img', 'data-src')
            else:
                article_image = get_tag_attribute(img_wraper, 'img', 'src')

            article_date = parse(get_element(article, 'time', text=True))

            article_byline = get_element(article, 'a', 'by-line', text=True)

            article_image_alt = get_tag_attribute(article, 'img', 'alt')

            if article_image == "not_found":
                temp_soup = make_soup(article_link)
                img_section = get_element(temp_soup, "div", "article-block", clean_str=False)
                article_image = get_tag_attribute(img_section, "section", "data-image-src-h")

            # print(article_title)
            # print(article_image)

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
