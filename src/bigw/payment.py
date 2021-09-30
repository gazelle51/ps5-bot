import logging
import logging.config

# Load logger
logging.config.fileConfig('./src/logger.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def proceed_to_payment(wd):
    '''
    Press the 'Proceed to payment' button if possible.
    Returns 'True' if the button was successfully pressed.
    Returns 'False' otherwise (e.g., button was not found).

    :param WebDriver wd: Selenium webdriver with page loaded.
    :return: true if successful, otherwise false
    :rtype: boolean
    '''

    # Find proceed to payment button
    proceed_to_payment_button = wd.find_elements_by_xpath(
        '//div[@class="proceed-button"]/button[@class="Button variant-primary size-normal" and not(@disabled)]')

    # Press button
    if len(proceed_to_payment_button) == 1:
        logger.info('Proceeding to payment')
        wd.execute_script('arguments[0].click();', proceed_to_payment_button[0])
        return True

    # No button
    elif len(proceed_to_payment_button) == 0:
        logger.warn('No "Proceed to payment" button found')

    # Multiple buttons
    else:
        logger.warn('Multiple "Proceed to payment" buttons found')

    logger.error('Could not go to payment')
    return False


def redeem_rewards_points(wd, test_mode):
    '''
    Redeem Rewards points if possible.
    Returns 'True' if the action was successful.
    Returns 'False' otherwise (e.g., button was not found).

    :param WebDriver wd: Selenium webdriver with page loaded.
    :param boolean test_mode: whether to run in test mode or not, if True the "Redeem" button won't be pressed.
    :return: true if successful, otherwise false
    :rtype: boolean
    '''

    # Find Rewards payment section
    rewards_payment_section = wd.find_element_by_xpath('//div[@class="RewardsPaymentOption"]')

    # --- Expand Rewards section

    # Find Rewards plus button
    rewards_plus_button = rewards_payment_section.find_elements_by_xpath(
        './/*[local-name() ="svg" and @data-src="/static/icons/plus.svg"]')

    # Press button
    if len(rewards_plus_button) == 1:
        logger.info('Expanding Rewards section')
        rewards_plus_button[0].click()

    else:
        # No button
        if len(rewards_plus_button) == 0:
            logger.warn('No Rewards plus button found')

        # Multiple buttons
        else:
            logger.warn('Multiple Rewards plus buttons found')

        logger.error('Could not redeem Rewards points')
        return False

    # --- Redeem button

    # Find "Redeem" button
    redeem_button = rewards_payment_section.find_elements_by_xpath(
        './/button[@type="submit" and @class="Button variant-primary size-normal submit-button"]')

    # Press button (if not in test mode)
    if len(redeem_button) == 1:
        logger.info('Redeeming Rewards points')
        if not test_mode:
            wd.execute_script('arguments[0].click();', redeem_button[0])
        return True

    # No button
    elif len(redeem_button) == 0:
        logger.warn('No "Redeem" button found')

    # Multiple buttons
    else:
        logger.warn('Multiple "Redeem" buttons found')

    logger.error('Could not redeem Rewards points')
    return False


def select_payment_method(wd, payment_type):
    '''
    Select the provided payment method radio button.
    Returns 'True' if the button was successfully pressed.
    Returns 'False' otherwise (e.g., button was not found).

    :param WebDriver wd: Selenium webdriver with page loaded.
    :param string payment_type: Payment method to select.
    :return: true if successful, otherwise false
    :rtype: boolean
    '''

    # Find payment method radio button
    payment_method_radio = wd.find_elements_by_xpath(
        '//div[@class="PaymentOptions"]/section/div[@class="PaymentOption"]/header/section'
        '[p[translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz") = "{}"]]'
        '/input'.format(payment_type.lower()))

    # Press radio button
    if len(payment_method_radio) == 1:
        logger.info('Selecting payment method "{}"'.format(payment_type))
        wd.execute_script('arguments[0].click();', payment_method_radio[0])
        return True

    # No radio button
    elif len(payment_method_radio) == 0:
        logger.warn('No "{}" payment method radio button found'.format(payment_type))

    # Multiple radio buttons
    else:
        logger.warn('Multiple "{}" payment method radio buttons found'.format(payment_type))

    logger.error('Could not select a payment method')
    return False


def enter_cvv_saved_credit_card(wd, cvv):
    '''
    Enter the CVV for a saved credit card.
    Returns 'True' if the button was successfully pressed.
    Returns 'False' otherwise (e.g., button was not found).

    :param WebDriver wd: Selenium webdriver with page loaded.
    :param string cvv: CVV number.
    :return: true if successful, otherwise false
    :rtype: boolean
    '''

    # Find CVV input box
    cvv_input_box = wd.find_elements_by_id('saved-cards__cv2')

    # Enter text
    if len(cvv_input_box) == 1:
        logger.info('Entering CVV')
        wd.execute_script("arguments[0].scrollIntoView();", cvv_input_box[0])
        cvv_input_box[0].send_keys(cvv)
        return True

    # No input box
    elif len(cvv_input_box) == 0:
        logger.warn('No CVV input box found')

    # Multiple input boxes
    else:
        logger.warn('Multiple CVV input boxes found')

    logger.error('Could not enter CVV number')
    return False


def pay_with_credit_card(wd):
    '''
    Press the 'Pay with Credit Card' button if possible.
    Note that the credit card must be saved to the account.
    Returns 'True' if the button was successfully pressed.
    Returns 'False' otherwise (e.g., button was not found).

    :param WebDriver wd: Selenium webdriver with page loaded.
    :return: true if successful, otherwise false
    :rtype: boolean
    '''

    # Find 'Pay with Credit Card' button
    pay_with_credit_card_button = wd.find_elements_by_xpath(
        '//form[@id="saved-cards"]/div[@class="action-wrapper"]/button[@class="Button variant-primary size-normal"]')

    # Press button
    if len(pay_with_credit_card_button) == 1:
        logger.info('Paying with credit card')
        wd.execute_script('arguments[0].click();', pay_with_credit_card_button[0])
        return True

    # No button
    elif len(pay_with_credit_card_button) == 0:
        logger.warn('No "Pay with Credit Card" button found')

    # Multiple buttons
    else:
        logger.warn('Multiple "Pay with Credit Card" buttons found')

    logger.error('Could not pay with credit card')
    return False
