import allure
import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from locators_ecom.select_store_locators import SelectStoreLocators


class SelectStore:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    @allure.step("Select first store and proceed to dashboard")
    def select_first_store(self):
        """Clicks the first store item (already pre-selected) and submits."""
        # The first store is already highlighted with 'is-selected' — just click it to be sure
        try:
            first_store = self.wait.until(
                EC.element_to_be_clickable(SelectStoreLocators.FIRST_STORE_ITEM)
            )
            store_name_el = first_store.find_elements(*SelectStoreLocators.STORE_NAME)
            store_name = store_name_el[0].text if store_name_el else "unknown"
            print(f"Selecting store: {store_name}")
            first_store.click()
        except TimeoutException:
            print("Could not click first store item — attempting submit directly.")

        # Click the "Select Store" button
        select_btn = self.wait.until(
            EC.element_to_be_clickable(SelectStoreLocators.SELECT_STORE_BTN)
        )
        self.driver.execute_script("arguments[0].click();", select_btn)

        # Wait for redirect to dashboard
        try:
            WebDriverWait(self.driver, 30).until(
                lambda d: "dashboard" in d.current_url.lower()
            )
            print(f"Store selected. Now on: {self.driver.current_url}")
        except TimeoutException:
            try:
                allure.attach(
                    self.driver.get_screenshot_as_png(),
                    name="Select Store Timeout",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception:
                pass
            pytest.fail(
                f"Timed out waiting for dashboard after store selection. "
                f"Current URL: {self.driver.current_url}"
            )
