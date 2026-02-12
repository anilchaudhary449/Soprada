from selenium.webdriver.common.by import By

class SlidersLocators:
    # Sidebar/Add New Slider
    ADD_NEW_SLIDER_BTN = (By.XPATH, "//span[contains(text(), 'Add New Slider')]")
    ALERT_TOP = (By.XPATH, "//div[@class='alert-wrapper alert-wrapper--top']")
    
    # Form Fields
    SLIDER_IMAGE_INPUT = (By.XPATH, "//input[@type='file']")
    TITLE_INPUT = (By.XPATH, "//input[@type='text' and @placeholder='Enter slider title']")
    SUBTITLE_INPUT = (By.XPATH, "//input[@type='text' and @placeholder='Enter slider subtitle']")
    DESCRIPTION_TEXTAREA = (By.XPATH, "//textarea[@placeholder='Enter slider description']")
    ACTION_LINK_NAME_INPUT = (By.XPATH, "//input[contains(@placeholder,'Shop')]")
    ACTION_LINK_URL_INPUT = (By.XPATH, "//input[contains(@placeholder,'products')]")
    SAVE_SLIDER_BTN = (By.XPATH, "//span[text()='Save Slider'] | //span[text()='Update Slider'] | //button[contains(text(), 'Update')] | //button[contains(text(), 'Save')]")
    
    # List Actions
    STATUS_DROPDOWNS = (By.XPATH, "//div[contains(@class,'slider-type')]/following::select[contains(@class,'szi-input__control')]")
    DROPDOWN_OPTIONS = (By.XPATH, "//select[contains(@class,'szi-input')]/option[not(@disabled)]")
    EDIT_BTNS = (By.XPATH, "//div[contains(@class,'slider-type')]//span[text()='Edit']")
    DELETE_BTNS = (By.XPATH, "//button[normalize-space()='Delete']")
    CONFIRM_DELETE_BTN = (By.XPATH, "//button[normalize-space()='Confirm']")
