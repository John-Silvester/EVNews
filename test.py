import pandas as pd

site_name = "teslarati"
sitetitles_file = "sitetitles.csv"
df1 = pd.read_csv(sitetitles_file, encoding='utf-8')
df1 = df1[df1.site.str.contains(site_name, case=False)]

print(df1)
title = df1['title']
title = title.to_string(index=False).strip()
outlet_page = "/" + df1['site']
outlet_page = outlet_page.to_string(index=False).strip()
source_file = df1['site'] + '_articles.csv'
source_file = source_file.to_string(index=False).strip()
df2 = pd.read_csv(source_file)
df2 = df2.head(5)
print(title)
print(outlet_page)
print(source_file)
print(df2)
