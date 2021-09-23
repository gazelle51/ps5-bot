from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import chromedriver_binary
import os
import pandas as pd
import requests
import time

load_dotenv()

USER_DATA_DIR = os.environ.get('USER_DATA_DIR')
PROFILE_NAME = os.environ.get('PROFILE_NAME')
POSTCODE = os.environ.get('POSTCODE')

# PS5 Consoles Search Results
SEARCH_URLS = [
    'https://www.bigw.com.au/gaming/ps5/ps5-consoles/c/64121178100/',  # PS5 consoles
]

# PS5 Consoles Pages
PS5_URLS = [
    'https://www.bigw.com.au/product/razer-wolverine-v2-controller-xbox/p/133727/',  # Online only in stock,
    # 'https://www.bigw.com.au/product/playstation-5-console/p/124625/',  # PlayStation 5 Console
    # 'https://www.bigw.com.au/product/nintendo-switch-lite-turquoise/p/58260/'  # Special
]

CART_URL = 'https://www.bigw.com.au/cart'
CHECKOUT_URL = 'https://www.bigw.com.au/checkout/delivery'

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--user-data-dir='+USER_DATA_DIR)
options.add_argument('--profile-directory=Profile 2')
# options.add_argument('--headless')

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
           "Upgrade-Insecure-Requests": "1",
           "DNT": "1",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}


def _close_catalogue_pop_up(wd):
    '''
    Close catalogue pop up box if it appears.

    :param WebDriver wd: Selenium webdriver with page loaded.
    :return: void
    :rtype: void
    '''

    pop_up_buttons = wd.find_elements_by_css_selector('.Button.variant-plain.size-normal.close-control')

    for button in pop_up_buttons:
        button.click()


def _add_to_cart(wd):
    '''
    Press the 'Add to cart' button if possible.
    Returns 'True' if the button was successfully pressed.
    Returns 'False' otherwise (e.g., button was not found).

    :param WebDriver wd: Selenium webdriver with page loaded.
    :return: true if successful, otherwise false
    :rtype: boolean
    '''

    # Find add to cart button
    add_to_cart_button = wd.find_elements_by_xpath(
        '//*[@class="ProductCartAndWishlist"]/div[@class="button-group"]/button[@class="Button variant-primary size-normal"]')

    # Check button exists
    if len(add_to_cart_button) == 1 and add_to_cart_button[0].text.lower() == 'add to cart':
        # Press button
        print('Adding to cart')
        add_to_cart_button[0].click()

        return True

    # Find alternative add to cart button
    add_to_cart_button_2 = wd.find_elements_by_xpath(
        '//*[@class="ProductAddToCart"]/button[@class="Button variant-primary size-normal"]')

    # Check button exists
    if len(add_to_cart_button_2) == 1 and add_to_cart_button_2[0].text.lower() == 'add to cart':
        # Press button
        print('Adding to cart')
        add_to_cart_button_2[0].click()

        return True

    # Button was not found
    print('Not available')
    return False


# Commented out code to analyse search results as we only care about one product
if False:
    df_rows = []
    for URL in SEARCH_URLS:
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


# Open Chrome
wd = webdriver.Chrome(options=options)

# Add PS5 to cart
for URL in PS5_URLS:
    print('Checking {}'.format(URL))

    # Navigate to URL
    wd.get(URL)
    wd.save_screenshot('ps5.png')

    # Add to cart if available
    add_to_cart_result = _add_to_cart(wd)
    if not add_to_cart_result:
        continue

    # Check if postcode needs to be set
    postcode_input = wd.find_elements_by_id('react-select-2-input')

    if len(postcode_input) == 1:
        # Enter postcode
        postcode_input[0].send_keys(POSTCODE)
        time.sleep(1)
        postcode_input[0].send_keys(Keys.ENTER)
        time.sleep(1)

        # Save postcode
        save_button = wd.find_element_by_css_selector('.Button.variant-primary.size-normal.save-button')
        save_button.click()

        # Add to cart
        add_to_cart_result_2 = _add_to_cart(wd)
        if not add_to_cart_result_2:
            continue

    # Stop looping if we successfully added to cart
    break

# Go to checkout
wd.get(CHECKOUT_URL)
wd.save_screenshot('checkout.png')

# wd.close()
# wd.quit()
