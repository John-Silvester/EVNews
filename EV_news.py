from flask import Flask, render_template, request
import pandas as pd
import subprocess
import sys

app = Flask(__name__)

# set number of articles (snoa)
snoa = 20


def retrieve_posts(source_file):
    global snoa
    # Use pandas to access data from CSV
    df1 = pd.read_csv(source_file, encoding='utf-8')
    df2 = df1.head(snoa)
    posts = df2.to_dict('r')
    return posts


@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template("EV_home.html",
                           title="Home",
                           outlet_page="/home")


@app.route("/site/<site_name>", methods=['GET', 'POST'])
def all_articles(site_name):
    global snoa
    if request.method == 'POST':
        snoa = int(request.form['page_num'])
    sitetitles_file = "sitetitles.csv"
    df1 = pd.read_csv(sitetitles_file, encoding='utf-8')
    df1 = df1[df1.site.str.contains(site_name, case=False)]
    title = df1['title']
    title = title.to_string(index=False).strip()
    outlet_page = "/site/" + df1['site']
    outlet_page = outlet_page.to_string(index=False).strip()
    source_file = df1['site'] + '_articles.csv'
    source_file = source_file.to_string(index=False).strip()

    posts = retrieve_posts(source_file)
    return render_template("EV_article.html",
                           posts=posts,
                           title=title,
                           outlet_page=outlet_page)


@app.route("/search", methods=['GET', 'POST'])
def search():
    global snoa
    if request.method == 'POST':
        source_search = request.form['outlet'].replace("/site/", "")
        source_file = source_search + "_articles.csv"
        df1 = pd.read_csv(source_file, encoding='utf-8')
        search_text = request.form['search']
        df2 = df1[df1.short_description.str.contains(search_text, case=False)]
        df2 = df2.head(snoa)
        posts = df2.to_dict('r')
        return render_template('EV_article.html',
                               title='Search ' + source_search,
                               posts=posts,
                               outlet_page="/site/" + source_search)


@app.route("/updatearticles")
def updatearticles():
    subprocess.call([sys.executable, './update_articles.py'])
    return render_template("EV_home.html", title="Home")


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/ev_database", endpoint='ev_database')
@app.route("/evdb", endpoint='evdb')
def evdb():
    if request.endpoint == 'ev_database':
        web_address = "https://ev-database.org/"
    else:
        web_address = "https://evdb.io/ev?sort=1&carType=car&evType=EV"
    return render_template('EV_DB.html',
                           title='EV DB',
                           web_address=web_address)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
