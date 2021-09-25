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
        '//*[@class="ProductCartAndWishlist"]/div[@class="button-group"]/button[@class="Button variant-primary size-normal"]')

    # Check button exists
    if len(add_to_cart_button) == 1 and add_to_cart_button[0].text.lower() == 'add to cart':
        # Press button
        print('Adding to cart')
        add_to_cart_button[0].click()

        return True

    # Find alternative add to cart button
    add_to_cart_button_2 = wd.find_elements_by_xpath(
        '//*[@class="ProductAddToCart"]/button[@class="Button variant-primary size-normal"]')

    # Check button exists
    if len(add_to_cart_button_2) == 1 and add_to_cart_button_2[0].text.lower() == 'add to cart':
        # Press button
        print('Adding to cart')
        add_to_cart_button_2[0].click()

        return True

    # Button was not found
    print('Not available')
    return False
