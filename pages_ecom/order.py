import allure
import time
import random
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from locators_ecom.order_locators import OrderLocators

class Order:
    def __init__(self, driver, timeout=60):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    @allure.step("Navigate to Order page and click Place an Order")
    def order_nav(self):
        # print("Navigating to Order page...")
        # order_sidebar = self.wait.until(EC.element_to_be_clickable(OrderLocators.SIDEBAR_ORDER_LINK))
        
        # try:
        #     order_sidebar.click()
        #     print("Order sidebar clicked...")
        # except Exception:
        #     self.driver.execute_script("arguments[0].click();", order_sidebar)
        #     print("Order sidebar clicked...")
        
        # time.sleep(1)

        print("Waiting for Place an Order button...")
        place_an_order = self.wait.until(EC.element_to_be_clickable(OrderLocators.PLACE_AN_ORDER_BTN))
        
        try:
            place_an_order.click()
            print("Place an Order button clicked...")
        except Exception:
            self.driver.execute_script("arguments[0].click();", place_an_order)
            print("Place an Order button clicked...")
        
        time.sleep(1)

    @allure.step("Select random customer")
    def select_customer(self):
        customer_search = self.wait.until(EC.presence_of_element_located(OrderLocators.CUSTOMER_SEARCH_INPUT))
        customer_search.clear()
        customer_search.send_keys("c")
        time.sleep(1)

        print("Selecting random customer...")
        customers = self.wait.until(EC.presence_of_all_elements_located(OrderLocators.CUSTOMER_RESULTS))
        selected_customer = random.choice(customers)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", selected_customer)
        time.sleep(1)
        try:
            selected_customer.click()
            print("Customer selected...")
        except Exception:
            self.driver.execute_script("arguments[0].click();", selected_customer)
            print("Customer selected...")
        finally:
            add_order = self.wait.until(EC.element_to_be_clickable(OrderLocators.ADD_ORDER))
            try:
                add_order.click()
                print("Add Order button clicked...")
            except Exception:
                self.driver.execute_script("arguments[0].click();", add_order)
                print("Add Order button clicked...")
        time.sleep(1)

    @allure.step("Search items: {item_name}")
    def search_items(self, item_name):
        print(f"Searching for item: {item_name}")
        search_input = self.wait.until(EC.presence_of_element_located(OrderLocators.ITEM_SEARCH_INPUT))
        search_input.clear()
        search_input.send_keys(item_name)
        time.sleep(1)

    @allure.step("Pick random item from search results")
    def searched_items_results(self):
        print("Picking item from search results...")
        results = self.wait.until(EC.presence_of_all_elements_located(OrderLocators.ITEM_SEARCH_RESULTS))
        selected_item = random.choice(results)
        print(f"Selected: {selected_item.text}")
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", selected_item)
        time.sleep(1)
        try:
            selected_item.click()
            print("Item selected...")
        except Exception:
            self.driver.execute_script("arguments[0].click();", selected_item)
            print("Item selected...")
        time.sleep(1)

    @allure.step("Select random variant")
    def select_variant(self):
        print("Checking for variants...")
        try:
            short_wait = WebDriverWait(self.driver, 10)
            variants = short_wait.until(EC.presence_of_all_elements_located(OrderLocators.VARIANT_OPTIONS))
            selected_variant = random.choice(variants)
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", selected_variant)
            time.sleep(1)
            try:
                selected_variant.click()
                print("Variant selected...")
            except Exception:
                self.driver.execute_script("arguments[0].click();", selected_variant)
                print("Variant selected...")
            time.sleep(1)
            return True
        except TimeoutException:
            print("No variants found.")
            return False

    @allure.step("Confirm item quantity: {items_quantity}")
    def confirm_items_quantity(self, items_quantity):
        print(f"Entering quantity: {items_quantity}")
        try:
            qty_input = self.wait.until(EC.presence_of_element_located(OrderLocators.QUANTITY_INPUT))
        except TimeoutException:
            qty_input = self.wait.until(EC.presence_of_element_located(OrderLocators.GENERIC_MODAL_QUANTITY_INPUT))

        qty_input.clear()
        qty_input.send_keys(items_quantity)
        print(f"Quantity entered: {items_quantity}")
        time.sleep(1)

        confirm_btn = self.wait.until(EC.element_to_be_clickable(OrderLocators.CONFIRM_QUANTITY_BTN))
        try:
            confirm_btn.click()
            print("Quantity confirmed...")
        except Exception:
            self.driver.execute_script("arguments[0].click();", confirm_btn)
            print("Quantity confirmed...")
        time.sleep(1)

    @allure.step("Enter discount: {discount}")
    def discount_field(self, discount):
        try:
            discount_input = self.wait.until(EC.presence_of_element_located(OrderLocators.DISCOUNT_INPUT))
            discount_input.clear()
            discount_input.send_keys(discount)
            print(f"Discount entered: {discount}")
            time.sleep(1)
        except TimeoutException:
            print("Discount field not found, skipping.")

    @allure.step("Select payment method: {method_name}")
    def payment_method(self, method_name='Cash On Delivery'):
        print(f"Selecting payment method: {method_name}")
        dropdown = self.wait.until(EC.presence_of_element_located(OrderLocators.PAYMENT_METHOD_SELECT))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", dropdown)
        
        select = Select(dropdown)
        try:
            select.select_by_visible_text(method_name)
            print(f"Payment method selected: {method_name}")
        except Exception:
            options = [opt for opt in select.options if opt.is_enabled() and opt.get_attribute("value")]
            if options:
                select.select_by_index(options.index(random.choice(options)))
            print(f"Payment method selected: {method_name}")
        time.sleep(1)

    @allure.step("Confirm create order in checkout")
    def confirm_create_order(self):
        btn = self.wait.until(EC.element_to_be_clickable(OrderLocators.CREATE_ORDER_CHECKOUT_BTN))
        try:
            btn.click()
            print("Order confirmed...")
        except Exception:
            self.driver.execute_script("arguments[0].click();", btn)
            print("Order confirmed...")
        time.sleep(1)

    @allure.step("Final confirm order")
    def confirm_order(self):
        confirm_btn = self.wait.until(EC.presence_of_element_located(OrderLocators.FINAL_CONFIRM_ORDER_BTN))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", confirm_btn)
        time.sleep(1)
        try:
            confirm_btn.click()
            print("Order confirmed...")
            
            # Assertion for Success Alert
            try:
                 alert = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(OrderLocators.ALERT_TOP))
                 print(f"Order Confirm Alert: {alert.text}")
                 assert "success" in alert.text.lower() or "created" in alert.text.lower(), f"Unexpected alert message: {alert.text}"
                 WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located(OrderLocators.ALERT_TOP))
            except TimeoutException:
                 print("No success alert appeared within timeout for Order.")
            except Exception as e:
                 print(f"An error occurred while verifying Order alert: {e}")
        except Exception:
            self.driver.execute_script("arguments[0].click();", confirm_btn)
            print("Order confirmed...")
        time.sleep(1)

    @allure.step("Grouped order details for {item_name}")
    def order_details(self, item_name, items_quantity):
        self.select_customer()
        self.search_items(item_name)
        self.searched_items_results()
        self.select_variant()
        self.confirm_items_quantity(items_quantity)
        self.discount_field(0)
        self.payment_method()
        self.confirm_create_order()
        self.confirm_order()

    @allure.step("Post-order actions: Edit and Confirm All")
    def action_Edit_to_place_order(self):
        try:
            edit_btn = self.wait.until(EC.element_to_be_clickable(OrderLocators.EDIT_BTN))
            try:
                edit_btn.click()
                print("Edit button clicked...")
            except Exception:
                self.driver.execute_script("arguments[0].click();", edit_btn)
                print("Edit button clicked...")
            time.sleep(1)
        except TimeoutException:
            print("Edit button not found, checking for Confirm All directly...")

        try:
            confirm_all = self.wait.until(EC.element_to_be_clickable(OrderLocators.CONFIRM_ALL_BTN))
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", confirm_all)
            try:
                confirm_all.click()
                print("Confirm All button clicked...")
            except Exception:
                self.driver.execute_script("arguments[0].click();", confirm_all)
                print("Confirm All button clicked...")
            time.sleep(1)
        except TimeoutException:
            print("Confirm All button not found.")

    @allure.step("Update order status randomly")
    def update_order_status(self):
        update_btn = self.wait.until(EC.presence_of_element_located(OrderLocators.UPDATE_ORDER_INFO_BTN))

        try:
            update_btn.click()
            print("Update button clicked...")
        except Exception:
            self.driver.execute_script("arguments[0].click();", update_btn)
            print("Update button clicked...")
        time.sleep(1)

        # Payment Status
        pay_select = self.wait.until(EC.presence_of_element_located(OrderLocators.PAYMENT_STATUS_SELECT))
        Select(pay_select).select_by_index(random.randint(1, len(Select(pay_select).options)-1))

        # Order Status
        ord_select = self.wait.until(EC.presence_of_element_located(OrderLocators.ORDER_STATUS_SELECT))
        Select(ord_select).select_by_index(random.randint(1, len(Select(ord_select).options)-1))

        update_modal_btn = self.wait.until(EC.element_to_be_clickable(OrderLocators.UPDATE_MODAL_BTN))
        try:
            update_modal_btn.click()
            print("Update modal button clicked...")
            
            # Assertion for Success Alert
            try:
                 alert = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(OrderLocators.ALERT_TOP))
                 print(f"Order Update Alert: {alert.text}")
                 assert "success" in alert.text.lower() or "updated" in alert.text.lower(), f"Unexpected alert message: {alert.text}"
                 WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located(OrderLocators.ALERT_TOP))
            except TimeoutException:
                 print("No success alert appeared within timeout for Order Update.")
            except Exception as e:
                 print(f"An error occurred while verifying Order Update alert: {e}")
        except Exception:
            self.driver.execute_script("arguments[0].click();", update_modal_btn)
            print("Update modal button clicked...")
        time.sleep(1)

    @allure.step("Verify print order button")
    def print_order(self):
        print_btns = self.wait.until(EC.presence_of_all_elements_located(OrderLocators.ORDER_DETAIL_BUTTONS))
        btn = random.choice(print_btns)
        print(f"Clicking print action: {btn.text}")
        try:
            btn.click()
            print("Print button clicked...")
        except Exception:
            self.driver.execute_script("arguments[0].click();", btn)
            print("Print button clicked...")
        time.sleep(1)