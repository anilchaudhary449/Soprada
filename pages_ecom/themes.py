import allure
import random
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators_ecom.themes_locators import ThemesLocators

class Themes:
    def __init__(self, driver, timeout=60):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout)

    @allure.step("Apply a random theme")
    def apply_random_theme(self):
        print("Applying a random theme...")
        
        # Scroll to theme section
        edit_btn = self.wait.until(EC.presence_of_element_located(ThemesLocators.EDIT_THEME_BTN))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", edit_btn)
        time.sleep(2)

        # Select random theme
        apply_btns = self.wait.until(EC.presence_of_all_elements_located(ThemesLocators.APPLY_THEME_BTNS))
        
        if apply_btns:
            target_btn = random.choice(apply_btns)
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", target_btn)
            time.sleep(1)
            
            try:
                target_btn.click()
                print("Theme 'Apply' button clicked...")
            except Exception:
                self.driver.execute_script("arguments[0].click();", target_btn)
                print("Theme 'Apply' button clicked...")
            
            time.sleep(2)

            # Confirm theme application
            confirm_btn = self.wait.until(EC.element_to_be_clickable(ThemesLocators.CONFIRM_APPLY_THEME_BTN))
            try:
                confirm_btn.click()
                print("Theme 'Confirm Apply' button clicked...")
            except Exception:
                self.driver.execute_script("arguments[0].click();", confirm_btn)
                print("Theme 'Confirm Apply' button clicked...")
            
            print("Theme applied successfully")
            time.sleep(2)
        else:
            print("No themes available to apply")

