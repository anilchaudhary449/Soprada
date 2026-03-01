from selenium.webdriver.common.by import By

class LoginLocators:
    EMAIL_INPUT = (By.ID, "email")
    LOGIN_BTN = (By.ID, "login-btn")
    RESEND_BTNS = [
        (By.XPATH, "//button[contains(text(),'Resend')]"),
        (By.XPATH, "//a[contains(text(),'Resend')]"),
        (By.XPATH, "//span[contains(text(),'Resend')]"),
        (By.XPATH, "//button[contains(text(),'Send again')]")
    ]
    OTP_INPUTS = (By.XPATH, "//input[@type='text' and @maxlength='1']")
    VERIFY_BTN = (By.XPATH, "//button[contains(@class,'login-btn') and normalize-space(.)='Verify']")
