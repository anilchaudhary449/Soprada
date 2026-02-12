import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators_ecom.enquiry_locators import EnquiryLocators

class Enquiry:
    def __init__(self, driver, timeout=60):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout)

    @allure.step("Mark all enquiries as seen")
    def mark_all_as_seen(self):
        # Wait for any lingering alerts (e.g. from previous tests) to disappear
        self.wait.until(EC.invisibility_of_element_located(EnquiryLocators.ALERT_VISIBLE))
        self.wait.until(EC.invisibility_of_element_located(EnquiryLocators.ALERT_TITLE))
        
        mark_as_seen = self.wait.until(EC.presence_of_element_located(EnquiryLocators.MARK_ALL_AS_SEEN_BTN))
        
        try:
            mark_as_seen.click()
            print("Mark all as seen button clicked...")
        except Exception as e:
            if "intercepted" in str(e).lower():
                print("Click intercepted, attempting JavaScript click...")
                self.driver.execute_script("arguments[0].click();", mark_as_seen)
                print("Mark all as seen button clicked...")
            else:
                raise e
        
        # Handles alert if present after update
        alert_message = self.wait.until(EC.visibility_of_element_located(EnquiryLocators.SUCCESS_ALERT))
        assert "Marked All as seen successfully" in alert_message.text, "Alert marked as seen message not found"
        time.sleep(2)

    @allure.step("Toggle enquiry status")
    def toggle_status(self):
        toggle_btn = self.wait.until(EC.presence_of_element_located(EnquiryLocators.TOGGLE_STATUS_BTN))
        assert toggle_btn.is_enabled(), "Toggle button isn't enabled."
        try:
            toggle_btn.click()
            print("Toggle button clicked...")
        except Exception:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", toggle_btn)
            self.driver.execute_script("arguments[0].click();", toggle_btn)
            print("Toggle button clicked...")
        
        # Handles alert if present after update
        alert_message = self.wait.until(EC.visibility_of_element_located(EnquiryLocators.SUCCESS_ALERT))
        print(f"Status Change Alert: {alert_message.text}")
        time.sleep(2)

    @allure.step("View and reply to enquiry")
    def view_enquiry(self, reply_message="Hello, this is a test message."):
        view_btn = self.wait.until(EC.presence_of_element_located(EnquiryLocators.VIEW_ENQUIRY_BTN))
        assert view_btn.is_enabled(), "View enquiry button isn't enabled."
        try:
            view_btn.click()
            print("View button clicked...")
        except Exception:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", view_btn)
            self.driver.execute_script("arguments[0].click();", view_btn)
            print("View button clicked...")
        
        time.sleep(2)

        # Check if status is 'Replied'
        status_elements = self.driver.find_elements(*EnquiryLocators.REPLID_STATUS_BADGE)
        if status_elements:
            print("Enquiry already replied. Clicking Edit button.")
            edit_enquiry = self.wait.until(EC.element_to_be_clickable(EnquiryLocators.EDIT_REPLY_BTN))
            try:
                edit_enquiry.click()
                print("Edit button clicked...")
            except Exception:
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", edit_enquiry)
                self.driver.execute_script("arguments[0].click();", edit_enquiry)
                print("Edit button clicked...")
            time.sleep(1)

        text_input = self.wait.until(EC.presence_of_element_located(EnquiryLocators.REPLY_TEXTAREA))
        text_input.clear()
        text_input.send_keys(reply_message)
        print("Reply message entered...")
        time.sleep(1)

        send_btn = self.wait.until(EC.presence_of_element_located(EnquiryLocators.SUBMIT_REPLY_BTN))
        assert send_btn.is_enabled(), "Submit button isn't enabled."
        try:
            send_btn.click()
            print("Submit button clicked...")
        except Exception:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", send_btn)
            self.driver.execute_script("arguments[0].click();", send_btn)
            print("Submit button clicked...")
        
        # Wait for success alert after reply
        # success_alert = self.wait.until(EC.visibility_of_element_located(EnquiryLocators.SUCCESS_ALERT))
        # assert "Replied" in success_alert.text or "successfully" in success_alert.text.lower()
        # time.sleep(2)

        