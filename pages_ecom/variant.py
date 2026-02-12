import allure
import time
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from resources.resources import get_random_size_and_type
from locators_ecom.variant_locators import VariantLocators

class Variant:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 60)
        
        # Verify we are on the correct page
        if "/variant" not in self.driver.current_url.lower():
            print(f"Warning: Expected /variant but on {self.driver.current_url}. Forcing navigation.")
            from pages_ecom.sidebar import Sidebar
            Sidebar(driver).navigate_to_variant()

    
    @allure.step("Add variant color: {color_name} ({color_hex})")
    def add_variant(self, color_name, color_hex):
        # Click "Add New Color"
        self.wait.until(EC.element_to_be_clickable(VariantLocators.ADD_NEW_COLOR_BTN)).click()

        # Enter Color Title
        enter_color_title = self.wait.until(EC.element_to_be_clickable(VariantLocators.COLOR_TITLE_INPUT))
        enter_color_title.clear()
        enter_color_title.send_keys(color_name)
        print("Color title entered...")

        # Select Color Hex
        select_color_hex = self.wait.until(EC.presence_of_element_located(VariantLocators.COLOR_HEX_INPUT))
        try:
            select_color_hex.click()
            print("Color hex selected...")
        except:
             self.driver.execute_script("arguments[0].click();", select_color_hex)
             
        select_color_hex.clear()
        select_color_hex.send_keys(color_hex)
        print("Color hex entered...")

        # Click Save
        self.wait.until(EC.element_to_be_clickable(VariantLocators.CREATE_COLOR_BTN)).click()
        print("Color saved...")
        
        # Wait for modal to close
        try:
            self.wait.until(EC.invisibility_of_element_located(VariantLocators.ACTIVE_MODAL))
        except:
            pass
        
        # Verify we're still on variant page
        if "/variant" not in self.driver.current_url.lower():
            print(f"WARNING: After saving color, redirected to {self.driver.current_url}. Re-navigating to Variant page...")
            from pages_ecom.sidebar import Sidebar
            Sidebar(self.driver).navigate_to_variant()
        
        time.sleep(1)

    @allure.step("Add random variant size")
    def add_sizes(self):
        # Verify we're on variant page
        if "/variant" not in self.driver.current_url.lower():
            print(f"ERROR: Not on variant page ({self.driver.current_url}). Cannot add sizes.")
            from pages_ecom.sidebar import Sidebar
            Sidebar(self.driver).navigate_to_variant()
        
        time.sleep(1)
        
        # Click 'All Sizes' button
        self.wait.until(EC.visibility_of_element_located(VariantLocators.ALL_SIZES_TAB)).click()
        print("All sizes tab clicked...")
        
        time.sleep(1) # Give it extra time to render the 'Add New Size' button

        # Click 'Add New Size'
        self.wait.until(EC.presence_of_element_located(VariantLocators.ADD_NEW_SIZE_BTN)).click()
        print("Add new size button clicked...")
        
        size_type, size_value = get_random_size_and_type()
        # Handling the Size Type Dropdown (Int/EU)
        try:
            standard_dropdown = self.wait.until(EC.presence_of_element_located(VariantLocators.SIZE_TYPE_DROPDOWN))
            select = Select(standard_dropdown)
            select.select_by_visible_text(size_type)
            print(f"Size type {size_type} selected...")
        except Exception as e:
            print(f"Failed to select size type '{size_type}': {e}")
            try:
                select = Select(self.driver.find_element(*VariantLocators.SIZE_TYPE_DROPDOWN))
                select.select_by_index(0)
                print("Size type selected by index...")
            except:
                pass

        # Enter Size Value
        enter_size_value = self.wait.until(EC.element_to_be_clickable(VariantLocators.SIZE_VALUE_INPUT))
        enter_size_value.clear()
        enter_size_value.send_keys(size_value)
        print("Size value entered...")    
        # Save Size
        self.wait.until(EC.element_to_be_clickable(VariantLocators.CREATE_SIZE_BTN)).click()
        print("Size saved...")
        
        time.sleep(1)
