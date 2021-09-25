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
        print('Proceeding to checkout')
        proceed_to_checkout_button[0].click()
        return True

    # No button
    elif len(proceed_to_checkout_button) == 0:
        print('No "Proceed to checkout" button found')

    # Multiple buttons
    else:
        print('Multiple "Proceed to checkout" buttons found')

    print('Could not go to checkout')
    return False
