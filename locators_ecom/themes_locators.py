from selenium.webdriver.common.by import By

class ThemesLocators:
    # Theme Selection
    EDIT_THEME_BTN = (By.XPATH, "//button[normalize-space(text())='Edit']")
    APPLY_THEME_BTNS = (By.XPATH, "//div[@class='theme-category-button d-flex']//button[normalize-space()='Apply']")
    CONFIRM_APPLY_THEME_BTN = (By.XPATH, "//button[normalize-space()='Apply Theme']")
