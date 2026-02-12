from selenium.webdriver.common.by import By

class PaymentsLocators:
    # Payment Settings Cards
    CASH_ON_DELIVERY_CARD = (By.XPATH, "(//div[contains(@class,'payment-type-settings')])[1]")
    ALERT_TOP = (By.XPATH, "//div[@class='alert-wrapper alert-wrapper--top']")
    MANUAL_PAYMENT_CARD = (By.XPATH, "(//div[contains(@class,'payment-type-settings')])[2]")
    
    # Cash on Delivery Modal
    COD_STATUS_SELECT = (By.XPATH, "(//select[contains(@class,'szi-input__control')])[1]")
    COD_UPDATE_BTN = (By.XPATH, "(//div[contains(@class,'modal__footer')])[1]/button[text()='Update']")
    
    # Manual Payment Modal
    MANUAL_STATUS_SELECT = (By.XPATH, "(//select[contains(@class,'szi-input__control')])[2]")
    MANUAL_QR_FILE_INPUT = (By.XPATH, "//div[contains(@class,'blog-image-select')]//input[@type='file']")
    MANUAL_UPDATE_BTN = (By.XPATH, "(//div[contains(@class,'modal__footer')])[2]/button[text()='Update']")
