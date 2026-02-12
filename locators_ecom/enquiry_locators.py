from selenium.webdriver.common.by import By

class EnquiryLocators:
    # Enquiry List Actions
    MARK_ALL_AS_SEEN_BTN = (By.XPATH, "//button[normalize-space()='Mark All as Seen']")
    TOGGLE_STATUS_BTN = (By.XPATH, "//label[@class='switch-label']/child::span")
    VIEW_ENQUIRY_BTN = (By.XPATH, "//button[@title='view']")
    
    # Enquiry Detail/Reply
    REPLID_STATUS_BADGE = (By.XPATH, "//span[text()='Replied']")
    EDIT_REPLY_BTN = (By.XPATH, "//button[contains(@class, 'btn btn-light') and normalize-space(.)='Edit']")
    REPLY_TEXTAREA = (By.XPATH, "//div[contains(@class,'enquiry-response')]/child::textarea")
    SUBMIT_REPLY_BTN = (By.XPATH, "//button[normalize-space(.)='Submit Enquiry Reply']")
    
    # Alerts/Notifications
    ALERT_VISIBLE = (By.XPATH, "//div[contains(@class,'alert--visible')]")
    ALERT_TITLE = (By.XPATH, "//div[@class='alert__title']")
    SUCCESS_ALERT = (By.XPATH, "//div[contains(@class,'bg-white alert alert--aquamarine alert--visible')]")
