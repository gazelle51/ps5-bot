import logging
import logging.config

# Load logger
logging.config.fileConfig('./src/logger.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def add_to_cart(wd):
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
        '//*[@class="ProductCartAndWishlist"]/div[@class="button-group"]/button[@class="Button variant-primary size-normal"]|'
        '//*[@class="ProductAddToCart"]/button[@class="Button variant-primary size-normal"]')

    # Press button
    if len(add_to_cart_button) == 1 and add_to_cart_button[0].text.lower() == 'add to cart':
        logger.info('Adding item to cart')
        add_to_cart_button[0].click()

        # Wait for item to successfully add to cart
        wd.find_element_by_xpath(
            '//*[@class="ProductAddToCart"]//button[@class="Button variant-primary size-normal decrement"]')

        return True

    # No button
    elif len(add_to_cart_button) == 0:
        logger.warn('No "Add to cart" button found')

    # Multiple buttons
    else:
        logger.warn('Multiple "Add to cart" buttons found')

    logger.error('Could not add item to cart')
    return False
