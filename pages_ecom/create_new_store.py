import allure
import time
import pytest
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException, NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from locators_ecom.create_new_store_locators import CreateStoreLocators

class Create_Store:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 120)

    def _dismiss_alert_if_present(self):
        """Dismiss any unexpected alert and return its text."""
        try:
            alert = self.driver.switch_to.alert
            text = alert.text
            alert.accept()
            return text
        except NoAlertPresentException:
            return None

    def _get_visible_error(self):
        """Grab any visible error/validation message on the page."""
        try:
            errors = self.driver.find_elements(
                By.XPATH,
                "//*[contains(@class,'error') or contains(@class,'alert') or contains(@class,'invalid') or contains(@class,'text-danger')]"
            )
            msgs = [e.text.strip() for e in errors if e.is_displayed() and e.text.strip()]
            return " | ".join(msgs) if msgs else None
        except Exception:
            return None

    @allure.step("Create new store: {store_name}")
    def create_store(self, store_name: str, store_contact: str):
        assert "create-store" in self.driver.current_url.lower(), \
            f"Current URL {self.driver.current_url} is not create-store"

        enter_store_name = self.wait.until(EC.presence_of_element_located(CreateStoreLocators.STORE_NAME_INPUT))
        enter_store_name.clear()
        enter_store_name.send_keys(store_name)

        enter_store_contact = self.wait.until(EC.presence_of_element_located(CreateStoreLocators.STORE_CONTACT_INPUT))
        enter_store_contact.clear()
        enter_store_contact.send_keys(store_contact)

        time.sleep(1)

        create_store_btn = self.wait.until(EC.presence_of_element_located(CreateStoreLocators.SUBMIT_BTN))
        assert create_store_btn.is_enabled(), "Create Store button isn't enabled."

        try:
            create_store_btn.click()
        except Exception:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                create_store_btn
            )
            self.driver.execute_script("arguments[0].click();", create_store_btn)

        # Wait for redirect away from create-store (to dashboard or any other page)
        try:
            WebDriverWait(self.driver, 60).until(
                lambda d: "dashboard" in d.current_url.lower()
                          or "create-store" not in d.current_url.lower()
            )
        except TimeoutException:
            # Dismiss any alert that may be blocking
            alert_text = self._dismiss_alert_if_present()
            error_text = self._get_visible_error()

            # Take a screenshot for debugging
            try:
                allure.attach(
                    self.driver.get_screenshot_as_png(),
                    name="Store Creation Timeout",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception:
                pass

            msg = f"Store creation timed out. Current URL: {self.driver.current_url}"
            if alert_text:
                msg += f" | Alert: {alert_text}"
            if error_text:
                msg += f" | Page error: {error_text}"

            pytest.fail(msg)
