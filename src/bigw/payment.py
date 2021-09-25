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
