from bs4 import BeautifulSoup
import requests
from dateutil.parser import parse
import pandas as pd

articles_file = 'chargedevs_articles.csv'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}

source = requests.get('https://chargedevs.com/category/newswire/page/2/', headers=headers).text

soup = BeautifulSoup(source, 'lxml')

articles = soup.find_all("article")
# print(articles)

storiesdf = []

for article in articles:
    if article.find('h3') is None:
        continue
    article_title = article.find('h3').text
    article_title = article_title.encode('utf-8')
    article_title = article_title.decode("utf-8")

    article_body = article.find('section', "entry-content clearfix").text
    article_body = article_body.strip()
    article_body = article_body.replace("…  Read more »", "")

    article_image_url = article.find('img')
    article_image = article_image_url.get('src')

    article_date = article.find('time').text
    article_date = parse(article_date)

    article_byline = article.find("span", "author").text

    article_link = article.find('div', "fourcol first featimg").a
    article_link = article_link.get('href')

    weboutlet = "Charged EVs"

    article_image_alt = "Image not found"

    storiesdf.append((article_date, article_title, article_body, article_link, article_image,
                      article_byline, article_image_alt, weboutlet))

df = pd.DataFrame(storiesdf, columns=['date', 'title', 'short_description', 'article_link', 'image',
                                      'byline', 'alt', 'outlet'])

df.to_csv(articles_file, index=False, encoding='utf-8')
