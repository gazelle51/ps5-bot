def close_catalogue_pop_up(wd):
    '''
    Close catalogue pop up box if it appears.

    :param WebDriver wd: Selenium webdriver with page loaded.
    :return: void
    :rtype: void
    '''

    pop_up_buttons = wd.find_elements_by_css_selector('.Button.variant-plain.size-normal.close-control')

    for button in pop_up_buttons:
        button.click()
