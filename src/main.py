
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import chromedriver_binary
import os
import time

from bigw.cart import add_to_cart
from bigw.checkout import proceed_to_checkout

load_dotenv()

PROFILE_NAME = os.environ.get('PROFILE_NAME')

# PS5 Consoles Pages
PS5_URLS = [
    'https://www.bigw.com.au/product/razer-wolverine-v2-controller-xbox/p/133727/',  # Online only in stock,
    # 'https://www.bigw.com.au/product/playstation-5-console/p/124625/',  # PlayStation 5 Console
    # 'https://www.bigw.com.au/product/nintendo-switch-lite-turquoise/p/58260/'  # Special
]

CART_URL = 'https://www.bigw.com.au/cart'

# Create images folder
if not os.path.exists('images'):
    os.makedirs('images')

# Set Chrome options
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--user-data-dir=./Chrome')
options.add_argument('--profile-directory=' + PROFILE_NAME)
# options.add_argument('--headless')

# Open Chrome
wd = webdriver.Chrome(options=options)

# Add PS5 to cart
item_in_cart = False
for URL in PS5_URLS:
    print('Checking {}'.format(URL))

    # Navigate to URL
    wd.get(URL)
    wd.save_screenshot('images/ps5.png')

    # Add to cart if available
    add_to_cart_result = add_to_cart(wd)
    if not add_to_cart_result:
        continue
    time.sleep(0.5)

    # Stop looping if we successfully were able to add to cart
    item_in_cart = True
    break

if not item_in_cart:
    print('No items in stock, stopping')
    exit()

# Go to cart
wd.get(CART_URL)
wd.save_screenshot('images/cart.png')

# Proceed to checkout
proceed_to_checkout_result = proceed_to_checkout(wd)
wd.save_screenshot('images/checkout.png')
if not proceed_to_checkout_result:
    exit()

# wd.close()
# wd.quit()
