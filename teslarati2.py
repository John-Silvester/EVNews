from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import date, timedelta

storiesdf = []
pagenumber = 1
newrecord = True
articles_file = "teslarati_articles.csv"

df1 = pd.read_csv(articles_file, encoding='utf-8')
storieslist = df1["title"].head(5).tolist()

while newrecord:
    print('Teslarati pass ', pagenumber)

    source = requests.get('https://www.teslarati.com/category/news/page/' + str(pagenumber) + "/").text

    soup = BeautifulSoup(source, 'lxml')

    articles = soup.find_all('li', class_='infinite-post')

    for article in articles:
        if article.find('h2') is None:
            continue
        article_title = article.find('h2').text
        if any(article_title in x for x in storieslist):
            newrecord = False
            break
        article_title = article_title.encode('utf-8')
        article_title = article_title.decode("utf-8")

        article_body = article.find('p').text

        article_image_url = article.find('div', class_="archive-list-out").div.img
        article_image = article_image_url.get('src')

        article_link = article.find('a')
        article_link = article_link.get('href')

        weboutlet = "Teslarati"
        article_image_alt = "Image not found"

        article_date = date.today() - timedelta(1)
        article_byline = ""

        storiesdf.append((article_date, article_title, article_body, article_link, article_image,
                          article_byline, article_image_alt, weboutlet))

    pagenumber = pagenumber + 1

df2 = pd.DataFrame(storiesdf, columns=['date', 'title', 'short_description', 'article_link', 'image',
                                       'byline', 'alt', 'outlet'])
frames = [df2, df1]
df_final = pd.concat(frames, sort=False)

df_final.to_csv(articles_file, index=False, encoding='utf-8')
