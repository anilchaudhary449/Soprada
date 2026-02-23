import allure
import random
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from locators_ecom.staff_locators import StaffLocators
from resources.resources import get_random_e_com_module, get_random_pos_module

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
        print(f"Full name entered...{fullname}")
        
        staff_email = self.wait.until(EC.presence_of_element_located(StaffLocators.EMAIL_INPUT))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", staff_email)
        time.sleep(0.5)
        staff_email.send_keys(email)
        print(f"Email entered...{email}")
        
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
        print(f"Phone number entered...{phone_number}")
        
        staff_address = self.wait.until(EC.presence_of_element_located(StaffLocators.ADDRESS_INPUT))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", staff_address)
        time.sleep(0.5)
        staff_address.send_keys(address)
        print(f"Address entered...{address}")
        
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
        print(f"Full name edited...{fullname}")
        
        staff_address = self.wait.until(EC.presence_of_element_located(StaffLocators.ADDRESS_INPUT))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", staff_address)
        staff_address.clear()
        staff_address.send_keys(address)
        print(f"Address edited...{address}")
        
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
            print(f"Delete button clicked...{select_delete_btn}")
        except:
            self.driver.execute_script("arguments[0].click();", select_delete_btn)
            print(f"Delete button clicked...{select_delete_btn}")
        
        self._safe_click(StaffLocators.CONFIRM_DELETE_BTN)
        time.sleep(5)

    @allure.step("Add role permissions to random staff")
    def add_role_permission(self):
        self._safe_click(StaffLocators.ADD_ROLE_PERMISSIONS_TOP_BTN)
        time.sleep(0.5)
        
        self._safe_click(StaffLocators.ADD_NEW_ROLE_PERMISSIONS_BTN)
        time.sleep(0.5)
        
        select_role_permission_elem = self.wait.until(EC.presence_of_element_located(StaffLocators.PERMISSION_ROLE_SELECT))
        try:
            select_role_permission_elem.click()
            print("Role permission clicked...")
        except:
            self.driver.execute_script("arguments[0].click();", select_role_permission_elem)
            print("Role permission clicked...")  
        time.sleep(0.5)
        
        staff_options_role =self.wait.until(EC.presence_of_all_elements_located(StaffLocators.SELECT_STAFF_ROLE))  
        select_staff_role = random.choice(staff_options_role)
        try:
            select_staff_role.click()
            print(f"Staff role selected...{select_staff_role.text}")
        except:
            self.driver.execute_script("arguments[0].click();", select_staff_role)
            print(f"Staff role selected...{select_staff_role.text}")
        time.sleep(0.5)

        allow_all_permissions_checkbox = self.wait.until(EC.presence_of_element_located(StaffLocators.ALLOW_ALL_PERMISSIONS_CHECKBOX))
        allow_all_permissions_checkbox.click()
        if allow_all_permissions_checkbox.is_selected():
            print("Allow all permissions checkbox is selected")
            allow_all_permissions_checkbox.click()
        else:
            print("Allow all permissions checkbox is not selected")
        time.sleep(0.5)

        #select e_com_tab
        e_comm_tab = self.wait.until(EC.presence_of_element_located(StaffLocators.E_Com))
        e_comm_tab.click()
        
        #randomly select e_com_module
        e_com_module = get_random_e_com_module()
        E_comm_modules = self.wait.until(EC.presence_of_element_located(StaffLocators.MODULES(e_com_module)))
        try:
            E_comm_modules.click()
            print(f"E-comm module selected...{E_comm_modules.text}")
        except:
            self.driver.execute_script("arguments[0].click();", E_comm_modules)
            print(f"E-comm module selected...{E_comm_modules.text}")
        time.sleep(0.5)

        #select pos_tab
        pos_tab = self.wait.until(EC.presence_of_element_located(StaffLocators.POS))
        pos_tab.click()
        
        #randomly select pos_module
        pos_module = get_random_pos_module()
        pos_modules = self.wait.until(EC.presence_of_element_located(StaffLocators.MODULES(pos_module)))
        try:
            pos_modules.click()
            print(f"Pos module selected...{pos_modules.text}")
        except:
            self.driver.execute_script("arguments[0].click();", pos_modules)
            print(f"Pos module selected...{pos_modules.text}")
        time.sleep(0.5)
        
        self._safe_click(StaffLocators.SUBMIT_PERMISSION_BTN)
        time.sleep(1)
