# import time
import csv
from jinja2 import Template
import webbrowser

# time.sleep(10)

source_file = "insideevs_articles.csv"
test_jinja_template_file = "Test_Jinja2_template.j2"

# String that will hold final full configuration of all interfaces
ev_news_articles = """
<!doctype html>
<html class="no-js" lang="">
    <head>
        <title>EV articles</title>
        <meta charset="utf-8">

        <link rel="stylesheet" type="text/css" href="main.css">
    </head>
    <body>
        <h1 id='site_title'>EV News</h1>
        <hr></hr>
"""

# Open up the Jinja templates file (as text) and then create a Jinja Template Object
with open(test_jinja_template_file) as f:
    test_jinja_template = Template(f.read(), keep_trailing_newline=True)

# Open up the CSV file containing the data
with open(source_file, newline='', encoding="utf-8") as f:
    # Use DictReader to access data from CSV
    reader = csv.DictReader(f)

    # For each row in the CSV, generate an interface configuration using the jinja templates
    for row in reader:
        test_jinja_article = test_jinja_template.render(
            image=row["image"],
            article_link=row["article_link"],
            title=row["title"],
            date=row["date"],
            short_description=row["short_description"],
            byline=row["byline"],
            alt=row["alt"],
            outlet=row["outlet"]
        )

        # Append this interface configuration to the full configuration
        ev_news_articles += test_jinja_article

article_foot = """

        <div class='footer'>
            <p>Footer Information</p>
        </div>

    </body>
</html>

"""

ev_news_articles += article_foot

# Save the final configuration to a file
with open("ev_news_articles.html", "w") as f:
    f.write(ev_news_articles)

webbrowser.open(r'http://localhost:63342/Beautiful_Soup/ev_news_articles.html', new=2)
