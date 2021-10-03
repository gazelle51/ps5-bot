import logging
import logging.config

# Load logger
logging.config.fileConfig('./src/logger.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def proceed_to_checkout(wd):
    '''
    Press the 'Proceed to checkout' button if possible.
    Returns 'True' if the button was successfully pressed.
    Returns 'False' otherwise (e.g., button was not found).

    :param WebDriver wd: Selenium webdriver with page loaded.
    :return: true if successful, otherwise false
    :rtype: boolean
    '''

    # Find proceed to checkout button
    proceed_to_checkout_button = wd.find_elements_by_xpath(
        '//div[@class="cart-summary-buttons"]/button[@class="Button variant-primary size-normal"]')

    # Press button
    if len(proceed_to_checkout_button) == 1:
        logger.info('Proceeding to checkout')
        wd.execute_script('arguments[0].click();', proceed_to_checkout_button[0])
        return True

    # No button
    elif len(proceed_to_checkout_button) == 0:
        logger.warn('No "Proceed to checkout" button found')

    # Multiple buttons
    else:
        logger.warn('Multiple "Proceed to checkout" buttons found')

    return False
