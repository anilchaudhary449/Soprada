import allure
import time
import random
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from locators_ecom.shipping_charge_settings_locators import ShippingChargeLocators

class ShippingChargeSettings:
    def __init__(self, driver, timeout=60):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
    
    @allure.step("Adding Shipping Charge")
    def add_shipping_settings(self, logistic_charge):
        add_shipping_charge = self.wait.until(EC.presence_of_element_located((ShippingChargeLocators.ADD_SHIPPING_CHARGE)))
        add_shipping_charge.click()
        print("Add shipping charge button clicked...")
        time.sleep(0.5)
        self.shipping_charge_settings(logistic_charge)


        
    @allure.step("Editing shipping charge settings")
    def shipping_charge_settings(self, logistic_charge):
        print("Opening edit modal...")
        edit_btns = self.wait.until(EC.presence_of_all_elements_located(ShippingChargeLocators.EDIT_BTNS))
        try:
            edit_btn = random.choice(edit_btns)
            edit_btn.click()
            print("Edit button clicked...")
        except Exception:
            edit_btn = random.choice(edit_btns)
            self.driver.execute_script("arguments[0].click();", edit_btn)
            print("Edit button clicked...")
        
        time.sleep(0.5)
        self.shipping_info(logistic_charge)
        time.sleep(0.5)


    @allure.step("Updating shipping info with logistic charge: {logistic_charge}")
    def shipping_info(self, logistic_charge):
        # Basic Info
        city_input = self.wait.until(EC.presence_of_element_located(ShippingChargeLocators.CITY_NAME_INPUT))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", city_input)
        
        charge_input = self.wait.until(EC.presence_of_element_located(ShippingChargeLocators.LOGISTIC_CHARGE_INPUT))
        charge_input.clear()
        charge_input.send_keys(logistic_charge)

        # District Selection
        dropdown = self.wait.until(EC.presence_of_element_located(ShippingChargeLocators.DISTRICT_SELECT))
        select = Select(dropdown)
        options = [opt for opt in select.options if opt.is_enabled() and opt.get_attribute("value")]
        if options:
            select.select_by_index(options.index(random.choice(options)))
        
        time.sleep(0.5)


        print("Updating shipping settings...")
        update_btn = self.wait.until(EC.element_to_be_clickable(ShippingChargeLocators.UPDATE_BTN))
        try:
            update_btn.click()
            print("Update button clicked...")
        except Exception:
            self.driver.execute_script("arguments[0].click();", update_btn)
            print("Update button clicked...")
        
        time.sleep(2)

        # Optional: Delete flow if needed by test
        # self.delete_shipping_settings()

    @allure.step("Delete shipping setting")
    def delete_shipping_settings(self):
        print("Attempting to delete shipping setting...")
        try:
            trash_btns = self.wait.until(EC.presence_of_all_elements_located(ShippingChargeLocators.TRASH_BTNS))
            trash_btn = random.choice(trash_btns)
            trash_btn.click()
            print("Trash button clicked...")
            
            confirm_btn = self.wait.until(EC.element_to_be_clickable(ShippingChargeLocators.CONFIRM_DELETE_BTN))
            try:
                confirm_btn.click()
                print("Confirm delete button clicked...")
            except Exception:
                self.driver.execute_script("arguments[0].click();", confirm_btn)
                print("Confirm delete button clicked...")
            
            time.sleep(2)
        except Exception as e:
            print(f"Delete flow failed or not found: {e}")

