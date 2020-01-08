from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

storiesdf = []
pagenumber = 1
newrecord = True
articles_file = "electrek_articles.csv"

df1 = pd.read_csv(articles_file, encoding='utf-8')
storieslist = df1["title"].head(5).tolist()

while newrecord:
    print('Electrek pass ', pagenumber)
    html = urlopen("https://electrek.co/page/" + str(pagenumber) + "/")
    soup = BeautifulSoup(html, "lxml")

    articles = soup.find_all("article", "post-content")

    for article in articles:
        if article.find('h1', 'post-title') is None:
            continue
        article_title = article.find('h1', 'post-title').text
        if any(article_title in x for x in storieslist):
            newrecord = False
            break
        article_title = article_title.encode('utf-8')
        article_title = article_title.decode("utf-8")

        article_link_tag = article.find('h1', 'post-title')
        article_link_step = article_link_tag.find('a', href=True)
        article_link = article_link_step.get('href')

        article_datetime = article.find('p', 'time-twitter').text.strip()
        article_datetime = article_datetime.replace('- ', '')
        article_datetime = article_datetime.replace(' ET', '')

        article_body = article.find('div', "post-body").text.strip()
        article_body = article_body.replace('expand full story', '', -1)
        article_body = article_body.replace('\n', '', -1)
        article_body = article_body.encode('utf-8')
        article_body = article_body.decode("utf-8")

        article_image_url_step = article.find('img')
        article_image_url = article_image_url_step.get('src')

        article_byline = article.find('span', itemprop='name').text
        article_byline = str(article_byline)
        article_byline = article_byline.encode('utf-8')
        article_byline = article_byline.decode("utf-8")

        article_image_alt = "Image not found"

        weboutlet = "Electrek"

        storiesdf.append((article_datetime, article_title, article_body, article_link, article_image_url,
                          article_byline, article_image_alt, weboutlet))

    pagenumber = pagenumber+1
#
df2 = pd.DataFrame(storiesdf, columns=['date', 'title', 'short_description', 'article_link', 'image',
                                       'byline', 'alt', 'outlet'])
df2['date'] = pd.to_datetime(df2['date'])


frames = [df2, df1]
df_final = pd.concat(frames, sort=False)

df_final.to_csv(articles_file, index=False, encoding='utf-8')
