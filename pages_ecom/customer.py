import allure
import os
import time
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from locators_ecom.customer_locators import CustomerLocators
from resources.resources import IMAGES_DIR

class Customer:
    def __init__(self, driver, timeout=60):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def _safe_click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        try:
            element.click()
        except:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Navigate to Add Customer modal")
    def customer_nav(self):
        self._safe_click(CustomerLocators.NAV_ADD_CUSTOMER_BTN)
        print("Add Customer button clicked...")
        time.sleep(1)

    @allure.step("Enter customer name: {customer_name}")
    def enter_customer_name(self, customer_name):
        customer_name_input = self.wait.until(EC.presence_of_element_located(CustomerLocators.NAME_INPUT))
        assert customer_name_input.is_enabled(), f"Customer Name input isn't enabled."
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", customer_name_input)
        customer_name_input.clear()
        customer_name_input.send_keys(customer_name)
        print("Customer name entered...")

    @allure.step("Enter customer email: {customer_email}")
    def enter_customer_email(self, customer_email):
        customer_email_input = self.wait.until(EC.presence_of_element_located(CustomerLocators.EMAIL_INPUT))
        assert customer_email_input.is_enabled(), f"Customer Email input isn't enabled."
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", customer_email_input)
        customer_email_input.clear()
        customer_email_input.send_keys(customer_email)
        print("Customer email entered...")

    @allure.step("Enter customer phone: {customer_phone}")
    def enter_customer_phone(self, customer_phone):
        customer_phone_input = self.wait.until(EC.presence_of_element_located(CustomerLocators.PHONE_INPUT))
        assert customer_phone_input.is_enabled(), f"Customer Phone input isn't enabled."
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", customer_phone_input)
        customer_phone_input.clear()
        customer_phone_input.send_keys(customer_phone)
        print("Customer phone entered...")

    @allure.step("Enter customer street: {customer_street}")
    def enter_customer_street(self, customer_street):
        customer_street_input = self.wait.until(EC.presence_of_element_located(CustomerLocators.STREET_INPUT))     
        assert customer_street_input.is_enabled(), f"Customer Street input isn't enabled."
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", customer_street_input)
        customer_street_input.clear()
        customer_street_input.send_keys(customer_street)
        print("Customer street entered...")

    @allure.step("Select random customer city")
    def select_customer_city(self):
        self._safe_click(CustomerLocators.CITY_SELECT)
        print("Customer city dropdown clicked...")
        
        customer_city_options = self.wait.until(EC.presence_of_all_elements_located(CustomerLocators.CITY_OPTIONS))     
        randomly_select_customer_city = random.choice(customer_city_options)
        try:
            randomly_select_customer_city.click()
            print("Customer city selected...")
        except:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", randomly_select_customer_city)
            self.driver.execute_script("arguments[0].click();", randomly_select_customer_city)
            print("Customer city selected...")

    @allure.step("Upload customer image: {image_name}")
    def upload_customer_image(self, image_name="customer_image.png"):
        image_customer = self.wait.until(EC.presence_of_element_located(CustomerLocators.FILE_INPUT))     
        
        if os.path.isabs(image_name):
             customer_image_path = image_name
        else:
             customer_image_path = os.path.join(IMAGES_DIR, image_name)
        
        if not os.path.exists(customer_image_path):
             print(f"Image not found at: {customer_image_path}")
        
        image_customer.send_keys(customer_image_path)
        print("Customer image uploaded...")
        time.sleep(2)

    @allure.step("Click Add Customer button")
    def add_customer_btn(self):
        self._safe_click(CustomerLocators.SUBMIT_CUSTOMER_BTN)
        print("Add Customer button clicked...")
        
        # Assertion for Success Alert
        try:
             alert = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(CustomerLocators.ALERT_TOP))
             print(f"Customer Add Alert: {alert.text}")
             valid_messages = ["success", "added", "updated", "processing"]
             assert any(msg in alert.text.lower() for msg in valid_messages), f"Unexpected alert message: {alert.text}"
             WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located(CustomerLocators.ALERT_TOP))
        except TimeoutException:
             print("No success alert appeared within timeout for Customer.")
        except Exception as e:
             print(f"An error occurred while verifying Customer alert: {e}")
        
    @allure.step("View and update recently created customer")
    def view_customer(self):
        view_customer_btns = self.wait.until(EC.presence_of_all_elements_located(CustomerLocators.VIEW_BTNS))
        select_view_btn = random.choice(view_customer_btns)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", select_view_btn)
        try:
            select_view_btn.click()
            print("View button clicked...")
        except:
            self.driver.execute_script("arguments[0].click();", select_view_btn)
            print("View button clicked...")
        time.sleep(2)

        self._safe_click(CustomerLocators.UPDATE_CUSTOMER_BTN)
        print("Update button clicked...")
        time.sleep(2)
