from selenium.webdriver.common.by import By

class OrderLocators:
    # Sidebar & Header
    SIDEBAR_ORDER_LINK = (By.XPATH, "//div[contains(@class,'sidebar__menu-section')]//descendant::span[text()='Orders']")
    ALERT_TOP = (By.XPATH, "//div[@class='alert-wrapper alert-wrapper--top']")
    PLACE_AN_ORDER_BTN = (By.XPATH, "//div[contains(@class,'gap-x-2') and normalize-space(.)='Place an Order']")
    
    # Customer Selection
    CUSTOMER_SEARCH_INPUT = (By.XPATH, "(//input[@placeholder='Search customer...'])[last()]")
    CUSTOMER_RESULTS = (By.XPATH, "//div[@class='grow']")
    ADD_ORDER = (By.XPATH, "//button[normalize-space(text())='Add Order']")
    
    # Item Search & Selection
    ITEM_SEARCH_INPUT = (By.XPATH, "//input[contains(@type,'text') and starts-with(@placeholder,'Search')]")
    ITEM_SEARCH_RESULTS = (By.XPATH, "//div[starts-with(@class,'product-search-show')] | //div[contains(@class,'product-select-item')]")
    
    # Variants & Quantity
    VARIANT_OPTIONS = (By.XPATH, "//div[starts-with(@class,'sku-variant-item')]")
    QUANTITY_INPUT = (By.XPATH, "//input[contains(@type,'number') and (contains(@min,'1'))]")
    GENERIC_MODAL_QUANTITY_INPUT = (By.XPATH, "//div[contains(@class,'modal')]//input[@type='number']")
    CONFIRM_QUANTITY_BTN = (By.XPATH, "//button[normalize-space(.)='Confirm']")
    
    # Checkout Details
    DISCOUNT_INPUT = (By.XPATH, "//label[normalize-space(text())='Discount']/following-sibling::input[@placeholder='Enter number']")
    PAYMENT_METHOD_SELECT = (By.XPATH, "//select[@placeholder='Select a Payment method']")
    CREATE_ORDER_CHECKOUT_BTN = (By.XPATH, "//button[normalize-space()='Create Order' and (contains(@class,'mt-6'))]")
    FINAL_CONFIRM_ORDER_BTN = (By.XPATH, "//button[normalize-space(.)='Create Order' and not(contains(@class,'mt-6'))] | //div[@class='create-order-button mt-8']//button[normalize-space(text())='Create Order']")
    
    # Order List/Detail Actions
    EDIT_BTN = (By.XPATH, "//a[@title='View Product'] | //td[contains(@class,'data__table-body')]//a")
    CONFIRM_ALL_BTN = (By.XPATH, "//button[contains(@class,'btn bg-success') and (normalize-space(text())='Confirm All')]")
    UPDATE_ORDER_INFO_BTN = (By.XPATH, "//div[starts-with(@class,'order-detail-buttons')]/child::button[normalize-space(text())='Update Order Information']")
    
    # Status Update Modal
    PAYMENT_STATUS_SELECT = (By.XPATH, "//select[@name='payment_status']")
    PAYMENT_STATUS_OPTIONS = (By.XPATH, "//select[@name='payment_status']/child::option[not(@disabled)]")
    ORDER_STATUS_SELECT = (By.XPATH, "//select[@name='order_status']")
    ORDER_STATUS_OPTIONS = (By.XPATH, "//select[@name='order_status']/child::option[not(@disabled)]")
    UPDATE_MODAL_BTN = (By.XPATH, "//div[@class='modal__footer']/child::button[normalize-space(text())='Update']")
    
    # Print/Invoice
    ORDER_DETAIL_BUTTONS = (By.XPATH, "//div[contains(@class,'order-detail-buttons')]/child::button")
