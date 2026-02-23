from selenium.webdriver.common.by import By

class StaffLocators:
    # Staff List
    ADD_NEW_STAFF_TOP_BTN = (By.XPATH, "//div[normalize-space(.)='Add New Staff'] | //button//div[normalize-space(text())='Add New Staff']")
    EDIT_BTNS = (By.XPATH, "//button[@title='Edit Staff' and @type='button']")
    DELETE_BTNS = (By.XPATH, "//button[@title='Delete Staff' and @type='button']")
    ALERT_TOP = (By.XPATH, "//div[@class='alert-wrapper alert-wrapper--top']")
    
    # Add/Edit Staff Modal
    FULLNAME_INPUT = (By.XPATH, "//input[@id='staff_full_name']")
    EMAIL_INPUT = (By.XPATH, "//input[@id='staff_email']")
    ROLE_SELECT = (By.XPATH, "//select[@id='staff_role']")
    PHONE_INPUT = (By.XPATH, "//input[@id='staff_phone']")
    ADDRESS_INPUT = (By.XPATH, "//input[@id='staff_address']")
    SUBMIT_STAFF_BTN = (By.XPATH, "//div[contains(@class,'modal__footer')]//button[normalize-space(text())='Add New Staff']")
    UPDATE_STAFF_BTN = (By.XPATH, "//div[contains(@class,'modal__footer')]//button[normalize-space(text())='Update Staff']")
    
    # Delete Confirmation
    CONFIRM_DELETE_BTN = (By.XPATH, "//button[text()='Delete Staff']")
    
    # Role Permissions
    ADD_ROLE_PERMISSIONS_TOP_BTN = (By.XPATH, "//div[@class='flex gap-x-2']/child::a[normalize-space()='Add Role Permissions'] | //div[@class='flex gap-x-2']/a[normalize-space(text())='Add Role Permissions']")
    ADD_NEW_ROLE_PERMISSIONS_BTN = (By.XPATH, "//div[@class='flex gap-x-2']//div[normalize-space()='Add New Role Permissions'] | //div[@class='flex items-center gap-x-2' and normalize-space(.)='Add New Role Permissions']")
    PERMISSION_ROLE_SELECT = (By.XPATH, "//select[contains(@class,'szi-input__control')]")
    SELECT_STAFF_ROLE = (By.XPATH, "//option[not(@disabled)]")

    #Allow All Permissions
    ALLOW_ALL_PERMISSIONS_CHECKBOX = (By.XPATH, "//input[@type='checkbox']")

    #platforms
    E_Com = (By.XPATH, "//div[contains(@class,'selected')]")
    POS = (By.XPATH, "//div[contains(@class,'selected')]//following-sibling::div[normalize-space(.)='Point of Sale']")
    
    # Modules
    MODULES = lambda module_name: (By.XPATH, f"//div[contains(@class,'flex items-center gap-x-3') and normalize-space(.)='{module_name}']")

    # Staff Options
    STAFF_OPTIONS = (By.XPATH, "//ul//following::li")
    SUBMIT_PERMISSION_BTN = (By.XPATH, "//div[contains(@class,'modal__footer')]//following-sibling::button[contains(@class,'pumpkin') or contains(normalize-space(),'Add New Role Permissions')]")
