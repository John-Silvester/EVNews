# from bs4 import BeautifulSoup
import requests
# import pandas as pd
from dateutil.parser import parse
from my_functions import *

storieslist = []
storiesdf = []
pagenumber = 1
newrecord = True
articles_file = "teslarati_articles.csv"
article_setup = False
weboutlet = "Teslarati"


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

        soup = make_soup('https://www.teslarati.com/category/news/page/' + str(pagenumber) + "/")

        articles = soup.find_all('li', class_='infinite-post')

        for article in articles:
            if get_element(article, 'h2', clean_str=False) == 'Empty':
                continue
            article_title = get_element(article, 'h2', text=True)
            if any(article_title in x for x in storieslist):
                newrecord = False
                break

            article_link = get_tag_attribute(article, 'a', 'href')

            article_body = article.find('p').text

            article_image = get_tag_attribute(article, 'img', 'src')
            article_image_hi_res = article_image.replace('450x270', '1000x600')
            image_request = requests.get(article_image_hi_res)
            article_image = article_image_hi_res if image_request.status_code == 200 else article_image

            article_image_alt = "Image not found"

            temp_soup = make_soup(article_link)

            article_date = parse(get_element(temp_soup, "time", text=True))

            article_byline = get_element(temp_soup, "span", "author-name vcard fn author", text=True)

            # print()
            # print(article_byline)
            # print(article_date)
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
