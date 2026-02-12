from selenium.webdriver.common.by import By

class InventoryManagementLocators:
    #low stocks
    LOW_STOCKS = (By.XPATH,"//button[normalize-space(.)='Low Stock']")

    #adjust stocks
    ADJUST_STOCKS = (By.XPATH,"//button[normalize-space(.)='Adjust Stock']")