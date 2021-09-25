from bs4 import BeautifulSoup
import pandas as pd
import requests

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
           "Upgrade-Insecure-Requests": "1",
           "DNT": "1",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}


def search_ps5_availability(search_urls):
    '''
    Check provided search result URLs to see is a PlayStation 5 is in stock.

    :param List<string> search_urls: URLs of search results to check, https://www.bigw.com.au/gaming/ps5/ps5-consoles/c/64121178100/'.
    :return: void
    :rtype: void
    '''

    df_rows = []

    for URL in search_urls:
        print('Getting data from {}'.format(URL))

        # Initialise beautiful soup
        page = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(page.content, features='html.parser')

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
