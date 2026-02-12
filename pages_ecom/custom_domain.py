import allure
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from locators_ecom.custom_domain_locators import CustomDomainLocators

class Custom_Domain:
    def __init__(self, driver, timeout=60):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout)

    @allure.step("Configure custom domain: {domain_name}")
    def custom_domain(self, domain_name, updated_domain):
        # Wait for either 'Add Custom Domain' button or 'Edit Domain' to appear
        self.wait.until(EC.presence_of_element_located(CustomDomainLocators.ADD_OR_EDIT_BTN))
        print("Add or Edit button found...")
        time.sleep(1)

        # Check if 'Add Custom Domain' button is present (implies no domain yet)
        add_domain_elements = self.driver.find_elements(*CustomDomainLocators.ADD_CUSTOM_DOMAIN_PAGE_BTN)
        print("Add domain elements found...")
        time.sleep(1)
        print(add_domain_elements)
        if not add_domain_elements or not add_domain_elements[0].is_displayed():
            self._edit_and_delete_domain(updated_domain)
            print("Edit and delete flow...")
        else:
            self._add_new_domain(domain_name)
            print("Add new domain flow...")

    def _edit_and_delete_domain(self, updated_domain):
        print("Existing domain found. Testing Edit and Delete flow.")
        edit_domain = self.wait.until(EC.element_to_be_clickable(CustomDomainLocators.EDIT_DOMAIN_PAGE_BTN))
        try:
            edit_domain.click()
            print("Edit domain button clicked...")
        except Exception:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", edit_domain)
            self.driver.execute_script("arguments[0].click();", edit_domain)
            print("Edit domain button clicked...")
        
        time.sleep(1)
        input_domain = self.wait.until(EC.presence_of_element_located(CustomDomainLocators.DOMAIN_INPUT))
        input_domain.clear()
        input_domain.send_keys(updated_domain)
        
        update_btn = self.wait.until(EC.element_to_be_clickable(CustomDomainLocators.UPDATE_DOMAIN_BTN))
        assert update_btn.is_enabled(), "Update Domain button isn't enabled."
        try:
            update_btn.click()
            print("Update domain button clicked...")
        except Exception:
            self.driver.execute_script("arguments[0].click();", update_btn)
            print("Update domain button clicked...")
        
        # Handle feedback
        try:
            alert = self.wait.until(EC.visibility_of_element_located(CustomDomainLocators.SUCCESS_ALERT))
            print(f"Update Alert: {alert.text}")
        except TimeoutException:
            pass

        time.sleep(1)
        self._toggle_advanced_dns()

        # Delete flow
        print("Proceeding to delete the domain.")
        delete_btn = self.wait.until(EC.element_to_be_clickable(CustomDomainLocators.DELETE_DOMAIN_PAGE_BTN))
        try:
            delete_btn.click()
            print("Delete domain button clicked...")
        except Exception:
            self.driver.execute_script("arguments[0].click();", delete_btn)
            print("Delete domain button clicked...")
        
        confirm_input = self.wait.until(EC.presence_of_element_located(CustomDomainLocators.DELETE_CONFIRM_INPUT))
        confirm_input.send_keys(updated_domain)
        
        final_delete_btn = self.wait.until(EC.element_to_be_clickable(CustomDomainLocators.DELETE_CONFIRM_BTN))
        try:
            final_delete_btn.click()
            print("Final delete button clicked...")
        except Exception:
            self.driver.execute_script("arguments[0].click();", final_delete_btn)
            print("Final delete button clicked...")
            
        try:
            alert = self.wait.until(EC.visibility_of_element_located(CustomDomainLocators.SUCCESS_ALERT))
            print(f"Delete Alert: {alert.text}")
        except TimeoutException:
            pass
        time.sleep(2)

    def _add_new_domain(self, domain_name):
        print("No existing domain. Testing Add Domain flow.")
        add_btn = self.wait.until(EC.element_to_be_clickable(CustomDomainLocators.ADD_CUSTOM_DOMAIN_PAGE_BTN))
        try:
            add_btn.click()
            print("Add domain button clicked...")
        except Exception:
            self.driver.execute_script("arguments[0].click();", add_btn)
            print("Add domain button clicked...")

        modal_input = self.wait.until(EC.presence_of_element_located(CustomDomainLocators.ADD_DOMAIN_MODAL_INPUT))
        modal_input.send_keys(domain_name)
        print("Domain name entered...")

        modal_submit = self.wait.until(EC.element_to_be_clickable(CustomDomainLocators.ADD_DOMAIN_MODAL_SUBMIT_BTN))
        try:
            modal_submit.click()
            print("Modal submit button clicked...")
        except Exception:
            self.driver.execute_script("arguments[0].click();", modal_submit)
            print("Modal submit button clicked...")
        
        try:
            alert = self.wait.until(EC.visibility_of_element_located(CustomDomainLocators.SUCCESS_ALERT))
            print(f"Add Alert: {alert.text}")
        except TimeoutException:
            pass
        
        self._toggle_advanced_dns()
        print("Advanced DNS toggled...")

    def _toggle_advanced_dns(self):
        advanced_dns = self.wait.until(EC.presence_of_element_located(CustomDomainLocators.ADVANCED_DNS_SETTING))
        try:
            advanced_dns.click()
            print("Advanced DNS clicked...")
        except Exception:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", advanced_dns)
            self.driver.execute_script("arguments[0].click();", advanced_dns)
            print("Advanced DNS clicked...")
        time.sleep(2)
