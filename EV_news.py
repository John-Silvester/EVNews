from flask import Flask, url_for, render_template, request
import csv
import pandas as pd
import subprocess
import sys

app = Flask(__name__)

# set number of articles (snoa)
snoa = 20
temp_file = "temp_articles.csv"


def retrieve_posts(source_file):
    global snoa
    # Use pandas to access data from CSV
    df1 = pd.read_csv(source_file, encoding='utf-8')
    df2 = df1.head(snoa)
    # posts = df2.to_dict('list')
    df2.to_csv(temp_file, index=False, encoding='utf-8')
    # Use DictReader to access data from CSV
    f = open(temp_file, newline='', encoding="utf-8")
    posts = csv.DictReader(f)
    return posts


@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template("EV_home.html",
                           title="Home",
                           outlet_page="/home")


@app.route("/electrek", methods=['GET', 'POST'])
def electrek():
    global snoa
    # source_file = url_for('EVNews', filename='electrek_articles.csv')
    source_file = "electrek_articles.csv"
    if request.method == 'POST':
        snoa = int(request.form['page_num'])
    posts = retrieve_posts(source_file)
    return render_template("EV_article.html",
                           posts=posts,
                           title="Electrek",
                           outlet_page="/electrek")


@app.route("/insideevs", methods=['GET', 'POST'])
def insideevs():
    global snoa
    source_file = "insideevs_articles.csv"
    if request.method == 'POST':
        snoa = int(request.form['page_num'])
    posts = retrieve_posts(source_file)
    return render_template("EV_article.html",
                           posts=posts,
                           title="insideevs",
                           outlet_page="/insideevs")


@app.route("/teslarati", methods=['GET', 'POST'])
def teslarati():
    global snoa
    source_file = "teslarati_articles.csv"
    if request.method == 'POST':
        snoa = int(request.form['page_num'])
    posts = retrieve_posts(source_file)
    return render_template("EV_article.html",
                           posts=posts,
                           title="TESLARATI",
                           outlet_page="/teslarati")


@app.route("/greencarguide", methods=['GET', 'POST'])
def greencarguide():
    global snoa
    source_file = "greencarguide_articles.csv"
    if request.method == 'POST':
        snoa = int(request.form['page_num'])
    posts = retrieve_posts(source_file)
    return render_template("EV_article.html",
                           posts=posts,
                           title="Green Car Guide",
                           outlet_page="/greencarguide")


@app.route("/cleantechnica", methods=['GET', 'POST'])
def cleantechnica():
    global snoa
    source_file = "cleantechnica_articles.csv"
    if request.method == 'POST':
        snoa = int(request.form['page_num'])
    posts = retrieve_posts(source_file)
    return render_template("EV_article.html",
                           posts=posts,
                           title="Clean Technica",
                           outlet_page="/cleantechnica")


@app.route("/greencarreports", methods=['GET', 'POST'])
def greencarreports():
    global snoa
    source_file = "greencarreports_articles.csv"
    if request.method == 'POST':
        snoa = int(request.form['page_num'])
    posts = retrieve_posts(source_file)
    return render_template("EV_article.html",
                           posts=posts,
                           title="Green Car Reports",
                           outlet_page="/greencarreports")


@app.route("/chargedevs", methods=['GET', 'POST'])
def chargedevs():
    global snoa
    source_file = "chargedevs_articles.csv"
    if request.method == 'POST':
        snoa = int(request.form['page_num'])
    posts = retrieve_posts(source_file)
    return render_template("EV_article.html",
                           posts=posts,
                           title="Charged EVs",
                           outlet_page="/chargedevs")


@app.route("/electrive", methods=['GET', 'POST'])
def electrive():
    global snoa
    source_file = "electrive_articles.csv"
    if request.method == 'POST':
        snoa = int(request.form['page_num'])
    posts = retrieve_posts(source_file)
    return render_template("EV_article.html",
                           posts=posts,
                           title="electrive",
                           outlet_page="/electrive")


@app.route("/updatearticles")
def updatearticles():
    subprocess.call([sys.executable, './update_articles.py'])
    return render_template("EV_home.html", title="Home")


@app.route("/search", methods=['GET', 'POST'])
def search():
    global snoa
    if request.method == 'POST':
        # page_num = int(request.form['page_num'])
        source_search = request.form['outlet']
        source_file = source_search + "_articles.csv"
        source_file = source_file.replace("/", "")
        # Use pandas to access data from CSV
        df1 = pd.read_csv(source_file, encoding='utf-8')
        search_text = request.form['search']
        df2 = df1[df1.short_description.str.contains(search_text, case=False)]
        df2 = df2.head(snoa)
        # posts = df2.to_dict()
        df2.to_csv(temp_file, index=False, encoding='utf-8')

        # Use DictReader to access data from CSV
        f = open(temp_file, newline='', encoding="utf-8")
        posts = csv.DictReader(f)

        return render_template('EV_article.html',
                               title='Search ' + source_search,
                               posts=posts,
                               outlet_page="/" + source_search)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
