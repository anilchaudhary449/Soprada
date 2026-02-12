from selenium.webdriver.common.by import By

class SettingsLocators:
    # Navigation Tabs
    THEME_SETTINGS_TAB = (By.XPATH, "//div[text()='Theme Settings']")
    SITE_INFORMATION_TAB = (By.XPATH, "//div[text()='Site Information']")
    COMPANY_DETAILS_TAB = (By.XPATH, "//div[text()='Company Details']")
    TAX_INFORMATION_TAB = (By.XPATH, "//div[text()='Tax Information']")
    CONTACT_INFORMATION_TAB = (By.XPATH, "//div[text()='Contact Information']")
    SOCIAL_MEDIA_LINKS_TAB = (By.XPATH, "//div[text()='Social Media Links']")
    RETURN_POLICY_TAB = (By.XPATH, "//div[text()='Return Policy']")
    PRIVACY_POLICY_TAB = (By.XPATH, "//div[text()='Privacy Policy']")
    TERMS_CONDITIONS_TAB = (By.XPATH, "//div[text()='Terms & Conditions']")
    
    # Common Actions
    SAVE_CHANGES_BTN = (By.XPATH, "//button[text()='Save Changes']")
    ALERT_TOP = (By.XPATH, "//div[@class='alert-wrapper alert-wrapper--top']")
    
    # Site Information
    ORG_NAME_INPUT = (By.XPATH, "//input[contains(@placeholder, 'organization')] | //div[contains(@class, 'organization')]//input")
    LOGO_UPLOAD = (By.XPATH, "//button[normalize-space()='Upload Logo']/child::input")
    FAVICON_UPLOAD = (By.XPATH, "//div[contains(@class,'upload-favicon')]//following::button[normalize-space()='Upload Favicon']/child::input | //div[contains(@class,'upload-favicon')]//input[@type='file']")
    PROFILE_UPLOAD = (By.XPATH, "//div[contains(@class,'image-button')]/button[normalize-space()='Upload Profile']/child::input | //div[contains(@class,'image-button')]//input[@type='file']")
    SLOGAN_INPUT = (By.XPATH, "//input[contains(@placeholder, 'slogan')] | //div[contains(@class, 'slogan')]//input")
    CURRENCY_SELECT = (By.XPATH, "//label[normalize-space()='Currency']/following-sibling::select[contains(@class,'szi-input__control')]")
    CURRENCY_OPTIONS = (By.XPATH, "//select[contains(@class,'szi-input__control')]/child::option[not(text()='No' or text()='Yes')]")
    MAINTENANCE_SELECT = (By.XPATH, "//label[normalize-space()='Under Maintenance']/following-sibling::select[contains(@class,'szi-input__control')]")
    MAINTENANCE_OPTIONS = (By.XPATH, "//select[contains(@class,'szi-input__control')]/child::option[(text()='No' or text()='Yes')]")
    MAP_TEXTAREA = (By.XPATH, "//div[contains(@class,'map')]/textarea")
    
    # Company Details
    ADDRESS_INPUT = (By.XPATH, "//div[contains(@class,'address')]/input")
    EDITOR_CONTENT = (By.XPATH, "//div[contains(@class,'ql-editor')]") # Generic for all policy/about us editors
    
    #Tax Information
    VAT_TOGGLE_BTN = (By.ID, "enable-disable-pan-vat-number")
    VAT_TOGGLE_BTN_CHECKBOX = (By.XPATH, "//label[normalize-space(.)='Enable VAT/PAN']")
    VAT_INPUT = (By.XPATH, "//input[@placeholder='Enter your VAT/PAN...']")
    VAT_PCT = (By.XPATH,"//input[@placeholder='Enter your VAT in Percent...']")

    # Contact Information
    CONTACT_NUM_INPUT = (By.XPATH, "//div[contains(@class,'contact-number')]/input")
    ALT_CONTACT_INPUT = (By.XPATH, "//div[contains(@class,'alternate-contact')]/input")
    
    EMAIL_INPUT = (By.XPATH, "//div[contains(@class,'email')]/input[@placeholder='Enter email']")
    ALT_EMAIL_INPUT = (By.XPATH, "//div[contains(@class,'alternate-email')]/input[@placeholder='Enter alt email']")
    WHATSAPP_INPUT = (By.XPATH, "//div[contains(@class,'whatsapp')]/input")
    VIBER_INPUT = (By.XPATH, "//div[contains(@class,'viber')]/input")
    
    # Social Media Links
    FB_INPUT = (By.XPATH, "//div[contains(@class,'facebook')]/input")
    INSTA_INPUT = (By.XPATH, "//div[contains(@class,'instagram')]/input")
    TWITTER_INPUT = (By.XPATH, "//div[contains(@class,'twitter')]/input")
    LINKEDIN_INPUT = (By.XPATH, "//div[contains(@class,'linkedin')]/input")
    YOUTUBE_INPUT = (By.XPATH, "//div[contains(@class,'youtube')]/input")
    TIKTOK_INPUT = (By.XPATH, "//div[contains(@class,'tiktok')]/input")
