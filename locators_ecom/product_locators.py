from selenium.webdriver.common.by import By

class ProductLocators:
    # Product List
    ADD_PRODUCT_BTN = (By.XPATH, "//div[contains(@class,'flex')]//a[normalize-space()='Add Product']")
    ALERT_TOP = (By.XPATH, "//div[@class='alert-wrapper alert-wrapper--top']")
    
    # Add Product Form
    PRODUCT_NAME_INPUT = (By.XPATH, "//input[starts-with(@placeholder,'Enter Product Name...') and contains(@type,'text')]")
    
    # Category Selection
    CATEGORY_DROPDOWN_HEADER = (By.XPATH, "//div[@class='custom-select-header']//descendant::span")
    ADD_NEW_CATEGORY_OPTION = (By.XPATH, "//div[contains(@class,'add-option')]//descendant::span")
    NEW_CATEGORY_TITLE_TEXTAREA = (By.XPATH, "//div[contains(@class,'category-title-input')]//textarea[starts-with(@placeholder,'Enter new category')]")
    FILE_INPUT_GENERIC = (By.XPATH, "(//input[@type='file'])[last()]")
    FILE_INPUT_MAIN = (By.XPATH, "(//input[@type='file'])[1]")
    SEO_TAB = (By.XPATH, "(//div[@class='px-0']/div)[last()]")
    TAXONOMY_INPUT = (By.XPATH, "(//input[starts-with(@placeholder,'eg.') and @type='text'])[last()]")
    META_DESC_INPUT = (By.XPATH, "(//textarea[starts-with(@placeholder,'Meta') ])[last()]")
    SUBMIT_CATEGORY_BTN = (By.XPATH, "//button[starts-with(@class,'btn') and (text()='Add New Category' or text()='Add Category')]")
    ACTIVE_MODAL = (By.XPATH, "//div[contains(@class, 'modal--active')]")
    
    # Selects
    SALE_SELECT = (By.XPATH, "//select[@name='sale']")
    SALE_OPTIONS = (By.XPATH, "//select[@name='sale']/option[not(@disabled)]")
    ARRIVAL_SELECT = (By.XPATH, "//select[@name='arrival']")
    ARRIVAL_OPTIONS = (By.XPATH, "//select[@name='arrival']/option[not(@disabled)]")
    TYPE_SELECT = (By.XPATH, "//select[@name='type']")
    TYPE_VARIABLE_OPTION = (By.XPATH, "//select[contains(@name,'type')]/option[@value='variable']")
    
    # Description
    DESCRIPTION_EDITOR = (By.XPATH, "//div[starts-with(@data-placeholder,'Enter Product Description...')]")
    
    # Variant Management
    VARIANT_IMAGE_PLACEHOLDER = (By.XPATH, "//div[contains(@class,'image-holder') and contains(@class,'h-12')]")
    VARIANT_IMAGE_PLACEHOLDER_LAST = (By.XPATH, "(//div[contains(@class,'image-holder') and contains(@class,'h-12')])[last()]")
    IMAGE_FILE_INPUT_ID = (By.XPATH, "(//input[@type='file'])[last()]")
    VARIANT_DONE_BTN = (By.XPATH, "//button[contains(@class,'btn btn-pumpkin') and normalize-space(text())='Done']")
    MODAL_SAVE_BTN = (By.XPATH, "//div[contains(@class, 'modal--active')]//button[normalize-space(text())='Save' or normalize-space(text())='Add' or normalize-space(text())='Apply' or normalize-space(text())='Done']")
    MODAL_FILE_INPUT = (By.XPATH, "//div[contains(@class, 'modal--active')]//input[@type='file']")
    
    # Pricing & Stock
    MARKED_PRICE_INPUT = (By.XPATH, "(//div[contains(@class,'marked-price-input')]//input[@type='number'])[last()]")
    SELLING_PRICE_INPUT = (By.XPATH, "(//div[contains(@class,'selling-price-input')]//input[@type='number'])[last()]")
    QUANTITY_INPUT = (By.XPATH, "(//div[contains(@class,'available-stock-input')]//input[@type='number'])[last()]")
    DISCOUNT_INPUT = (By.XPATH, "(//div[contains(@class,'discount-input')]/child::input[contains(@class,'szi-input__control')])[last()]")
    
    # Size/Color Selection
    SIZE_SELECT_BTN = (By.XPATH, "(//div[contains(@class,'custom-select-header')]/child::span[contains(@class,'custom-select-value') and contains(text(),'Select Size')])[last()]")
    SIZE_OPTIONS = (By.XPATH, "//div[contains(@class,'custom-select-options')]//span[not(normalize-space(text())='Add New Size')]")
    COLOR_SELECT_BTN = (By.XPATH, "(//div[contains(@class,'custom-select-header')]/child::span[contains(@class,'custom-select-value') and contains(text(),'Select Color')])[last()]")
    COLOR_OPTIONS = (By.XPATH, "//div[contains(@class,'custom-select-options')]//span[not(normalize-space(text())='Add New Color')]")
    
    # Extra Variants
    ADD_VARIANT_LINK = (By.XPATH, "//div[starts-with(@class,'text-pumpkin') and normalize-space(text()='Add Variant')]")
    
    # Final Save
    SAVE_PRODUCT_BTN = (By.XPATH, "//button[normalize-space()='Save' and contains(@type,'button')]")
