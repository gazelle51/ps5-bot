# Auto buy an item
# Script built from tutorial at https://spltech.co.uk/how-to-make-a-python-bot/
#
# xpath is a lazy method as if the website changes any HTML it will no longer work
# Better to try and find things using classes and IDs
#
# Can get blocked if these steps are executed very quickly so implement wait periods
# Randomised timers are best

from selenium import webdriver as wd
import chromedriver_binary
import time

URL = 'https://www.newegg.com/global/au-en/asus-geforce-rtx-3090-rog-strix-rtx3090-o24g-white/p/N82E16814126482?Description=rtx%203090&cm_re=rtx_3090-_-9SIAYB7FRF8536-_-Product&quicklink=true'

# Open Chrome and navigate to URL
wd = wd.Chrome()
wd.implicitly_wait(10)
wd.get(URL)

time.sleep(2)

# Add to cart
# Find button, inspect in browser, right click and copy xpath
add_to_cart_button = wd.find_element_by_xpath('//*[@id="ProductBuy"]/div/div[2]/button')
add_to_cart_button.click()

# View cart
view_cart_button = wd.find_element_by_xpath('//*[@id="modal-intermediary"]/div/div/div[2]/div[2]/button[2]')
view_cart_button.click()

# Pause
time.sleep(2)

# Secure checkout
secure_checkout_button = wd.find_element_by_xpath(
    '//*[@id="app"]/div[1]/section/div/div/form/div[2]/div[3]/div/div/div[3]/div/button')
secure_checkout_button.click()

# Pause
time.sleep(2)

# Login
email_input = wd.find_element_by_xpath('//*[@id="labeled-input-signEmail"]')
email_input.send_keys('myemail@email.com')
sign_in_button = wd.find_element_by_xpath('//*[@id="signInSubmit"]')
sign_in_button.click()

# Close Chrome
wd.close()
