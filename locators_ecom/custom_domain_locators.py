from selenium.webdriver.common.by import By

class CustomDomainLocators:
    # Page Header/Actions
    ADD_OR_EDIT_BTN = (By.XPATH, "//button[contains(@class,'btn') and (normalize-space()='Add Custom Domain' or normalize-space()='Edit Domain')]")
    ADD_CUSTOM_DOMAIN_PAGE_BTN = (By.XPATH, "//button[contains(@class,'btn') and normalize-space()='Add Custom Domain']")
    EDIT_DOMAIN_PAGE_BTN = (By.XPATH, "(//button[contains(@class,'btn') and normalize-space()='Edit Domain'])[1]")
    
    # Forms
    DOMAIN_INPUT = (By.XPATH, "//input[@placeholder='Enter your domain (e.g., example.com)']")
    UPDATE_DOMAIN_BTN = (By.XPATH, "//button[contains(@class,'btn') and text()='Update Domain']")
    
    # Add Modal
    ADD_DOMAIN_MODAL_INPUT = (By.XPATH, "//input[@type='text' and starts-with(@placeholder,'Enter your domain')]")
    ADD_DOMAIN_MODAL_SUBMIT_BTN = (By.XPATH, "//button[contains(@class,'btn') and normalize-space()='Add Domain']")
    
    # Delete Modal
    DELETE_DOMAIN_PAGE_BTN = (By.XPATH, "(//button[contains(@class,'btn') and normalize-space()='Delete Domain'])[1]")
    DELETE_CONFIRM_INPUT = (By.XPATH, "//input[@placeholder='Enter domain name to delete']")
    DELETE_CONFIRM_BTN = (By.XPATH, "//button[contains(@class,'bg-danger') and text()='Delete Domain']")
    
    # Settings
    ADVANCED_DNS_SETTING = (By.XPATH, "//div[@class='px-6 py-4 mx-4']/child::div[contains(@class,'cursor-pointer')]")
    
    # Feedback
    SUCCESS_ALERT = (By.XPATH, "//div[contains(@class,'bg-white alert alert--aquamarine alert--visible')]")
