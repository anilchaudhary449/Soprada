from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators_ecom.inventory_management_locators import InventoryManagementLocators


class InventoryManagement:

    def __init__(self, driver, timeout=120):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout)
    
    def inventory_management(self):
        low_stocks = self.wait.until(EC.element_to_be_clickable((InventoryManagementLocators.LOW_STOCKS)))
        try:
            low_stocks.click()
        except:
            self.driver.execute_script("arguments[0].click();",low_stocks)
        
        adjust_stocks = self.wait.until(EC.element_to_be_clickable((InventoryManagementLocators.ADJUST_STOCKS)))
        try:
            adjust_stocks.click()
        except:
            self.driver.execute_script("arguments[0].click();",adjust_stocks)
        
    