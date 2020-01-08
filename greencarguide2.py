from bs4 import BeautifulSoup
import requests
import pandas as pd
from dateutil.parser import parse

storiesdf = []
pagenumber = 1
newrecord = True
articles_file = "greencarguide_articles.csv"

df1 = pd.read_csv(articles_file, encoding='utf-8')
storieslist = df1["title"].head(5).tolist()

while newrecord:
    print('green car guide pass ', pagenumber)
    source = requests.get('https://www.greencarguide.co.uk/green-car-news/page/' + str(pagenumber) + "/").text

    soup = BeautifulSoup(source, 'lxml')

    articles = soup.find_all("card", "news")

    for article in articles:
        if article.find("span", "title") is None:
            continue
        article_title = article.find("span", "title").text
        if any(article_title in x for x in storieslist):
            newrecord = False
            break
        article_title = article_title.encode('utf-8')
        article_title = article_title.decode("utf-8")

        article_body = article.find('span', "description").p.text

        article_image_url = article.find('img')
        article_image = article_image_url.get('data-lazy-srcset')
        *_, article_image = article_image.split(',')
        article_image = article_image.strip()
        article_image, *_ = article_image.split(" ")

        article_date = article.find('span', "post-date").text
        article_date = parse(article_date)
        article_byline = ""

        article_link = article.find('a')
        article_link = article_link.get('href')

        weboutlet = "greencarguide"
        article_image_alt = "Image not found"

        storiesdf.append((article_date, article_title, article_body, article_link, article_image,
                          article_byline, article_image_alt, weboutlet))

    pagenumber = pagenumber + 1

df2 = pd.DataFrame(storiesdf, columns=['date', 'title', 'short_description', 'article_link', 'image',
                                       'byline', 'alt', 'outlet'])

frames = [df2, df1]
df_final = pd.concat(frames, sort=False)

df_final.to_csv(articles_file, index=False, encoding='utf-8')
