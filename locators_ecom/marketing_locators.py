from selenium.webdriver.common.by import By

class MarketingLocators:
    # Marketing List Actions
    VIEW_BTN = (By.XPATH, "//button[text()='View']")
    ALERT_TOP = (By.XPATH, "//div[@class='alert-wrapper alert-wrapper--top']")
    ADD_COUPON_CODE_BTN = (By.XPATH, "(//button[normalize-space()='Add Coupon Code'])[1]")
    COUPON_VIEW_BTNS = (By.XPATH, "//button[@title='view']")
    
    # Add Coupon Form
    PROMOTION_TITLE_INPUT = (By.XPATH, "//div[contains(@class,'coupon-promotion')]/child::input")
    PROMOTION_CODE_INPUT = (By.XPATH, "//div[contains(@class,'coupon-code')]/child::input")
    DISCOUNT_PERCENTAGE_INPUT = (By.XPATH, "//div[contains(@class,'coupon-discount')]/child::input")
    MAX_DISCOUNT_LIMIT_INPUT = (By.XPATH, "//div[contains(@class,'coupon-max-discount')]/child::input")
    
    # Advanced Options
    ADVANCED_OPTIONS_TOGGLE = (By.XPATH, "//div[contains(@class,'coupon-advanced-options-wrapper')]/child::div")
    MINIMUM_PURCHASE_INPUT = (By.XPATH, "//div[contains(@class,'coupon_min_Purchase')]/child::input")
    START_DATE_INPUT = (By.XPATH, "//div[contains(@class,'coupon-start-date') or contains(@class,'start_date')]/child::input")
    END_DATE_INPUT = (By.XPATH, "//div[contains(@class,'coupon-end-date') or contains(@class,'end_date')]/child::input")
    MAX_USE_INPUT = (By.XPATH, "//div[contains(@class,'coupon-max-use')]/child::input")
    
    # Modal Footer Actions
    ADD_COUPON_SUBMIT_BTN = (By.XPATH, "//div[contains(@class,'modal__footer')]/child::button[text()='Add Coupon Code']")
    CLOSE_MODAL_BTN = (By.XPATH, "//button[text()='Close']")
    CROSS_MODAL_BTN = (By.XPATH, "//div[contains(@class,'modal__header')]/following::button[contains(@class,'modal__close')]")
