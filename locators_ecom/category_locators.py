from selenium.webdriver.common.by import By

class CategoryLocators:
    # Sidebar
    SIDEBAR_CATEGORY = (By.XPATH, "//div[@class='sidebar__menu-section']/following::span[text()='Category']")
    
    # Category List
    ADD_NEW_CATEGORY_BTN = (By.XPATH, "//button[contains(@class,'btn') and normalize-space()='Add New Category']")
    ALERT_TOP = (By.XPATH, "//div[@class='alert-wrapper alert-wrapper--top']")
    
    # Modals (General)
    ACTIVE_MODAL = (By.XPATH, "//div[contains(@class, 'modal--active')]")
    
    # Add/Edit Category Form
    TITLE_INPUT = (By.XPATH, "(//input[contains(@type,'text') and starts-with(@placeholder,'Enter')])[last()]")
    IMAGE_FILE_INPUT = (By.XPATH, "//div[starts-with(@class,'category-image-select')]//input[@type='file']")
    SEO_SETTING_TAB = (By.XPATH, "(//div[@class='px-0']/div)[last()]")
    TAXONOMY_INPUT = (By.XPATH, "(//input[starts-with(@placeholder,'eg.') and @type='text'])[last()]")
    META_DESC_INPUT = (By.XPATH, "(//textarea[starts-with(@placeholder,'Meta') ])[last()]")
    ADD_CATEGORY_SUBMIT_BTN = (By.XPATH, "//div[contains(@class,'modal--active')]//descendant::button[starts-with(@class,'btn') and text()='Add Category']")
    UPDATE_CATEGORY_SUBMIT_BTN = (By.XPATH, "//button[starts-with(@class,'btn') and text()='Update']")
    
    # Sub-category List
    ADD_SUB_CATEGORY_BTNS = (By.XPATH, "//tr[@data-level='0']//button[contains(@class,'btn--ghost') and @title='Add']")
    EDIT_SUB_CATEGORY_BTNS = (By.XPATH, "//tr[@data-level='1' or @data-level='2' or @data-level='3']//button[contains(@class,'btn--ghost') and @title='Edit']")
    DELETE_SUB_CATEGORY_BTNS = (By.XPATH, "//tr[contains(@data-level,'1') or contains(@data-level,'2') or contains(@data-level,'3')]//button[@title='Delete']")
    DELETE_CATEGORY_BTNS = (By.XPATH, "//tr[@data-level='0']//button[contains(@class,'btn--ghost') and @title='Delete']")
    
    # Sub-category Form
    ADD_SUB_CATEGORY_SUBMIT_BTN = (By.XPATH, "//button[starts-with(@class,'btn') and text()='Add Subcategory']")
    SUB_CATEGORY_FILE_INPUT = (By.XPATH, "(//input[@type='file'])[last()]")
    
    # Confirmation Modals
    CONFIRM_DELETE_SUB_BTN = (By.XPATH, "//button[contains(@class,'premium-btn')]/following::span[text()='Delete Sub-category']")
    CONFIRM_DELETE_CAT_BTN = (By.XPATH, "//button[contains(@class,'premium-btn')]/following::span[text()='Delete Category']")
