from selenium.webdriver.common.by import By

class CreateStoreLocators:
    STORE_NAME_INPUT = (By.XPATH, "//input[contains(@type,'text') and (@placeholder='Enter Shop Name')]")
    STORE_CONTACT_INPUT = (By.XPATH, "//input[contains(@type,'text') and (@placeholder='Enter Phone Number')]")
    SUBMIT_BTN = (By.XPATH, "//button[contains(@class,'btn btn-gradient btn--block btn--lg') and normalize-space(text()='Submit')]")
