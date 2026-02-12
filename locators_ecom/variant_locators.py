from selenium.webdriver.common.by import By

class VariantLocators:
    # Color Section
    ADD_NEW_COLOR_BTN = (By.XPATH, "//span[normalize-space(text())='Add New Color'] | //button[normalize-space(.)='Add New Color']")
    COLOR_TITLE_INPUT = (By.XPATH, "//input[starts-with(@placeholder,'Enter color title') and contains(@type,'text')]")
    COLOR_HEX_INPUT = (By.XPATH, "//input[@id='variant_color_hex']")
    CREATE_COLOR_BTN = (By.XPATH, "//div[contains(@class,'modal--active')]//button[normalize-space(.)='Create Color' or normalize-space(text())='Create Color']")
    
    # Size Section
    ALL_SIZES_TAB = (By.XPATH, "//div[normalize-space(text())='All Sizes']")
    ADD_NEW_SIZE_BTN = (By.XPATH, "//div[normalize-space(.)='Add New Size' and contains(@class,'gap-x-2')]")
    SIZE_TYPE_DROPDOWN = (By.XPATH, "//select[contains(@class,'szi-input__control')]")
    SIZE_VALUE_INPUT = (By.XPATH, "//input[starts-with(@placeholder,'Enter size title')] | //input[starts-with(@placeholder,'Enter color title')]")
    CREATE_SIZE_BTN = (By.XPATH, "//div[contains(@class,'modal--active')]//button[normalize-space(.)='Create Size']")
    
    # Common
    ACTIVE_MODAL = (By.XPATH, "//div[contains(@class,'modal--active')]")
