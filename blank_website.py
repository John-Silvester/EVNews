# from bs4 import BeautifulSoup
# import requests
# import pandas as pd
from dateutil.parser import parse
from my_functions import *

storieslist = []
storiesdf = []
pagenumber = 1
newrecord = True
articles_file = "cleantechnica_articles3.csv"
article_setup = False
weboutlet = 'CleanTechnica'


# def make_soup(web_address):
#     global pagenumber
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
#                       'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
#     req_source = requests.get(web_address, headers=headers).text
#     beautiful_output = BeautifulSoup(req_source, 'lxml')
#     return beautiful_output
#
#
# def make_utf8(string_in):
#     string_in = string_in.encode('utf-8')
#     string_out = string_in.decode("utf-8")
#     return string_out
#
#
# def get_element(html_code, tag_type, tag_class='', text=False, clean_str=True):
#     new_string = ''
#     if tag_class == '' and text is False:
#         new_string = html_code.find(tag_type)
#     if tag_class != '' and text is False:
#         new_string = html_code.find(tag_type, tag_class)
#     if new_string is None:
#         new_string = 'Empty'
#         return new_string
#
#     if tag_class == '' and text is True:
#         if html_code.find(tag_type) is None:
#             new_string = 'Empty'
#             return new_string
#         new_string = html_code.find(tag_type).text
#     if tag_class != '' and text is True:
#         if html_code.find(tag_type, tag_class) is None:
#             new_string = 'Empty'
#             return new_string
#         new_string = html_code.find(tag_type, tag_class).text
#     if not clean_str:
#         return new_string
#
#     new_string = str(new_string)
#     new_string = new_string.replace('\n', '')
#     new_string = new_string.replace('\r', '')
#     new_string = make_utf8(new_string)
#     return new_string
#
#
# def get_tag_attribute(html_code, tag_type, attribute, tag_class=''):
#     if tag_class == '':
#         new_string = html_code.find(tag_type).get(attribute)
#     else:
#         new_string = html_code.find(tag_type, tag_class).get(attribute)
#     if new_string is None:
#         new_string = 'not_found'
#         return new_string
#
#     new_string = str(make_utf8(new_string))
#     return new_string
#
#
# def update_articles(dframe1, dframe2):
#     global articles_file
#     new_df = pd.DataFrame(dframe2, columns=['date', 'title', 'short_description', 'article_link', 'image',
#                                             'byline', 'alt', 'outlet'])
#
#     frames = [new_df, dframe1]
#     df_final = pd.concat(frames, sort=False)
#     df_final.to_csv(articles_file, index=False, encoding='utf-8')
#     print(weboutlet, ' completed')
#     return True
#
#
# def setup_articles(dframe2):
#     global articles_file
#     new_df = pd.DataFrame(dframe2, columns=['date', 'title', 'short_description', 'article_link', 'image',
#                                             'byline', 'alt', 'outlet'])
#     new_df.to_csv(articles_file, index=False, encoding='utf-8')
#     print(weboutlet, ' completed')
#     return True


def main():
    global newrecord, pagenumber, storiesdf, storieslist, weboutlet, articles_file, article_setup
    df1 = pd.DataFrame(columns=['date', 'title', 'short_description', 'article_link', 'image',
                                'byline', 'alt', 'outlet'])
    if not article_setup:
        df1 = pd.read_csv(articles_file, encoding='utf-8')
        storieslist = df1["title"].head(10).tolist()

    while newrecord:
        print(weboutlet, ' page ', pagenumber, '\n')

        soup = make_soup('https://cleantechnica.com/category/clean-transport-2/page/' + str(pagenumber) + "/")

        articles = soup.find_all("article", "omc-blog-two omc-half-width-category")

        for article in articles:
            if get_element(article, 'h2', clean_str=False) == 'Empty':
                continue
            article_title = get_element(article, 'h2', text=True)
            if any(article_title in x for x in storieslist):
                newrecord = False
                break

            article_body = get_element(article, 'p', "omc-blog-two-exceprt", text=True)

            article_image = get_tag_attribute(article, 'img', 'src')
            article_image = article_image.replace("-290x166", "")

            article_date = get_element(article, 'p', "omc-blog-two-date", text=True)
            article_date, article_byline = article_date.split('|')
            article_date = parse(article_date.strip())

            article_byline = article_byline.strip()

            article_link = get_element(article, 'div', 'omc-blog-two-text', clean_str=False)
            article_link = get_tag_attribute(article_link, 'a', 'href')

            article_image_alt = "Image not found"

            print(article_title)
            print(article_link)

            storiesdf.append((article_date, article_title, article_body, article_link, article_image,
                              article_byline, article_image_alt, weboutlet))

        if article_setup:
            newrecord = False
            break
        pagenumber += 1

    if article_setup:
        setup_articles(storiesdf, weboutlet, articles_file)
    else:
        update_articles(df1, storiesdf, weboutlet, articles_file)


if __name__ == '__main__':
    main()
