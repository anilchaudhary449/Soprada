from selenium.webdriver.common.by import By

class CustomerLocators:
    # Customer List
    NAV_ADD_CUSTOMER_BTN = (By.XPATH, "//div[starts-with(@class,'customer-add-new-button')]/child::button")
    ALERT_TOP = (By.XPATH, "//div[@class='alert-wrapper alert-wrapper--top']")
    VIEW_BTNS = (By.XPATH, "//div[@class='action-group']/button[@title='view']")
    
    # Add/Edit Customer Modal
    NAME_INPUT = (By.XPATH, "//div[starts-with(@class,'add-customer-name col-12')]/child::input")
    EMAIL_INPUT = (By.XPATH, "//div[starts-with(@class,'add-customer-email col-6')]/child::input")
    PHONE_INPUT = (By.XPATH, "//div[starts-with(@class,'add-customer-name col-6')]/child::input")
    STREET_INPUT = (By.XPATH, "//div[starts-with(@class,'add-customer-address col-6')]/child::input[@placeholder='Enter customer Street Address']")
    CITY_SELECT = (By.XPATH, "//label[text()='City']/following-sibling::select[contains(@class,'szi-input__control')]")
    CITY_OPTIONS = (By.XPATH, "//option[not(@disabled)]")
    FILE_INPUT = (By.XPATH, "//div[starts-with(@class,'p-6')]/child::input[@type='file']")
    SUBMIT_CUSTOMER_BTN = (By.XPATH, "//div[@class='modal__footer']/button[text()='Add New Customer']")
    
    # View/Update Customer
    UPDATE_CUSTOMER_BTN = (By.XPATH, "//button[normalize-space()='Update Customer']")
