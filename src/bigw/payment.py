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
        print('Proceeding to payment')
        # wd.execute_script("arguments[0].scrollIntoView();", proceed_to_payment_button[0])
        wd.execute_script('arguments[0].click();', proceed_to_payment_button[0])
        return True

    # No button
    elif len(proceed_to_payment_button) == 0:
        print('No "Proceed to payment" button found')

    # Multiple buttons
    else:
        print('Multiple "Proceed to payment" buttons found')

    print('Could not go to payment')
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
        print('Selecting payment method "{}"'.format(payment_type))
        payment_method_radio[0].click()
        return True

    # No radio button
    elif len(payment_method_radio) == 0:
        print('No "{}" payment method radio button found'.format(payment_type))

    # Multiple radio buttons
    else:
        print('Multiple "{}" payment method radio buttons found'.format(payment_type))

    print('Could not select a payment method')
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
        print('Entering CVV')
        cvv_input_box[0].send_keys(cvv)
        return True

    # No input box
    elif len(cvv_input_box) == 0:
        print('No CVV input box found')

    # Multiple input boxes
    else:
        print('Multiple CVV input boxes found')

    print('Could not enter CVV number')
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
        print('Paying with credit card')
        pay_with_credit_card_button[0].click()
        return True

    # No button
    elif len(pay_with_credit_card_button) == 0:
        print('No "Pay with Credit Card" button found')

    # Multiple buttons
    else:
        print('Multiple "Pay with Credit Card" buttons found')

    print('Could not pay with credit card')
    return False
