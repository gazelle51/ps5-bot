from bs4 import BeautifulSoup
from selenium import webdriver as wd
import chromedriver_binary
import pandas as pd
import requests

URL = 'https://www.newegg.com/global/au-en/p/pl?N=100203018%20601357248'

# # Open Chrome and navigate to URL
# wd = wd.Chrome()
# wd.get(URL)
# wd.set_window_size(1920, 1080)
# wd.save_screenshot('screenshot.png')

# Initialise beautiful soup
page = requests.get(URL)
soup = BeautifulSoup(page.content, features='html.parser')

# # Close Chrome
# wd.close()

# Find results div
items = soup.find('div', {'class': 'items-grid-view'})

# Find all result items
print(str(len(items.findAll('div', {'class': 'item-cell'})))+' items found')
rows = []
for item in items.findAll('div', {'class': 'item-cell'}):
    # Item title
    item_title = item.find('a', {'class': 'item-title'})

    # Out of stock message
    item_promo = item.find('p', {'class': 'item-promo'})
    item_promo_text = item_promo.text if item_promo else 'AVAILABLE'

    row = [item_title.text, item_promo_text]
    rows.append(row)

# Load data into Pandas
df = pd.DataFrame.from_records(rows, columns=['Item Title', 'Status'])

# Check if any of the items are in stock
isAvailable = 'AVAILABLE' in df['Status'].values
