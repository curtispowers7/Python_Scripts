#This tutorial was created by someone else and I followed along to learn the basics of BeautifulSoup

# importing the libraries
from bs4 import BeautifulSoup
import requests

url="https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"

# Make a GET request to fetch the raw HTML content
html_content = requests.get(url).text

# Parse the html content
soup = BeautifulSoup(html_content, "lxml")
print(soup.prettify()) # print the parsed data of html

gdp_table = soup.find("table", attrs={"class": "wikitable"})
gdp_table_data = gdp_table.tbody.find_all("tr")

headings = []
for td in gdp_table_data[0].find_all("td"):
    headings.append(td.b.text.replace('\n', ' ').strip())
    
data = {}
for table, heading in zip(gdp_table_data[1].find_all("table"), headings):
    t_headers = []
    for th in table.find_all("th"):
        t_headers.append(th.text.replace('\n', ' ').strip())
    
    table_data = []
    for tr in table.tbody.find_all("tr"):
        t_row = {}
        for td, th in zip(tr.find_all("td"), t_headers):
            t_row[th] = td.text.replace('\n', '').strip()
        table_data.append(t_row)
    
    data[heading] = table_data
