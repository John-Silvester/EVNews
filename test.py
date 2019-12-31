import csv
import pandas as pd

# set number of article (snoa)
snoa = 7
source_file = "/home/john/PycharmProjects/EVNews/electrek_articles.csv"
temp_file = "/home/john/PycharmProjects/EVNews/temp_articles.csv"
# Use pandas to access data from CSV
df1 = pd.read_csv(source_file, encoding='utf-8')
# df2 = df1.head(snoa)
df2 = df1[df1.short_description.str.contains('porsche', case=False)]
# posts = df2.to_dict()
df2.to_csv(temp_file, index=False, encoding='utf-8')

# Use DictReader to access data from CSV
f = open(temp_file, newline='', encoding="utf-8")
posts = csv.DictReader(f)

# total_rows = df2.values.tolist()
# total_rows = len(total_rows)

for post in posts:
    print(post['date'], post['title'])
