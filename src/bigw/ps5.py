from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
import chromedriver_binary
import logging
import logging.config
import os

from bigw.cart import add_to_cart
from bigw.checkout import proceed_to_checkout
from bigw.order_confirmation import get_order_data
from bigw.payment import enter_cvv_saved_credit_card, pay_with_credit_card, proceed_to_payment, redeem_rewards_points, select_payment_method

# Load logger
logging.config.fileConfig('./src/logger.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def find_and_buy_ps5(test_mode):
    '''
    Check for a PS5 in stock at Big W and attempt to buy it.
    If run in test mode, the PS5 will not actually be bought but the process will be simulated.

    :param boolean test_mode: whether the function should be run in test mode or not.
    :return: true if PS5 was bought successfully, otherwise false
    :rtype: boolean
    '''

    # Whether PS5 buy was successful or not
    success_flag = False

    # Constants
    CVV = os.environ.get('CVV')
    PROFILE_NAME = os.environ.get('PROFILE_NAME')
    PS5_URLS = [
        'https://www.bigw.com.au/product/playstation-5-console/p/124625/',  # PlayStation 5 Console
    ] if not test_mode else [
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

            # Stop looping if we successfully were able to add to cart
            item_in_cart = True
            break

        if not item_in_cart:
            logger.info('No items in stock, stopping')

            # Quit Chrome
            wd.close()
            wd.quit()

            # PS5 was not bought so stop
            return success_flag

        # Go to cart
        wd.get(CART_URL)
        wd.save_screenshot('output/{}_cart.png'.format(datetime.now().strftime('%Y%m%d_%H%M%S')))

        # Proceed to checkout
        proceed_to_checkout_result = proceed_to_checkout(wd)
        wd.save_screenshot('output/{}_checkout.png'.format(datetime.now().strftime('%Y%m%d_%H%M%S')))
        if not proceed_to_checkout_result:
            raise Exception('Could not go to checkout')

        # Proceed to payment
        proceed_to_payment_result = proceed_to_payment(wd)
        wd.save_screenshot('output/{}_payment.png'.format(datetime.now().strftime('%Y%m%d_%H%M%S')))
        if not proceed_to_payment_result:
            raise Exception('Could not go to payment')

        # Redeem rewards points
        redeem_rewards_points_result = redeem_rewards_points(wd, test_mode)
        wd.save_screenshot('output/{}_redeem_rewards.png'.format(datetime.now().strftime('%Y%m%d_%H%M%S')))
        if not redeem_rewards_points_result:
            raise Exception('Could not redeem Rewards points')

        # Select payment method
        select_payment_method_result = select_payment_method(wd, 'credit card')
        wd.save_screenshot('output/{}_payment_method.png'.format(datetime.now().strftime('%Y%m%d_%H%M%S')))
        if not select_payment_method_result:
            raise Exception('Could not select a payment method')

        # Enter CVV
        enter_cvv_saved_credit_card_result = enter_cvv_saved_credit_card(wd, CVV)
        wd.save_screenshot('output/{}_cvv.png'.format(datetime.now().strftime('%Y%m%d_%H%M%S')))
        if not enter_cvv_saved_credit_card_result:
            raise Exception('Could not enter CVV number')

        # If not test mode
        if not test_mode:
            # Pay with credit card
            pay_with_credit_card_result = pay_with_credit_card(wd)
            wd.save_screenshot('output/{}_pay_with_credit_card.png'.format(datetime.now().strftime('%Y%m%d_%H%M%S')))
            if not pay_with_credit_card_result:
                raise Exception('Could not pay with credit card')

            # Wait for order confirmation
            wd.find_elements_by_xpath('//div[@class="page-content"]//table')
            wd.save_screenshot('output/{}_order_confirmation.png'.format(datetime.now().strftime('%Y%m%d_%H%M%S')))

            # PS5 was bought
            success_flag = True
            logger.info('Order is confirmed')

            # Load order confirmation into Beautiful Soup
            soup = BeautifulSoup(wd.page_source)

        # If test mode
        else:
            logger.info('Skipped payment, loading dummy order confirmation')

            # PS5 was bought
            success_flag = True
            logger.info('Order is confirmed')

            # Load order confirmation into Beautiful Soup
            soup = BeautifulSoup(open('./src/bigw/order_confirmation.html', encoding="utf8"), "html.parser")

        # Set up order data
        order_data = get_order_data(soup)

        # Save to file
        order_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
        with open('output/{}_order_data.txt'.format(order_datetime), 'w') as f:
            f.write(order_data)
        logger.info('Order details saved to {}_order_data.txt'.format(order_datetime))

        wd.save_screenshot('output/{}_finished.png'.format(datetime.now().strftime('%Y%m%d_%H%M%S')))

        # Quit Chrome
        wd.close()
        wd.quit()

        return success_flag

    except Exception as e:
        logger.exception(e)

        # Save error
        wd.save_screenshot('output/{}_error.png'.format(datetime.now().strftime('%Y%m%d_%H%M%S')))
        with open('output/{}_error.html'.format(datetime.now().strftime('%Y%m%d_%H%M%S')), 'w') as f:
            f.write(wd.page_source)

        # Quit Chrome
        wd.close()
        wd.quit()

        return success_flag
