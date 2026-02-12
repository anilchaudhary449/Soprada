from selenium.webdriver.common.by import By

class SidebarLocators:
    ACTIVE_MODAL = (By.XPATH, "//div[contains(@class,'modal--active')]")
    SIDEBAR_ITEM = lambda text: (By.XPATH, \
        f"//div[contains(@class,'relative flex gap-x-7')]//a[normalize-space(text())='{text}']")
