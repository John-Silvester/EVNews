import pandas as pd

site_name = "carsales"
sitetitles_file = "siteaddresses.csv"
pd.options.display.max_colwidth = 120
df1 = pd.read_csv(sitetitles_file, encoding='utf-8')
df1 = df1[df1.site.str.contains(site_name, case=False)]

title = df1['title']
title = title.to_string(index=False).strip()
outlet_page = "/web/" + df1['site']
outlet_page = outlet_page.to_string(index=False).strip()
web_address = df1['web_address']
web_address = web_address.to_string(index=False).strip()

print(title)
print(outlet_page)
print(web_address)
