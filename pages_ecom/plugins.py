import allure
import time
import random
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators_ecom.plugins_locators import PluginsLocators

class Plugins:
    def __init__(self, driver, timeout=60):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout)

    @allure.step("Filter plugins")
    def plugins(self):
        print("Filtering plugins...")
        dropdown = self.wait.until(EC.element_to_be_clickable(PluginsLocators.PLUGINS_DROPDOWN))
        try:
            dropdown.click()
        except Exception:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", dropdown)
            self.driver.execute_script("arguments[0].click();", dropdown)
        
        options = self.wait.until(EC.presence_of_all_elements_located(PluginsLocators.DROPDOWN_OPTIONS))
        selected_option = random.choice(options)
        try:
            selected_option.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", selected_option)
        time.sleep(1)

    @allure.step("Install random plugin")
    def install_plugins(self):
        print("Installing a random plugin...")
        install_btns = self.wait.until(EC.presence_of_all_elements_located(PluginsLocators.INSTALL_BTNS))
        selected_btn = random.choice(install_btns)
        try:
            selected_btn.click()
        except Exception:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", selected_btn)
            self.driver.execute_script("arguments[0].click();", selected_btn)
        time.sleep(1)

    @allure.step("Activate/Confirm plugin installation")
    def activate_plugin(self):
        print("Confirming plugin activation...")
        confirm_btn = self.wait.until(EC.element_to_be_clickable(PluginsLocators.CONFIRM_BTN))
        try:
            confirm_btn.click()
            print("Confirm button clicked...")
        except Exception:
            self.driver.execute_script("arguments[0].click();", confirm_btn)
            print("Confirm button clicked...")
        
        try:
            # Check for validation messages (common in some plugins requiring API keys)
            error_msg = self.wait.until(EC.presence_of_element_located(PluginsLocators.VALIDATION_ERROR_MSG))
            print(f"Resulting message: {error_msg.text}")
        except TimeoutException:
            print("No immediate validation error. Plugin sequence finished.")
            pass
        
        time.sleep(1)
