from bs4 import BeautifulSoup
import requests
import pandas as pd
from dateutil.parser import parse

storiesdf = []
pagenumber = 1
newrecord = True
articles_file = "thevergecars_articles.csv"

df1 = pd.read_csv(articles_file, encoding='utf-8')
storieslist = df1["title"].head(5).tolist()
# print(df1)

while newrecord:
    print('The Verge - cars pass ', pagenumber)
    articles_file = 'thevergecars_articles.csv'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}

    source = requests.get('https://www.theverge.com/cars/archives/' + str(pagenumber) + "/", headers=headers).text

    soup = BeautifulSoup(source, 'lxml')

    articles = soup.find_all("div", "c-compact-river__entry")
    # print(articles)

    for article in articles:
        if article.find('h2') is None:
            continue
        article_title = article.find('h2').text
        if any(article_title in x for x in storieslist):
            newrecord = False
            break
        article_title = article_title.encode('utf-8')
        article_title = article_title.decode("utf-8")

        article_body = article_title

        article_image_url = article.find('noscript').img
        article_image = article_image_url.get('src')

        article_date = article.find('time', class_="c-byline__item")
        article_date = article_date.get('datetime')
        article_date = parse(article_date)

        if article.find('span', 'c-byline__author-name') is None:
            article_byline = ""
        else:
            article_byline = article.find('span', 'c-byline__author-name').text

        article_link = article.find('h2').a
        article_link = article_link.get('href')

        weboutlet = "The Verge - cars"
        article_image_alt = "Image not found"

        storiesdf.append((article_date, article_title, article_body, article_link, article_image,
                          article_byline, article_image_alt, weboutlet))

        # print()
        # print(article_date)
        # print(article_byline)
        #
        # print(article_title)
        # print(article_body)
        # print(article_link)
        # print(article_image)
        # print(article_image_alt)
        # print(weboutlet)
#
    pagenumber = pagenumber + 1


df2 = pd.DataFrame(storiesdf, columns=['date', 'title', 'short_description', 'article_link', 'image',
                                       'byline', 'alt', 'outlet'])

frames = [df2, df1]
df_final = pd.concat(frames, sort=False)

df_final.to_csv(articles_file, index=False, encoding='utf-8')
