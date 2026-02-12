from selenium.webdriver.common.by import By

class BlogLocators:
    # Blog List
    ADD_BLOG_BTN = (By.XPATH, "//a[contains(normalize-space(.),'New Blog')] | //a[contains(@href,'blog/add')]")
    BLOG_CATEGORY_BTN = (By.XPATH, "//a[contains(normalize-space(.),'Blog Category')] | //a[contains(@href,'blog/category')]")

    # Blog New/Add Category
    NEW_CATEGORY_BTN = (By.XPATH, "//button[.//span[normalize-space(.)='New Category']] | //span[normalize-space(.)='New Category']")
    CATEGORY_NAME_INPUT = (By.XPATH, "//input[@id='title'] | //input[@placeholder='Enter category title...']")
    SHORT_DESCRIPTION_INPUT = (By.XPATH, "//textarea[@id='short_description'] | //textarea[@placeholder='Enter category short description...']")    
    SAVE_CATEGORY_BTN = (By.XPATH, "//button[normalize-space(.)='Create Blog Category' or .//span[normalize-space(.)='Create Blog Category']]")

    # Blog Category Action
    EDIT_CATEGORY_BTNS = (By.XPATH, "//button[@title='Edit Blog'] | //button[descendant::*[@title='Edit Blog']]")
    DELETE_CATEGORY_BTNS = (By.XPATH, "//button[@title='Delete Blog'] | //button[descendant::*[@title='Delete Blog']]")

    # Blog Category Update
    UPDATE_CATEGORY_BTN = (By.XPATH, "//button[normalize-space(.)='Update Blog Category']")
 
    # Blog Category Delete
    CONFIRM_DELETE_CATEGORY_BTN = (By.XPATH, "//button[normalize-space(.)='Delete Category']")
    
    # Blog
    VIEW_BTNS = (By.XPATH, "//button[@title='View Blog'] | //td[@class='data__table-body']//button[@type='button' and @title='View Blog']")
    EDIT_BTNS = (By.XPATH, "//a[@title='Edit Blog'] | //button[@title='Edit Blog'] | //a[contains(@href, 'edit')]")
    DELETE_BTNS = (By.XPATH, "//button[@title='Delete Blog'] | //button[descendant::*[@title='Delete Blog']]")
    
    # Add/Edit Blog Form
    TITLE_INPUT = (By.XPATH, "//input[@id='blog_title'] | //input[@placeholder='Enter blog title...']")
    IMAGE_FILE_INPUT = (By.XPATH, "//input[@id='blog_image' and @type='file'] | //input[@type='file']")
    AUTHOR_INPUT = (By.XPATH, "//input[@id='blog_author'] | //input[@placeholder='Enter blog author...']")
    CATEGORY_SELECT = (By.XPATH, "//select[@id='blog_category'] | //select[@name='category']")
    CATEGORY_OPTIONS = (By.XPATH, "//select[@id='blog_category']//option[not(@disabled)] | //select[@name='category']//option[not(@disabled)]")
    CONTENT_EDITOR = (By.XPATH, "//div[@id='blog_content']//div[contains(@class,'ql-editor')] | //div[contains(@class,'ql-editor')]")
    SEO_SETTING_BTN = (By.XPATH, "//div[normalize-space()='SEO Settings' and @class='h6']")
    SEO_META_DESCRIPTION = (By.XPATH, "//textarea[contains(@placeholder,'meta') or @id='blog_meta_description']")
    SAVE_BLOG_BTN = (By.XPATH, "//span[normalize-space()= 'Create Blog' or normalize-space(.)='Update Blog']")
    
    # Confirmation
    CONFIRM_DELETE_BTN = (By.XPATH, "//button[contains(text(),'Delete Blog') or contains(text(),'Confirm') or contains(text(),'Delete Category')]")

    #toast
    ALERT_TOP = (By.XPATH, "//div[@class='alert-wrapper alert-wrapper--top']")
