import allure
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from locators_ecom.create_new_store_locators import CreateStoreLocators

class Create_Store:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 120)

    @allure.step("Create new store: {store_name}")
    def create_store(self, store_name: str, store_contact: str):
        assert "create-store" in self.driver.current_url.lower(), f"Current URL {self.driver.current_url} is not create-store"
        
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
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", create_store_btn)
            self.driver.execute_script("arguments[0].click();", create_store_btn) 

        # Wait for potential dashboard redirect
        self.wait.until(lambda d: "dashboard" in d.current_url.lower() or "create-store" not in d.current_url.lower())
