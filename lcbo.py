import re
import requests
import yaml
import html
from bs4 import BeautifulSoup

product_id = 390003
#product_id = 57548

url = f'https://www.lcbo.com/webapp/wcs/stores/servlet/PhysicalStoreInventoryView?langId=-1&storeId=10203&catalogId=10051&productId={product_id}'

page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(page.content, "html.parser")
title = soup.find("div", {'class': 'namePartPriceContainer'}).find("a").text

print("Title:", title)

data = soup.findAll("script")[-1].string
data = ''.join(c for c in data if c == ' ' or not c.isspace())

data = html.unescape(data)

m = re.search(r"storesArray = (.*?);", data)
stores = yaml.safe_load(re.sub(r'(?<={|,)([a-zA-Z][a-zA-Z0-9]*)(?=:)', r'"\1"', m.groups()[0]))

#'city': 'WATERLOO', 'description': 'COLUMBIA & FISCHER HALLMAN (LAURELWOOD)', 'address1': '450 COLUMBIA ST WEST', 'address2': '', 'phone': '(519) 886-1559                  ', 'uniqueId': '715841918', 'inventory': 'Math.floor("65.0")'}
found = False
for store in stores:
    if store["city"].lower() in ("waterloo", "kitchener"):
        found = True
        print("City:", store["city"])
        print("Location:", store["description"])

        print("Quantity:", re.search(r"\d+", store["inventory"])[0])
        print("")

if not found:
    print("None")
