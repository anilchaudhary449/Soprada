import allure
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from locators_ecom.login_locators import LoginLocators

class login_with_otp:
    def __init__(self, driver, timeout=120):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.action = ActionChains(self.driver)

    @allure.step("Open Saauzi site: {URL}")
    def open_saauzi_site(self, URL):
        self.driver.get(URL)

    @allure.step("Trigger resend OTP")
    def trigger_resend_otp(self):
        """Clicks the resend OTP button/link if available."""
        try:
            for locator in LoginLocators.RESEND_BTNS:
                elements = self.driver.find_elements(*locator)
                if elements and elements[0].is_displayed():
                    elements[0].click()
                    return True
            return False
        except Exception:
            return False

    @allure.step("Enter email: {email}")
    def enter_specific_email(self, email):
        """Enters a specific email address into the login field."""
        email_input = self.wait.until(EC.visibility_of_element_located(LoginLocators.EMAIL_INPUT))
        email_input.clear()
        email_input.send_keys(email)
        
        login_btn = self.wait.until(EC.element_to_be_clickable(LoginLocators.LOGIN_BTN))
        assert login_btn.is_enabled(), "Login button is not enabled"
        login_btn.click()

    @allure.step("Enter OTP: {otp_code}")
    def enter_otp_direct(self, otp_code):
        """Enters the OTP code directly into the digit inputs."""
        otp_inputs = self.wait.until(EC.presence_of_all_elements_located(LoginLocators.OTP_INPUTS))
        
        # In many Saauzi forms, you can't just send_keys to the group.
        # We'll enter them one by one.
        for i, digit in enumerate(otp_code):
            if i < len(otp_inputs):
                otp_inputs[i].click()
                otp_inputs[i].clear()
                otp_inputs[i].send_keys(digit)
                time.sleep(0.1) # Small delay for UI to register
        
        time.sleep(1)
        verify_btn = self.wait.until(EC.element_to_be_clickable(LoginLocators.VERIFY_BTN))
        self.driver.execute_script("arguments[0].click();", verify_btn)
