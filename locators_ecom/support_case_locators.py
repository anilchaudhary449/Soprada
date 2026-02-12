from selenium.webdriver.common.by import By

class SupportCaseLocators:
    # Filter Controls
    STATUS_FILTER_SELECT = (By.XPATH, "//select[@class='szi-input__control szi-input__control--select']")
    
    # Feedback
    VISIBLE_ALERT = (By.XPATH, "//div[contains(@class,'alert--visible')]")
