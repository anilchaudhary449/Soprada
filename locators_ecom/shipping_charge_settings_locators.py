from selenium.webdriver.common.by import By

class ShippingChargeLocators:
    # Sidebar
    SIDEBAR_LINK = (By.XPATH, "//div[contains(@class,'sidebar__menu')]//span[normalize-space()='Shipping Charge Settings']")
    
    # List Actions
    ADD_SHIPPING_CHARGE = (By.XPATH, "//button[normalize-space(.)='New Shipping Area (City)']")
    EDIT_BTNS = (By.XPATH, "//div[contains(@class,'action-group')]/child::button[starts-with(@class,'btn') and contains(@title,'Edit')]")
    TRASH_BTNS  = (By.XPATH, "//div[contains(@class,'action-group')]/child::button[starts-with(@class,'btn') and contains(@title,'trash')]")
    
    # Edit Modal
    CITY_NAME_INPUT = (By.XPATH, "//input[contains(@type,'text') and contains(@placeholder,'Enter city name')]")
    LOGISTIC_CHARGE_INPUT = (By.XPATH, "//div[@class='my-6 add-logistic-charge']/child::input[contains(@type,'text') and contains(@class,'szi-input__control')]")
    DISTRICT_SELECT = (By.XPATH, "//select[@name='district']")
    DISTRICT_OPTIONS = (By.XPATH, "//option[not(@disabled)]")
    UPDATE_BTN = (By.XPATH, "//div[contains(@class,'modal-footer-buttons')]/button[text()='Update'] | //div[contains(@class,'modal-footer-buttons')]/button[text()='Save']")
    
    # Delete Confirmation
    CONFIRM_DELETE_BTN = (By.XPATH, "//div[contains(@class,'modal__container')]/following::button[starts-with(@class,'btn') and contains(text(),'Confirm')]")
