from bs4 import BeautifulSoup
import requests
import pandas as pd
from dateutil.parser import parse

storiesdf = []
pagenumber = 1
newrecord = True
articles_file = "chargedevs_articles.csv"

df1 = pd.read_csv(articles_file, encoding='utf-8')
storieslist = df1["title"].head(5).tolist()

while newrecord:
    print('Charged EVs pass ', pagenumber)
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}

    source = requests.get('https://chargedevs.com/category/newswire/page/' + str(pagenumber) + "/",
                          headers=headers).text
    soup = BeautifulSoup(source, 'lxml')

    articles = soup.find_all("article")

    for article in articles:
        if article.find('h3') is None:
            continue
        article_title = article.find('h3').text
        if any(article_title in x for x in storieslist):
            newrecord = False
            break
        article_title = article_title.encode('utf-8')
        article_title = article_title.decode("utf-8")

        article_body = article.find('section', "entry-content clearfix").text
        article_body = article_body.strip()
        article_body = article_body.replace("…  Read more »", "")

        article_image_url = article.find('img')
        article_image = article_image_url.get('src')

        article_date = article.find('time').text
        article_date = parse(article_date)

        article_link = article.find('div', "fourcol first featimg").a
        article_link = article_link.get('href')

        article_byline = article.find("span", "author").text

        weboutlet = "Charged EVs"

        article_image_alt = "Image not found"

        storiesdf.append((article_date, article_title, article_body, article_link, article_image,
                          article_byline, article_image_alt, weboutlet))

    pagenumber = pagenumber + 1

df2 = pd.DataFrame(storiesdf, columns=['date', 'title', 'short_description', 'article_link', 'image',
                                       'byline', 'alt', 'outlet'])

frames = [df2, df1]
df_final = pd.concat(frames, sort=False)

df_final.to_csv(articles_file, index=False, encoding='utf-8')
