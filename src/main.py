from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv
from selenium import webdriver
import argparse
import chromedriver_binary
import logging
import logging.config
import os
import time

from bigw.cart import add_to_cart
from bigw.checkout import proceed_to_checkout
from bigw.order_confirmation import get_order_data
from bigw.payment import enter_cvv_saved_credit_card, pay_with_credit_card, proceed_to_payment, redeem_rewards_points, select_payment_method

# Load environment variables
load_dotenv()

# Load logger
logging.config.fileConfig('./src/logger.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

# Load arguments
parser = argparse.ArgumentParser(description='Check for a PS5 in stock at Big W and buy it if it\'s in stock.')
parser.add_argument('--test', dest='test_mode', action='store_const', const=True, default=False,
                    help='run in test mode (default: do not run in test mode)')
args = parser.parse_args()

# Constants
CVV = os.environ.get('CVV')
PROFILE_NAME = os.environ.get('PROFILE_NAME')
PS5_URLS = [
    'https://www.bigw.com.au/product/playstation-5-console/p/124625/',  # PlayStation 5 Console
] if not args.test_mode else [
    'https://www.bigw.com.au/product/razer-wolverine-v2-controller-xbox/p/133727/',  # Online only in stock
    # 'https://www.bigw.com.au/product/nintendo-switch-lite-turquoise/p/58260/'  # Special
]
CART_URL = 'https://www.bigw.com.au/cart'

# Create output folder
if not os.path.exists('output'):
    os.makedirs('output')

# Set Chrome options
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--user-data-dir=./Chrome')
options.add_argument('--profile-directory=' + PROFILE_NAME)
# options.add_argument('--headless')

# Open Chrome
wd = webdriver.Chrome(options=options)
wd.maximize_window()
wd.implicitly_wait(10)

try:
    # Add PS5 to cart
    item_in_cart = False
    for URL in PS5_URLS:
        logger.info('Checking {}'.format(URL))

        # Navigate to URL
        wd.get(URL)
        wd.save_screenshot('output/{}_ps5.png'.format(datetime.now().strftime('%Y%m%d_%H%M%S')))

        # Add to cart if available
        add_to_cart_result = add_to_cart(wd)
        if not add_to_cart_result:
            continue
        # TODO: replace explicit wait with waiting for spinner to go
        time.sleep(1)

        # Stop looping if we successfully were able to add to cart
        item_in_cart = True
        break

    if not item_in_cart:
        logger.info('No items in stock, stopping')
        exit()

    # Go to cart
    wd.get(CART_URL)
    wd.save_screenshot('output/{}_cart.png'.format(datetime.now().strftime('%Y%m%d_%H%M%S')))

    # Proceed to checkout
    proceed_to_checkout_result = proceed_to_checkout(wd)
    wd.save_screenshot('output/{}_checkout.png'.format(datetime.now().strftime('%Y%m%d_%H%M%S')))
    if not proceed_to_checkout_result:
        # TODO: error
        exit()

    # Proceed to payment
    proceed_to_payment_result = proceed_to_payment(wd)
    wd.save_screenshot('output/{}_payment.png'.format(datetime.now().strftime('%Y%m%d_%H%M%S')))
    if not proceed_to_payment_result:
        exit()

    # Redeem rewards points
    redeem_rewards_points_result = redeem_rewards_points(wd, args.test_mode)
    wd.save_screenshot('output/{}_redeem_rewards.png'.format(datetime.now().strftime('%Y%m%d_%H%M%S')))
    if not redeem_rewards_points_result:
        exit()

    # Select payment method
    select_payment_method_result = select_payment_method(wd, 'credit card')
    wd.save_screenshot('output/{}_payment_method.png'.format(datetime.now().strftime('%Y%m%d_%H%M%S')))
    if not select_payment_method_result:
        exit()

    # Enter CVV
    enter_cvv_saved_credit_card_result = enter_cvv_saved_credit_card(wd, CVV)
    wd.save_screenshot('output/{}_cvv.png'.format(datetime.now().strftime('%Y%m%d_%H%M%S')))
    if not enter_cvv_saved_credit_card_result:
        exit()

    # If not test mode
    if not args.test_mode:
        # Pay with credit card
        pay_with_credit_card_result = pay_with_credit_card(wd)
        wd.save_screenshot('output/{}_pay_with_credit_card.png'.format(datetime.now().strftime('%Y%m%d_%H%M%S')))
        if not pay_with_credit_card_result:
            exit()

        # Wait for order confirmation
        wd.find_elements_by_xpath('//div[@class="page-content"]//table')
        wd.save_screenshot('output/{}_order_confirmation.png'.format(datetime.now().strftime('%Y%m%d_%H%M%S')))

        # Load order confirmation into Beautiful Soup
        soup = BeautifulSoup(wd.page_source)

    # If test mode
    else:
        logger.info('Skipped payment, loading dummy order confirmation')

        # Load order confirmation into Beautiful Soup
        soup = BeautifulSoup(open('./src/bigw/order_confirmation.html', encoding="utf8"), "html.parser")

    # Set up order data
    order_data = get_order_data(soup)

    # Save to file
    with open('output/{}_order_data.txt'.format(datetime.now().strftime('%Y%m%d_%H%M%S')), 'w') as f:
        f.write(order_data)

    wd.save_screenshot('output/{}_finished.png'.format(datetime.now().strftime('%Y%m%d_%H%M%S')))

    # Quit Chrome
    wd.close()
    wd.quit()

except Exception as e:
    logger.exception(e)
    wd.save_screenshot('output/{}_error.png'.format(datetime.now().strftime('%Y%m%d_%H%M%S')))
    # TODO: save HTML
    wd.close()
    wd.quit()
    raise e
