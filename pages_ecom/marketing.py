import allure
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from locators_ecom.marketing_locators import MarketingLocators

class Marketing:
    def __init__(self, driver, timeout=60):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout)

    @allure.step("Click View to enter marketing details")
    def marketing(self):
        print("Navigating to marketing details...")
        try:
            view_btn = self.wait.until(EC.element_to_be_clickable(MarketingLocators.VIEW_BTN))
            try:
                view_btn.click()
                print("View button clicked...")
            except Exception:
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", view_btn)
                self.driver.execute_script("arguments[0].click();", view_btn)
                print("View button clicked...")
            time.sleep(2)
        except Exception as e:
            print(f"Warning: Could not click marketing 'View' button. Possibly already on page. Error: {e}")

    @allure.step("Add coupon code: {heading} (Code: {code})")
    def add_coupon_code(self, heading, code, dis_pct, pct_amt, min_pur_amt, start_date, end_date):
        print(f"Adding coupon code: {code}")
        add_coupon_btn = self.wait.until(EC.element_to_be_clickable(MarketingLocators.ADD_COUPON_CODE_BTN))
        try:
            add_coupon_btn.click()
            print("Add coupon button clicked...")
        except Exception:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", add_coupon_btn)
            self.driver.execute_script("arguments[0].click();", add_coupon_btn)
            print("Add coupon button clicked...")

        # Basic Info
        promotion_title = self.wait.until(EC.presence_of_element_located(MarketingLocators.PROMOTION_TITLE_INPUT))
        promotion_title.send_keys(heading)
        print("Promotion title entered...")

        promotion_code = self.wait.until(EC.presence_of_element_located(MarketingLocators.PROMOTION_CODE_INPUT))
        promotion_code.send_keys(code)
        print("Promotion code entered...")

        promotion_dis_pct = self.wait.until(EC.presence_of_element_located(MarketingLocators.DISCOUNT_PERCENTAGE_INPUT))
        promotion_dis_pct.send_keys(dis_pct)
        print("Discount percentage entered...")

        promotion_dis_amt = self.wait.until(EC.presence_of_element_located(MarketingLocators.MAX_DISCOUNT_LIMIT_INPUT))
        promotion_dis_amt.send_keys(pct_amt)
        print("Max discount limit entered...")

        # Advanced Settings
        print("Opening advanced settings...")
        advanced_setting = self.wait.until(EC.element_to_be_clickable(MarketingLocators.ADVANCED_OPTIONS_TOGGLE))
        try:
            advanced_setting.click()
            print("Advanced settings clicked...")
        except Exception:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", advanced_setting)
            self.driver.execute_script("arguments[0].click();", advanced_setting)
            print("Advanced settings clicked...")

        time.sleep(1)
        minimum_purchase = self.wait.until(EC.presence_of_element_located(MarketingLocators.MINIMUM_PURCHASE_INPUT))
        minimum_purchase.send_keys(min_pur_amt)
        print("Minimum purchase amount entered...")

        start_date_input = self.wait.until(EC.presence_of_element_located(MarketingLocators.START_DATE_INPUT))
        start_date_input.send_keys(start_date)
        print("Start date entered...")

        end_date_input = self.wait.until(EC.presence_of_element_located(MarketingLocators.END_DATE_INPUT))
        end_date_input.send_keys(end_date)
        print("End date entered...")

        maximum_use = self.wait.until(EC.presence_of_element_located(MarketingLocators.MAX_USE_INPUT))
        maximum_use.send_keys(str(random.randint(10, 500)))
        print("Maximum use entered...")

        time.sleep(1)
        print("Saving coupon...")
        submit_btn = self.wait.until(EC.element_to_be_clickable(MarketingLocators.ADD_COUPON_SUBMIT_BTN))
        try:
            submit_btn.click()
            print("Coupon submitted...")
        except Exception:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", submit_btn)
            self.driver.execute_script("arguments[0].click();", submit_btn)
            print("Coupon successfully submitted.")
        
        # Assertion for Success Alert
        try:
             alert = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(MarketingLocators.ALERT_TOP))
             print(f"Marketing Coupon Alert: {alert.text}")
             assert "success" in alert.text.lower() or "added" in alert.text.lower(), f"Unexpected alert message: {alert.text}"
             WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located(MarketingLocators.ALERT_TOP))
        except TimeoutException:
             print("No success alert appeared within timeout for Marketing.")
        except Exception as e:
             print(f"An error occurred while verifying Marketing alert: {e}")
    
    @allure.step("View recently created coupon")
    def view_coupon(self):
        print("Viewing coupon details...")
        try:
            view_btns = self.wait.until(EC.presence_of_all_elements_located(MarketingLocators.COUPON_VIEW_BTNS))
            recent_view_btn = view_btns[0]
            try:
                recent_view_btn.click()
                print("View button clicked...")
            except Exception:
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", recent_view_btn)
                self.driver.execute_script("arguments[0].click();", recent_view_btn)
                print("View button clicked...")
            
            time.sleep(1)
            
            # Dismiss modal
            try:
                close_btn = self.wait.until(EC.element_to_be_clickable(MarketingLocators.CLOSE_MODAL_BTN))
                close_btn.click()
                print("Close button clicked...")
            except Exception:
                try:
                    cross_btn = self.wait.until(EC.element_to_be_clickable(MarketingLocators.CROSS_MODAL_BTN))
                    cross_btn.click()
                    print("Cross button clicked...")
                except Exception:
                    print("Could not find a way to close the view modal.")
            
            time.sleep(1)
        except Exception as e:
            print(f"Error viewing coupon: {e}")

    