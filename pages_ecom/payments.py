import allure
import time
import random
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from locators_ecom.payments_locators import PaymentsLocators

class Payments:
    def __init__(self, driver, timeout=60):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout)

    @allure.step("Configure Cash on Delivery payment")
    def payments_cash_on_delivery(self, status='Yes'):
        print("Configuring Cash on Delivery...")
        cash_on_delivery = self.wait.until(EC.element_to_be_clickable(PaymentsLocators.CASH_ON_DELIVERY_CARD))
        
        try:
            cash_on_delivery.click()
            print("Cash on Delivery clicked...")
        except Exception:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", cash_on_delivery)
            self.driver.execute_script("arguments[0].click();", cash_on_delivery)
            print("Cash on Delivery clicked...")
        
        time.sleep(1)

        status_select_elem = self.wait.until(EC.presence_of_element_located(PaymentsLocators.COD_STATUS_SELECT))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", status_select_elem)
        time.sleep(1)
        
        select = Select(status_select_elem)
        try:
            select.select_by_value(status)
            print(f"Status selected: {status}")
        except Exception:
            select.select_by_index(0)
            print(f"Status selected: {status}")

        update_btn = self.wait.until(EC.element_to_be_clickable(PaymentsLocators.COD_UPDATE_BTN))
        try:
            update_btn.click()
            print("Update button clicked...")
        except Exception:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", update_btn)
            self.driver.execute_script("arguments[0].click();", update_btn)
        
        # Assertion for Success Alert
        try:
             alert = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(PaymentsLocators.ALERT_TOP))
             print(f"COD Update Alert: {alert.text}")
             assert "success" in alert.text.lower() or "updated" in alert.text.lower(), f"Unexpected alert message: {alert.text}"
             WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located(PaymentsLocators.ALERT_TOP))
        except TimeoutException:
             print("No success alert appeared within timeout for COD Update.")
        except Exception as e:
             print(f"An error occurred while verifying COD alert: {e}")

    @allure.step("Configure Manual Payment with QR: {QR_image}")
    def payments_manual_payment(self, QR_image):
        print("Configuring Manual Payment...")
        manual_payment = self.wait.until(EC.element_to_be_clickable(PaymentsLocators.MANUAL_PAYMENT_CARD))
        
        try:
            manual_payment.click()
            print("Manual Payment clicked...")
        except Exception:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", manual_payment)
            self.driver.execute_script("arguments[0].click();", manual_payment)
            print("Manual Payment clicked...")
        
        time.sleep(1)

        status_select_elem = self.wait.until(EC.presence_of_element_located(PaymentsLocators.MANUAL_STATUS_SELECT))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", status_select_elem)
        time.sleep(1)
        
        select = Select(status_select_elem)
        options = [opt for opt in select.options if opt.get_attribute("value")]
        if options:
            select.select_by_visible_text(random.choice(options).text)
        time.sleep(0.5)

        # Upload manual payment QR
        manual_payment_QR = self.wait.until(EC.presence_of_element_located(PaymentsLocators.MANUAL_QR_FILE_INPUT))
        manual_payment_QR.send_keys(QR_image)
        time.sleep(1)

        update_btn = self.wait.until(EC.element_to_be_clickable(PaymentsLocators.MANUAL_UPDATE_BTN))
        try:
            update_btn.click()
            print("Update button clicked...")
        except Exception:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", update_btn)
            self.driver.execute_script("arguments[0].click();", update_btn)
        
        # Assertion for Success Alert
        try:
             alert = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(PaymentsLocators.ALERT_TOP))
             print(f"Manual Payment Update Alert: {alert.text}")
             assert "success" in alert.text.lower() or "updated" in alert.text.lower(), f"Unexpected alert message: {alert.text}"
             WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located(PaymentsLocators.ALERT_TOP))
        except TimeoutException:
             print("No success alert appeared within timeout for Manual Payment Update.")
        except Exception as e:
             print(f"An error occurred while verifying Manual Payment alert: {e}")
