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

    # Press button
    if len(payment_method_radio) == 1:
        print('Selecting payment method "{}"'.format(payment_type))
        payment_method_radio[0].click()
        return True

    # No button
    elif len(payment_method_radio) == 0:
        print('No "{}" payment method radio button found'.format(payment_type))

    # Multiple buttons
    else:
        print('Multiple "{}" payment method radio buttons found'.format(payment_type))

    print('Could not select a payment method')
    return False
