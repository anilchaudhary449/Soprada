from selenium.webdriver.common.by import By

class PluginsLocators:
    # Plugins List
    PLUGINS_DROPDOWN = (By.XPATH, "//div[contains(@class,'plugins-tools')]/div[@class='plugins-dropdown']")
    DROPDOWN_OPTIONS = (By.XPATH, "//option[not(@value='All Plugins')]")
    INSTALL_BTNS = (By.XPATH, "//button[normalize-space()='Install']")
    
    # Activation Modal
    CONFIRM_BTN = (By.XPATH, "//button[normalize-space(text())='Confirm']")
    VALIDATION_ERROR_MSG = (By.XPATH, "//div[contains(@class,'text-danger')]")
