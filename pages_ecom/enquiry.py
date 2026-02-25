import allure
import time
import random
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
        status_replied_elements = self.driver.find_elements(*EnquiryLocators.REPLIED_STATUS_BADGE)

        if status_replied_elements:
            print("Status is: Replied. Executing Replied flow (L12 -> L13 -> L15 -> L16).")
            # Click L12 (EDIT_REPLY_BTN)
            edit_enquiry_btns = self.wait.until(EC.presence_of_all_elements_located(EnquiryLocators.EDIT_REPLY_BTN))
            edit_enquiry_btn = random.choice(edit_enquiry_btns)
            try:
                edit_enquiry_btn.click()
                print("Edit button (L12) clicked...")
            except Exception:
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", edit_enquiry_btn)
                self.driver.execute_script("arguments[0].click();", edit_enquiry_btn)
                print("Edit button (L12) clicked via JS...")
            
            time.sleep(1)
            # Click L13 (EDIT_BTN)
            edit_btn = self.wait.until(EC.presence_of_element_located(EnquiryLocators.EDIT_BTN))
            try:
                edit_btn.click()
                print("Internal Edit button (L13) clicked...")
            except Exception:
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", edit_btn)
                self.driver.execute_script("arguments[0].click();", edit_btn)
                print("Internal Edit button (L13) clicked via JS...")
            
            time.sleep(1)
            # Enter message in L15 (REPLY_TEXTAREA)
            try:
                text_input = self.wait.until(EC.element_to_be_clickable(EnquiryLocators.REPLY_TEXTAREA))
                text_input.click()
                text_input.clear()
                text_input.send_keys(reply_message)
                print("Reply message (L15) entered...")
            except Exception:
                print("Direct typing failed for Replied flow, attempting JavaScript input...")
                text_input = self.wait.until(EC.presence_of_element_located(EnquiryLocators.REPLY_TEXTAREA))
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", text_input)
                self.driver.execute_script("arguments[0].value = '';", text_input)
                self.driver.execute_script(f"arguments[0].value = '{reply_message}';", text_input)
                self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", text_input)
                self.driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", text_input)
                print("Reply message (L15) entered via JS...")

            time.sleep(1)
            # Click L16 (SUBMIT_REPLY_BTN)
            send_btn = self.wait.until(EC.presence_of_element_located(EnquiryLocators.SUBMIT_REPLY_BTN))
            assert send_btn.is_enabled(), "Submit button isn't enabled."
            try:
                send_btn.click()
                print("Submit button (L16) clicked...")
            except Exception:
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", send_btn)
                self.driver.execute_script("arguments[0].click();", send_btn)
                print("Submit button (L16) clicked via JS...")
        else:
            # Check if status is 'Pending'
            print("Status is: Pending. Executing Pending flow (L12 -> L15 -> L16).")
            self.wait.until(EC.presence_of_all_elements_located(EnquiryLocators.PENDING_STATUS_BADGE))
            
            edit_enquiry_btns = self.wait.until(EC.presence_of_all_elements_located(EnquiryLocators.EDIT_REPLY_BTN))
            edit_enquiry_btn = random.choice(edit_enquiry_btns)
            
            try:
                edit_enquiry_btn.click()
                print("Edit button clicked...")
            except Exception:
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", edit_enquiry_btn)
                self.driver.execute_script("arguments[0].click();", edit_enquiry_btn)
                print("Edit button clicked...")
            
            time.sleep(1)
            try:
                text_input = self.wait.until(EC.element_to_be_clickable(EnquiryLocators.REPLY_TEXTAREA))
                text_input.click()
                text_input.clear()
                text_input.send_keys(reply_message)
                print("Reply message entered...")
            except Exception:
                print("Direct typing failed, attempting JavaScript input...")
                text_input = self.wait.until(EC.presence_of_element_located(EnquiryLocators.REPLY_TEXTAREA))
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", text_input)
                self.driver.execute_script("arguments[0].value = '';", text_input)
                self.driver.execute_script(f"arguments[0].value = '{reply_message}';", text_input)
                # Trigging input/change events for frameworks that monitor the field
                self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", text_input)
                self.driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", text_input)
                print("Reply message entered via JS...")
            
            time.sleep(1)

            send_btn = self.wait.until(EC.element_to_be_clickable(EnquiryLocators.SUBMIT_REPLY_BTN))
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

        