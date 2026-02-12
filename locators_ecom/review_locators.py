from selenium.webdriver.common.by import By

class ReviewLocators:
    # Review Table Actions
    # Generic toggle for first row or rows with data-id
    SWITCH_TOGGLE = (By.XPATH, "//tr[contains(@data-id,'1')]//following::span[@class='switch-toggle'] | //span[@class='switch-toggle']")
    
    # Feedback
    SUCCESS_ALERT = (By.XPATH, "//div[contains(@class,'bg-white alert alert--aquamarine alert--visible')]")
