import allure
import time
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from locators_ecom.support_case_locators import SupportCaseLocators

class SupportCase:
    def __init__(self, driver, timeout=60):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout)

    @allure.step("Filter support cases by status: {status}")
    def filter_by_status(self, status):
        print(f"Filtering support cases by status: {status}")
        
        # Wait for alerts to clear
        try:
            self.wait.until(EC.invisibility_of_element_located(SupportCaseLocators.VISIBLE_ALERT))
        except Exception:
            pass

        dropdown_elem = self.wait.until(EC.presence_of_element_located(SupportCaseLocators.STATUS_FILTER_SELECT))
        select = Select(dropdown_elem)
        
        try:
            select.select_by_visible_text(status)
            print(f"Status {status} selected...")
        except Exception as e:
            print(f"Initial select failed: {e}. Retrying with wait...")
            time.sleep(2)
            select.select_by_visible_text(status)
            print(f"Status {status} selected...")
            pass
        
        time.sleep(2)


        