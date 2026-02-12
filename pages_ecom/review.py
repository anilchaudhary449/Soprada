import allure
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators_ecom.review_locators import ReviewLocators

class Review:
    def __init__(self, driver, timeout=60):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout) 

    @allure.step("Toggle review visibility status")
    def toggle_review_visibility(self):
        print("Toggling review visibility...")
        toggle = self.wait.until(EC.element_to_be_clickable(ReviewLocators.SWITCH_TOGGLE))
        try:
            toggle.click()
            print("Review visibility toggled...")
        except Exception:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", toggle)
            self.driver.execute_script("arguments[0].click();", toggle)
            print("Review visibility toggled...")
        
        # Handles alert if present after update
        try:
            alert = self.wait.until(EC.visibility_of_element_located(ReviewLocators.SUCCESS_ALERT))
            print(f"Review Visibility Alert: {alert.text}")
        except Exception:
            print("No visible alert found after toggling review.")
            
        time.sleep(2)

        
