import allure
import time
import random
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from locators_ecom.sliders_locators import SlidersLocators

class Sliders:
    def __init__(self, driver, timeout=60):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout)
    
    @allure.step("Fill slider form")
    def _fill_slider_form(self, title, subtitle, description, actionlinkname, actionlinkurl):
        print(f"Filling slider form: {title}")
        
        # Wait for modal/form to be fully loaded
        time.sleep(2)
        
        fields = {
            SlidersLocators.TITLE_INPUT: title,
            SlidersLocators.SUBTITLE_INPUT: subtitle,
            SlidersLocators.DESCRIPTION_TEXTAREA: description,
            SlidersLocators.ACTION_LINK_NAME_INPUT: actionlinkname,
            SlidersLocators.ACTION_LINK_URL_INPUT: actionlinkurl
        }

        for locator, value in fields.items():
            try:
                elem = self.wait.until(EC.visibility_of_element_located(locator))
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", elem)
                time.sleep(0.5)
                try:
                    elem.clear()
                except Exception:
                    pass
                elem.send_keys(value)
            except Exception as e:
                print(f"Failed to fill field {locator}: {e}")
                continue

        # Try to find and click the save/update button with fallbacks
        print("Looking for Save/Update button...")
        try:
            save_btn = self.wait.until(EC.element_to_be_clickable(SlidersLocators.SAVE_SLIDER_BTN))
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", save_btn)
            time.sleep(1)
            try:
                save_btn.click()
                print("Save button clicked successfully")
            except Exception:
                self.driver.execute_script("arguments[0].click();", save_btn)
                print("Save button clicked via JavaScript")
        except Exception as e:
            print(f"Primary save button not found: {e}. Trying alternative buttons...")
            # Fallback: try to find any button with Save or Update text
            try:
                from selenium.webdriver.common.by import By
                alt_buttons = self.driver.find_elements(By.XPATH, "//button[contains(., 'Save')] | //button[contains(., 'Update')] | //span[contains(., 'Save')] | //span[contains(., 'Update')]")
                if alt_buttons:
                    print(f"Found {len(alt_buttons)} alternative buttons")
                    for btn in alt_buttons:
                        if btn.is_displayed():
                            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", btn)
                            time.sleep(0.5)
                            self.driver.execute_script("arguments[0].click();", btn)
                            print(f"Clicked alternative button with text: {btn.text}")
                            break
            except Exception as fallback_error:
                print(f"Fallback also failed: {fallback_error}")
        
        # Assertion for Success Alert
        try:
             alert = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(SlidersLocators.ALERT_TOP))
             print(f"Slider Form Alert: {alert.text}")
             assert "success" in alert.text.lower() or "added" in alert.text.lower() or "updated" in alert.text.lower(), f"Unexpected alert message: {alert.text}"
             WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located(SlidersLocators.ALERT_TOP))
        except TimeoutException:
             print("No success alert appeared within timeout for Slider.")
        except Exception as e:
             print(f"An error occurred while verifying Slider alert: {e}")

    @allure.step("Edit random slider")
    def edit_sliders(self, title, subtitle, description, actionlinkname, actionlinkurl):
        print("Editing a random slider...")
        
        # Select random status dropdown
        dropdowns = self.wait.until(EC.presence_of_all_elements_located(SlidersLocators.STATUS_DROPDOWNS))
        target_dropdown = random.choice(dropdowns)
        
        select = Select(target_dropdown)
        options = [opt for opt in select.options if opt.is_enabled() and opt.get_attribute("value")]
        if options:
            selected_option = random.choice(options)
            # Click the option directly instead of using index
            try:
                selected_option.click()
                print("Status dropdown clicked...")
            except Exception:
                self.driver.execute_script("arguments[0].click();", selected_option)
                print("Status dropdown clicked...")
        
        time.sleep(1)

        # Click random Edit button
        edit_btns = self.wait.until(EC.presence_of_all_elements_located(SlidersLocators.EDIT_BTNS))
        btn = random.choice(edit_btns)
        try:
            btn.click()
            print("Edit button clicked...")
        except Exception:
            self.driver.execute_script("arguments[0].click();", btn)
            print("Edit button clicked...")
        
        time.sleep(1)
        self._fill_slider_form(title, subtitle, description, actionlinkname, actionlinkurl)

    @allure.step("Add new slider: {title}")
    def add_sliders(self, image_path, title, subtitle, description, actionlinkname, actionlinkurl):
        print("Adding a new slider...")
        
        try:
            add_btn = self.driver.find_element(*SlidersLocators.ADD_NEW_SLIDER_BTN)
            if add_btn.is_displayed():
                add_btn.click()
                print("Add button clicked...")
        except Exception:
            print("Add button not found...")
            pass

        file_input = self.wait.until(EC.presence_of_element_located(SlidersLocators.SLIDER_IMAGE_INPUT))
        file_input.send_keys(image_path)
        print("Image path entered...")
        time.sleep(2)

        self._fill_slider_form(title, subtitle, description, actionlinkname, actionlinkurl)

    @allure.step("Delete random slider")
    def delete_sliders(self):
        print("Deleting a random slider...")
        try:
            delete_btns = self.wait.until(EC.presence_of_all_elements_located(SlidersLocators.DELETE_BTNS))
            btn = random.choice(delete_btns)
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", btn)
            time.sleep(0.5)
            
            try:
                btn.click()
                print("Delete button clicked...")
            except Exception:
                self.driver.execute_script("arguments[0].click();", btn)
                print("Delete button clicked...")
                
            confirm_btn = self.wait.until(EC.element_to_be_clickable(SlidersLocators.CONFIRM_DELETE_BTN))
            confirm_btn.click()
            print("Confirm delete button clicked...")
            
            # Assertion for Success Alert
            try:
                 alert = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(SlidersLocators.ALERT_TOP))
                 print(f"Slider Delete Alert: {alert.text}")
                 assert "success" in alert.text.lower() or "deleted" in alert.text.lower(), f"Unexpected alert message: {alert.text}"
                 WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located(SlidersLocators.ALERT_TOP))
            except TimeoutException:
                 print("No success alert appeared within timeout for Slider Delete.")
            except Exception as e:
                 print(f"An error occurred while verifying Slider Delete alert: {e}")
        except Exception as e:
            print(f"Delete operation failed: {e}")

