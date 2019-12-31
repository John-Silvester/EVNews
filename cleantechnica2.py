from bs4 import BeautifulSoup
# from urllib.request import urlopen
import requests
import pandas as pd
# from datetime import date, timedelta
from dateutil.parser import parse

storiesdf = []
pagenumber = 1
newrecord = True
articles_file = "/home/john/PycharmProjects/EVNews/cleantechnica_articles.csv"

df1 = pd.read_csv(articles_file, encoding='utf-8')
storieslist = df1["title"].head(5).tolist()
# print(df1)

while newrecord:
    print('pass ', pagenumber)
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}
    source = requests.get('https://cleantechnica.com/category/clean-transport-2/page/' + str(pagenumber) + "/",
                          headers=headers).text

    soup = BeautifulSoup(source, 'lxml')

    articles = soup.find_all("article", "omc-blog-two omc-half-width-category")
    # print(articles)

    for article in articles:
        if article.find('h2').a is None:
            continue
        article_title = article.find('h2').text
        if any(article_title in x for x in storieslist):
            newrecord = False
            break
        article_title = article_title.encode('utf-8')
        article_title = article_title.decode("utf-8")

        article_body = article.find('p', "omc-blog-two-exceprt").text

        article_image_url = article.find('img')
        article_image = article_image_url.get('src')

        article_date = article.find('p', class_="omc-blog-two-date").text
        article_date, article_byline = article_date.split('|')
        article_date = article_date.strip()
        article_date = parse(article_date)
        article_byline = article_byline.strip()

        article_link = article.find_all('a')
        _, article_link, *args = article_link
        article_link = article_link.get('href')
        weboutlet = "CleanTechnica"
        article_image_alt = "Image not found"

        storiesdf.append((article_date, article_title, article_body, article_link, article_image,
                          article_byline, article_image_alt, weboutlet))

        #
        # print(article_date)
        # print(article_byline)
        #
        # print(article_title)
        # print(article_body)
        # print(article_link)
        # print(article_image)
        # print(article_image_alt)
        # print(weboutlet)

    pagenumber = pagenumber + 1


df2 = pd.DataFrame(storiesdf, columns=['date', 'title', 'short_description', 'article_link', 'image',
                                       'byline', 'alt', 'outlet'])
# print(storiesdf)
#
# print(df1)
# print(df2)
frames = [df2, df1]
df_final = pd.concat(frames, sort=False)

df_final.to_csv(articles_file, index=False, encoding='utf-8')
