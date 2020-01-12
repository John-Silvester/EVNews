from bs4 import BeautifulSoup
import requests
from dateutil.parser import parse
import pandas as pd

articles_file = 'reneweconomy_articles.csv'

source = requests.get('https://reneweconomy.com.au/category/smart-transport/page/70/').text

soup = BeautifulSoup(source, 'lxml')

articles = soup.find_all("article", "post-item")
# print(articles)

storiesdf = []

for article in articles:
    if article.find('h3') is None:
        continue
    article_title = article.find('h3').text
    article_title = article_title.encode('utf-8')
    article_title = article_title.decode("utf-8")

    if article.find('div', "entry-content") is None:
        article_body = ""
    else:
        article_body = article.find('div', "entry-content").text

    if article.find('span', 'lazy') is None:
        article_image = article.find("div", "post-image lazy")
        article_image = str(article_image)
    else:
        article_image_url = article.find('span', 'lazy')
        article_image = str(article_image_url)

    _, article_image = article_image.split('(')
    article_image, _ = article_image.split(')')
    article_image = article_image.replace("'", "", 2)

    article_date = article.find('time').text
    article_date = parse(article_date)
    if article.find("url fn n") is None:
        article_byline = article.find("a", "url fn n").text
    else:
        article_byline = article.find("url fn n").text

    article_link = article.find('a')
    article_link = article_link.get('href')

    weboutlet = "RenewEconomy"
    article_image_alt = "Post Image"

    storiesdf.append((article_date, article_title, article_body, article_link, article_image,
                      article_byline, article_image_alt, weboutlet))

    print()

    print(article_title)
    print(article_date)
    print(article_body)
    print(article_link)
#     print(article_image_url)
    print(article_image)
    print(article_byline)
    print(article_image_alt)
    print(weboutlet)


df = pd.DataFrame(storiesdf, columns=['date', 'title', 'short_description', 'article_link', 'image',
                                      'byline', 'alt', 'outlet'])
# df['date'] = pd.to_datetime(df['date'])

df.to_csv(articles_file, index=False, encoding='utf-8')
