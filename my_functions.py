from bs4 import BeautifulSoup
import requests
import pandas as pd


def make_soup(web_address):
    # global pagenumber
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
    req_source = requests.get(web_address, headers=headers).text
    beautiful_output = BeautifulSoup(req_source, 'lxml')
    return beautiful_output


def make_utf8(string_in):
    string_in = string_in.encode('utf-8')
    string_out = string_in.decode("utf-8")
    return string_out


def get_element(html_code, tag_type, tag_class='', text=False, clean_str=True):
    new_string = ''
    if tag_class == '' and text is False:
        new_string = html_code.find(tag_type)
    if tag_class != '' and text is False:
        new_string = html_code.find(tag_type, tag_class)
    if new_string is None:
        new_string = 'Empty'
        return new_string

    if tag_class == '' and text is True:
        if html_code.find(tag_type) is None:
            new_string = 'Empty'
            return new_string
        new_string = html_code.find(tag_type).text
    if tag_class != '' and text is True:
        if html_code.find(tag_type, tag_class) is None:
            new_string = 'Empty'
            return new_string
        new_string = html_code.find(tag_type, tag_class).text
    if not clean_str:
        return new_string

    new_string = str(new_string)
    new_string = new_string.replace('\n', '')
    new_string = new_string.replace('\r', '')
    new_string = make_utf8(new_string)
    return new_string


def get_tag_attribute(html_code, tag_type, attribute, tag_class=''):
    if tag_class == '':
        new_string = html_code.find(tag_type).get(attribute)
    else:
        new_string = html_code.find(tag_type, tag_class).get(attribute)
    if new_string is None:
        new_string = 'not_found'
        return new_string

    new_string = str(make_utf8(new_string))
    return new_string


def update_articles(dframe1, dframe2, weboutlet, articles_file, article_count):
    # global articles_file
    new_df = pd.DataFrame(dframe2, columns=['date', 'title', 'short_description', 'article_link', 'image',
                                            'byline', 'alt', 'outlet'])

    frames = [new_df, dframe1]
    df_final = pd.concat(frames, sort=False)
    df_final.to_csv(articles_file, index=False, encoding='utf-8')
    print(f'{weboutlet} completed with {article_count} articles')
    return True


def setup_articles(dframe2, weboutlet, articles_file, article_count):
    # global articles_file
    new_df = pd.DataFrame(dframe2, columns=['date', 'title', 'short_description', 'article_link', 'image',
                                            'byline', 'alt', 'outlet'])
    new_df.to_csv(articles_file, index=False, encoding='utf-8')
    print(f'\n {weboutlet} completed with {article_count} articles')
    return True
