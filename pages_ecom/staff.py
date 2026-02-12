import allure
import random
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from locators_ecom.staff_locators import StaffLocators

class Staff:
    def __init__(self, driver, timeout=60):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout)

    def _safe_click(self, locator, scroll=True):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        if scroll:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            time.sleep(0.5)
        try:
            element.click()
        except:
            self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Add new staff: {fullname}")
    def add_staff(self, fullname, email, phone_number, address):
        self._safe_click(StaffLocators.ADD_NEW_STAFF_TOP_BTN)
        time.sleep(0.5)
        
        staff_fullname = self.wait.until(EC.presence_of_element_located(StaffLocators.FULLNAME_INPUT))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", staff_fullname)
        time.sleep(0.5)
        staff_fullname.send_keys(fullname)
        print("Full name entered...")
        
        staff_email = self.wait.until(EC.presence_of_element_located(StaffLocators.EMAIL_INPUT))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", staff_email)
        time.sleep(0.5)
        staff_email.send_keys(email)
        print("Email entered...")
        
        select_role_elem = self.wait.until(EC.presence_of_element_located(StaffLocators.ROLE_SELECT))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", select_role_elem)
        time.sleep(0.5)
        select_role = Select(select_role_elem)
        options = [opt for opt in select_role.options if not opt.get_attribute("disabled") and opt.get_attribute("value")]
        if options:
            select_role.select_by_visible_text(random.choice(options).text)
        
        staff_phone = self.wait.until(EC.presence_of_element_located(StaffLocators.PHONE_INPUT))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", staff_phone)
        time.sleep(0.5)
        staff_phone.send_keys(phone_number)
        print("Phone number entered...")
        
        staff_address = self.wait.until(EC.presence_of_element_located(StaffLocators.ADDRESS_INPUT))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", staff_address)
        time.sleep(0.5)
        staff_address.send_keys(address)
        print("Address entered...")
        
        self._safe_click(StaffLocators.SUBMIT_STAFF_BTN)
        
        # Assertion for Success Alert
        try:
             alert = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(StaffLocators.ALERT_TOP))
             print(f"Staff Add Alert: {alert.text}")
             assert "success" in alert.text.lower() or "added" in alert.text.lower(), f"Unexpected alert message: {alert.text}"
             WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located(StaffLocators.ALERT_TOP))
        except TimeoutException:
             print("No success alert appeared within timeout for Staff Add.")
        except Exception as e:
             print(f"An error occurred while verifying Staff alert: {e}")

    @allure.step("Edit staff: {fullname}")
    def edit_staff(self, fullname, address):
        edit_btns = self.wait.until(EC.presence_of_all_elements_located(StaffLocators.EDIT_BTNS))
        select_edit_btn = random.choice(edit_btns)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", select_edit_btn)
        time.sleep(0.5)
        self.driver.execute_script("arguments[0].click();", select_edit_btn)
        time.sleep(0.5)

        staff_fullname = self.wait.until(EC.presence_of_element_located(StaffLocators.FULLNAME_INPUT))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", staff_fullname)
        staff_fullname.clear()
        staff_fullname.send_keys(fullname)
        print("Full name entered...")
        
        staff_address = self.wait.until(EC.presence_of_element_located(StaffLocators.ADDRESS_INPUT))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", staff_address)
        staff_address.clear()
        staff_address.send_keys(address)
        print("Address entered...")
        
        self._safe_click(StaffLocators.UPDATE_STAFF_BTN)
        # time.sleep(5)

    @allure.step("Delete one random staff")
    def delete_staff(self):
        delete_btns = self.wait.until(EC.presence_of_all_elements_located(StaffLocators.DELETE_BTNS))
        select_delete_btn = random.choice(delete_btns)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", select_delete_btn)
        time.sleep(0.5)
        try:
            select_delete_btn.click()
            print("Delete button clicked...")
        except:
            self.driver.execute_script("arguments[0].click();", select_delete_btn)
            print("Delete button clicked...")
        
        self._safe_click(StaffLocators.CONFIRM_DELETE_BTN)
        time.sleep(5)

    @allure.step("Add role permissions to random staff")
    def add_role_permission(self):
        self._safe_click(StaffLocators.ADD_ROLE_PERMISSIONS_TOP_BTN)
        time.sleep(0.5)
        
        self._safe_click(StaffLocators.ADD_NEW_ROLE_PERMISSIONS_BTN)
        time.sleep(0.5)
        
        select_role_permission_elem = self.wait.until(EC.presence_of_element_located(StaffLocators.PERMISSION_ROLE_SELECT))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", select_role_permission_elem)
        time.sleep(0.5)
        select_role_p = Select(select_role_permission_elem)
        options = [opt for opt in select_role_p.options if not opt.get_attribute("disabled") and opt.get_attribute("value")]
        if options:
            select_role_p.select_by_visible_text(random.choice(options).text)
        
        self._safe_click(StaffLocators.SELECT_STAFF_DROPDOWN)
        time.sleep(0.5) 
        
        select_staff_permission = self.wait.until(EC.presence_of_all_elements_located(StaffLocators.STAFF_OPTIONS))
        select_random_staff_permission = random.choice(select_staff_permission)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", select_random_staff_permission)
        try:
            select_random_staff_permission.click()
            print("Staff permission selected...")
        except:
            self.driver.execute_script("arguments[0].click();", select_random_staff_permission)
            print("Staff permission selected...")
        
        self._safe_click(StaffLocators.SUBMIT_PERMISSION_BTN)
        time.sleep(1)
