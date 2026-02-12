from selenium.webdriver.common.by import By

class LoginLocators:
    EMAIL_INPUT = (By.XPATH, "//input[@class='form-input']")
    LOGIN_BTN = (By.XPATH, "//button[contains(@class,'btn-login')]/span")
    RESEND_BTNS = [
        (By.XPATH, "//button[contains(text(),'Resend')]"),
        (By.XPATH, "//a[contains(text(),'Resend')]"),
        (By.XPATH, "//span[contains(text(),'Resend')]"),
        (By.XPATH, "//button[contains(text(),'Send again')]")
    ]
    OTP_INPUTS = (By.XPATH, "//input[@type='text' and @maxlength='1']")
    VERIFY_BTN = (By.XPATH, "//button[contains(@class,'btn-verify')]")
