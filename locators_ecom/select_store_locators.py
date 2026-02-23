from selenium.webdriver.common.by import By

class SelectStoreLocators:
    # First store item in the list (already pre-selected with 'is-selected' class)
    FIRST_STORE_ITEM = (By.CSS_SELECTOR, "div.store-item:first-child")
    # The "Select Store" submit button
    SELECT_STORE_BTN = (By.CSS_SELECTOR, "button.btn-submit")
    # Store name text inside a store item
    STORE_NAME = (By.CSS_SELECTOR, "span.store-name")
