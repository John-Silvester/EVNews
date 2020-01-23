from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import datetime

storiesdf = []
pagenumber = 1
newrecord = True
articles_file = "insideevs_articles.csv"

df1 = pd.read_csv(articles_file)
storieslist = df1["title"].head(5).tolist()

while newrecord:
    print('Inside EVs pass ', pagenumber)
    url = 'https://insideevs.com'
    html = urlopen("https://insideevs.com/news/?p=" + str(pagenumber))
    soup = BeautifulSoup(html, "lxml")

    articles = soup.find_all("div", "item")

    for article in articles:
        if article.find('h3') is None:
            continue
        article_title = article.find('h3').text
        if any(article_title in x for x in storieslist):
            newrecord = False
            break
        article_title = article_title.encode('utf-8')
        # print(article_title)
        article_title = article_title.decode("utf-8")
        article_title = str(article_title)
        article_link_tag = article.find('h3')
        article_link_step = article_link_tag.find('a', href=True)
        article_link = article_link_step.get('href')
        if not article_link.startswith('http'):
            article_link = url+article_link
        article_date_tag = article.find('span', 'date')
        if article_date_tag is None:
            continue
        article_date_step = article_date_tag.get('data-time')
        ts = int(article_date_step)
        article_date = datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        article_body = article.find('a', 'text').text
        article_body = article_body.encode('utf-8')
        article_body = article_body.decode("utf-8")
        article_body = str(article_body)
        article_byline = article.find('span', 'name').text
        article_image_link = article.find('img', src=True)
        article_image = article_image_link.get('data-src')
        article_image_alt = article_image_link.get('alt')
        article_image_alt = article_image_alt.encode('utf-8')
        article_image_alt = article_image_alt.decode("utf-8")
        weboutlet = "Inside EVs"

        storiesdf.append((article_date, article_title, article_body, article_link, article_image,
                          article_byline, article_image_alt, weboutlet))

    pagenumber = pagenumber + 1

df2 = pd.DataFrame(storiesdf, columns=['date', 'title', 'short_description', 'article_link', 'image',
                                       'byline', 'alt', 'outlet'])
frames = [df2, df1]
df_final = pd.concat(frames, sort=False)

df_final.to_csv(articles_file, index=False, encoding='utf-8')
