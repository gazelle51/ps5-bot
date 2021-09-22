from bs4 import BeautifulSoup
import pandas as pd
import requests

# PS5 Consoles Search Results
URLS = [
    'https://www.bigw.com.au/gaming/ps5/ps5-consoles/c/64121178100/',  # PS5 search results
    'https://www.bigw.com.au/search?text=console'  # Console search results
]
#       'https://www.bigw.com.au/product/playstation-5-console/p/124625/',  # Coming soon
#       'https://www.bigw.com.au/product/playstation-5-digital-edition-console/p/124626/',  # Coming soon
#       'https://www.bigw.com.au/product/nintendo-switch-lite-dialga-palkia-edition/p/182759/',  # Pre order
#       'https://www.bigw.com.au/product/nintendo-switch-lite-turquoise/p/58260/'  # Special
#       'https://www.bigw.com.au/product/xbox-series-s-512gb-console/p/124384/' # Normal


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
           "Upgrade-Insecure-Requests": "1",
           "DNT": "1",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}
df_rows = []

for URL in URLS:
    print(URL)

    # Initialise beautiful soup
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, features='html.parser')

    print('Loaded into bs4')

    # Find result PS5 products
    products = soup.find('div', {'class': 'results-pane'}) \
        .findChild('div', {'class': 'results'}) \
        .findChildren('a', {'class': 'ProductTile2', 'aria-label': lambda x: x and 'PlayStation 5' in x})

    # Extract data about each product
    for product in products:
        # Product
        product_name = product['aria-label']

        # URL
        product_url = product['href']

        # Label
        product_label = product.find('div', {'class': 'ProductLabel'})

        # Price
        product_price = product.find('div', {'class': 'PriceSection'})

        df_rows.append(['Big W',
                        product_name,
                        'https://www.bigw.com.au' + product_url,
                        product_label.text.lower() if product_label else None,
                        product_price.text if product_price else None])

# Load data into Pandas
df = pd.DataFrame.from_records(df_rows, columns=['Store', 'Product', 'URL', 'Status', 'Price'])
print(df)

# Check if any product is available
isAvailable = any(x in df['Status'].values for x in [None, 'special'])

print(isAvailable)
