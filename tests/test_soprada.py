from pages_ecom.inventory_management import InventoryManagement
import pytest
import allure
import os
import time
import random
from selenium.common.exceptions import NoSuchDriverException, WebDriverException
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pages_ecom.category import Category
from pages_ecom.custom_domain import Custom_Domain
from pages_ecom.login_otp import login_with_otp
from pages_ecom.create_new_store import Create_Store
from pages_ecom.product import Product
from pages_ecom.variant import Variant
from pages_ecom.order import Order
from pages_ecom.shipping_charge_settings import ShippingChargeSettings
from pages_ecom.customer import Customer
from pages_ecom.review import Review
from pages_ecom.enquiry import Enquiry
from pages_ecom.support_case import SupportCase
from pages_ecom.blog import Blog
from pages_ecom.marketing import Marketing
from pages_ecom.sliders import Sliders
from pages_ecom.themes import Themes
from pages_ecom.plugins import Plugins
from pages_ecom.staff import Staff
from pages_ecom.payments import Payments
from pages_ecom.settings import Settings
from resources.resources import *
from utils.gmail_api import GmailAPI, OTPHandler
from pages_ecom.sidebar import Sidebar


p_name = product_name()
@pytest.fixture(scope="module")
def setup():
    """Firefox-only setup fixture"""
    # Selenium 4+ and WebDriverManager will handle finding Firefox and Geckodriver automatically.
    # The manual shutil.which checks were incorrectly skipping tests on Windows.

    firefox_options = Options()
    firefox_options.set_preference("privacy.trackingprotection.enabled", True)
    
    # Enable headless mode in CI/CD environments
    if os.environ.get('GITHUB_ACTIONS') == 'true' or os.environ.get('CI') == 'true':
        firefox_options.add_argument("--headless")
    
    # driver = webdriver.Firefox(options=firefox_options)
    try:
        driver = webdriver.Firefox(options=firefox_options)
    except (NoSuchDriverException, WebDriverException) as exc:
        pytest.skip(f"Firefox driver unavailable: {exc}")
    driver.maximize_window()
    
    yield driver
    # driver.quit()

@pytest.fixture(scope="module")
def logged_in_setup(setup):
    driver = setup
    login_page = login_with_otp(driver)
    
    # Initialize Gmail API (OAuth 2.0)
    gmail_api = GmailAPI(GMAIL_API_CREDENTIALS, GMAIL_API_TOKEN)
    
    # Cleanup previous OTP emails
    gmail_api.cleanup_inbox(GMAIL_OTP_QUERY)
    
    # Perform Login
    login_page.open_saauzi_site(URL)
    login_page.enter_specific_email(GMAIL_USER)
    
    # Fetch OTP with retry
    status, otp = OTPHandler.fetch_with_retry(
        gmail_api, 
        GMAIL_OTP_QUERY, 
        GMAIL_OTP_REGEX, 
        max_attempts=2, 
        resend_callback=login_page.trigger_resend_otp
    )
    
    if status != "OTP_RECEIVED" or not otp:
        pytest.fail(f"OTP fetch failed: {status}")
    

    login_page.enter_otp_direct(otp)
    
    # Wait for login to complete
    try:
        WebDriverWait(driver, 60).until(lambda d: "dashboard" in d.current_url.lower() or "create-store" in d.current_url.lower())
    except Exception as e:
        # Check if there is an error message visible on the login page
        error_msgs = driver.find_elements(By.XPATH, "//div[contains(@class,'text-danger')] | //span[contains(@class,'error')]")
        if error_msgs:
            error_text = " | ".join([m.text for m in error_msgs if m.is_displayed() and m.text])
            if error_text:
                allure.attach(driver.get_screenshot_as_png(), name="Login Error Visible", attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Login failed after entering OTP. Error visible on page: {error_text}")
        
        # Take a screenshot for debugging in CI
        driver.save_screenshot("login_failed.png")
        allure.attach(driver.get_screenshot_as_png(), name="Login Timeout/Failure", attachment_type=allure.attachment_type.PNG)
        print(f"Login timed out. Screenshot saved as login_failed.png. Current URL: {driver.current_url}")
        raise e
    
    if "create-store" in driver.current_url:
        create_store_page = Create_Store(driver)
        create_store_page.create_store(f"{store_name()}", f"{store_contact()}")
        WebDriverWait(driver, 35).until(lambda d: "dashboard" in d.current_url.lower())

    return driver

@allure.feature("Authentication")
@allure.story("Login Verification")
@allure.title("Verify login is successful with OTP")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.sanity
@pytest.mark.cross_browser
def test_verify_login(logged_in_setup):
    """Verifies that the setup fixture successfully logged us in."""
    driver = logged_in_setup
    assert "dashboard" in driver.current_url.lower()

@allure.feature("Store Management")
@allure.story("Create Store")
@allure.title("Verify store creation")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.sanity
@pytest.mark.cross_browser
def test_create_store(logged_in_setup):
    driver = logged_in_setup
    # Store creation is now handled in logged_in_setup if needed
    assert "dashboard" in driver.current_url.lower(), "Store creation failed or Dashboard not visible"

@allure.feature("Store Custom Domain")
@allure.story("Custom Domain")
@allure.title("Verify custom domain configuration")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.sanity
@pytest.mark.cross_browser
def test_custom_domain(logged_in_setup):
    driver = logged_in_setup
    sidebar = Sidebar(driver)
    sidebar.navigate_to_custom_domain()
    
    custom_domain_page = Custom_Domain(driver)
    custom_domain_page.custom_domain(custom_domain, updated_domain)

@allure.feature("Store Management")
@allure.story("Categories")
@allure.title("Verify category and sub-category operations")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.sanity
@pytest.mark.cross_browser
def test_category(logged_in_setup):
    driver = logged_in_setup
    sidebar = Sidebar(driver)
    sidebar.navigate_to_category()
    
    category_page = Category(driver)
    
    # Create first category
    first_category_title = f"{category_title()}+{get_nepal_time_str()}"
    first_category_result = category_page.category(first_category_title)
    
    # Create second category with different title
    # time.sleep(2)  # Small delay to ensure different timestamp
    # second_category_title = f"{category_title()}+{get_nepal_time_str()}"
    # second_category_result = category_page.category(second_category_title)
    
    # Only add sub-category if the main category was successfully created
    if first_category_result == 1:
        sub_category_title = f"{category_title()}+{get_nepal_time_str()}"
        if category_page.add_sub_category(sub_category_title) == 1:
            category_page.delete_sub_category()
    
    # Delete both categories (delete in reverse order - last created first)
    # category_page.delete_category()  # Deletes second category
    time.sleep(1)
    category_page.delete_category()  # Deletes first category

@allure.feature("Store Management")
@allure.story("Products")
@allure.title("Verify product creation with variants")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.sanity
@pytest.mark.cross_browser
def test_product(logged_in_setup):
    driver = logged_in_setup
    sidebar = Sidebar(driver)
    sidebar.navigate_to_product()
    
    product_page = Product(driver)
    mp = marked_price()
    sp = selling_price()
    aq = available_quantity()
    dis_pct = discount()

    
    mp1 = marked_price()
    sp1 = selling_price()
    aq1 = available_quantity()
    dis_pct1 = discount()
    
    product_page.product()
    product_page.enter_product_name(p_name)
    product_page.enter_product_description(get_product_description(p_name))
    product_page.upload_product_category_image(p_name)
    product_page.select_category(f"{category_title()}+{get_nepal_time_str()}")
    product_page.select_sale_status()
    product_page.select_arrival_status()
    product_page.selet_product_type()
    
    # Fill in variant details FIRST before uploading image
    product_page.marked_price(mp)
    product_page.selling_price(sp)
    product_page.available_quantity(aq)
    product_page.size()
    product_page.color()
    product_page.discount(dis_pct)
    
    # NOW upload variant image and save
    product_page.upload_variant_image(p_name)
    
    # Add additional variant
    product_page.add_additional_variant(p_name, mp1, sp1, aq1, dis_pct1)
    
    product_page.save_product()

@allure.feature("Management of Inventories")
@allure.story("Inventory Management")
@allure.title("Adjust Inventories")
def test_inventory_management(logged_in_setup):
    driver = logged_in_setup
    sidebar = Sidebar(driver)
    sidebar.navigate_to_inventory_management()

    inventory_management_page = InventoryManagement(driver)
    inventory_management_page.inventory_management()

@allure.feature("Store Management")
@allure.story("Variant")
@allure.title("Verify variant (Color/Size) configuration")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.sanity
@pytest.mark.cross_browser
def test_variant(logged_in_setup):
    driver = logged_in_setup
    sidebar = Sidebar(driver)
    sidebar.navigate_to_variant()
    
    variant_page = Variant(driver)
    color_name, color_hex = get_random_color()

    variant_page.add_variant(f"{color_name}+{get_nepal_time_str()}", color_hex)
    time.sleep(2)
    # Add Size

    variant_page.add_sizes()
    # time.sleep(2)

@allure.feature("Store Management")
@allure.story("Order")
@allure.title("Verify full order placement, update and print cycle")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.sanity
@pytest.mark.cross_browser
def test_order(logged_in_setup):
    driver = logged_in_setup
    try:
        driver.refresh()
    except Exception as e:
        print(f"Warning: driver.refresh() failed: {e}. Continuing...")
    time.sleep(5)
    sidebar = Sidebar(driver)
    sidebar.navigate_to_order()
    order_page = Order(driver)

    p_name2 = get_random_alphabet()
    confirm_quant = confirm_quantity()
    
    order_page.order_nav()
    order_page.order_details(p_name2, confirm_quant)
    order_page.action_Edit_to_place_order()
    order_page.update_order_status()
    order_page.print_order()

@allure.feature("Store Logistics")
@allure.story("Shipping Charges Settings")
@allure.title("Verify shipping charge configuration")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.sanity
@pytest.mark.cross_browser
def test_shipping_charge_settings(logged_in_setup):
    driver = logged_in_setup
    sidebar = Sidebar(driver)
    sidebar.navigate_to_shipping_charge_settings()
    
    shipping_charge_settings_page = ShippingChargeSettings(driver)
    l_charge = logistic_charge()
    shipping_charge_settings_page.add_shipping_settings(l_charge)
    shipping_charge_settings_page.shipping_charge_settings(l_charge)
    shipping_charge_settings_page.delete_shipping_settings()

@allure.feature("Customer Service")
@allure.story("Customer")
@allure.title("Verify customer registration")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.sanity
@pytest.mark.cross_browser
def test_customer(logged_in_setup):
    driver = logged_in_setup
    sidebar = Sidebar(driver)
    sidebar.navigate_to_customer()

    customer_page = Customer(driver)

    c_name = customer_name()
    c_email = customer_email()
    c_phone = customer_phone()
    c_street = customer_street()
    # c_city = customer_city()
    c_image = customer_image()
    
    customer_page.customer_nav()
    customer_page.enter_customer_name(c_name)
    customer_page.enter_customer_email(c_email)
    customer_page.enter_customer_phone(c_phone)
    customer_page.enter_customer_street(c_street)
    customer_page.select_customer_city()
    customer_page.upload_customer_image(c_image)
    customer_page.add_customer_btn()

@allure.feature("Customer Service")
@allure.story("Reviews")
@allure.title("Verify reviews section")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.sanity
@pytest.mark.cross_browser
def test_review(logged_in_setup):
    driver = logged_in_setup
    sidebar = Sidebar(driver)
    sidebar.navigate_to_review()
    review_page = Review(driver)
    review_page.toggle_review_visibility()

# @allure.feature("Customer Service")
# @allure.story("Enquiries")
# @allure.title("Verify enquiry handling")
# @pytest.mark.smoke
# @pytest.mark.regression
# @pytest.mark.sanity
# @pytest.mark.cross_browser
# def test_enquiry(logged_in_setup):
#     driver = logged_in_setup
#     sidebar = Sidebar(driver)
#     sidebar.navigate_to_enquiry()
#     enquiry_page = Enquiry(driver)
#     enquiry_page.mark_all_as_seen()
#     enquiry_page.toggle_status()
#     enquiry_page.view_enquiry()

# @allure.feature("Customer Service")
# @allure.story("Support Cases")
# @allure.title("Verify support case management")
# @pytest.mark.smoke  
# @pytest.mark.regression
# @pytest.mark.sanity
# @pytest.mark.cross_browser
# def test_support_case(logged_in_setup):
#     driver = logged_in_setup
#     sidebar = Sidebar(driver)
#     sidebar.navigate_to_support_case()
#     support_case_page = SupportCase(driver)

#     support_case_status = random_status()
#     support_case_page.filter_by_status(support_case_status)

# @allure.feature("Content & Marketing")
# @allure.story("Blog")
# @allure.title("Verify blog post lifecycle")
# @pytest.mark.smoke
# @pytest.mark.regression
# @pytest.mark.sanity
# @pytest.mark.cross_browser
# def test_blog(logged_in_setup):
#     driver = logged_in_setup
#     sidebar = Sidebar(driver)
#     sidebar.navigate_to_blog()                      
#     blog_page = Blog(driver)

#     blog_category_name, blog_category_short_description = get_random_blog_category_data()
#     blog_page.new_category(blog_category_name, blog_category_short_description)
#     # time.sleep(2)
#     # blog_category_name1, blog_category_short_description1 = get_random_blog_category_data()
#     # blog_page.new_category(blog_category_name1, blog_category_short_description1)
#     time.sleep(0.5)

#     blog_page.edit_category(blog_category_name+"_updated", blog_category_short_description+"_updated")
#     blog_page.delete_category()
#     time.sleep(0.5)
    
#     title, image_path, content, author, meta_description = get_random_blog_data()
#     blog_page.add_blog(title, image_path, content, author, meta_description)
#     blog_page.view_blog()
#     blog_page.edit_blog(title+"_updated", image_path, content+"_updated", author+"_updated", meta_description+"_updated")
#     blog_page.delete_blog()

# @allure.feature("Content & Marketing")
# @allure.story("Coupons")
# @allure.title("Verify coupon code creation and viewing")
# @pytest.mark.smoke
# @pytest.mark.regression
# @pytest.mark.sanity
# @pytest.mark.cross_browser
# def test_marketing(logged_in_setup):
#     driver = logged_in_setup
#     sidebar = Sidebar(driver)
#     sidebar.navigate_to_marketing()
#     marketing_page = Marketing(driver)
    
#     # Generate random test data
#     heading = f"{promo_heading()}"
#     code = f"SAVE{random.randint(1, 9999)}"
#     dis_pct = str(random.randint(5, 50))
#     pct_amt = str(random.randint(50, 200))
#     min_pur_amt = str(random.randint(500, 2000))
#     start_date = get_random_start_date()
#     end_date = get_random_end_date(start_date)
    
#     marketing_page.marketing()
#     marketing_page.add_coupon_code(heading, code, dis_pct, pct_amt, min_pur_amt, start_date, end_date)
#     marketing_page.view_coupon()

# @allure.feature("Content & Marketing")
# @allure.story("Sliders")
# @allure.title("Verify slider management")
# @pytest.mark.smoke
# @pytest.mark.regression
# @pytest.mark.sanity
# @pytest.mark.cross_browser
# def test_sliders(logged_in_setup):
#     driver = logged_in_setup
#     sidebar = Sidebar(driver)
#     sidebar.navigate_to_sliders()
#     sliders_page = Sliders(driver)
    
#     # Generate random slider data
#     title, subtitle, description, image_path, link_name, link_url = get_random_slider_data()
    
#     # Test Adding a Slider
#     print(f"Adding slider: {title}")
#     sliders_page.add_sliders(image_path, title, subtitle, description, link_name, link_url)
    
#     time.sleep(2)
#     # Test Editing a Slider (randomly)
#     title2, subtitle2, description2, _, link_name2, link_url2 = get_random_slider_data()
#     print(f"Editing slider to: {title2}")
#     sliders_page.edit_sliders(title2, subtitle2, description2, link_name2, link_url2)
#     time.sleep(2)
#     sliders_page.delete_sliders()

# @allure.feature("Store Settings")
# @allure.story("Themes")
# @allure.title("Verify theme selection")
# @pytest.mark.smoke
# @pytest.mark.regression
# @pytest.mark.sanity
# @pytest.mark.cross_browser
# def test_themes(logged_in_setup):
#     driver = logged_in_setup
#     sidebar = Sidebar(driver)
#     sidebar.navigate_to_themes()
#     themes_page = Themes(driver)
#     themes_page.apply_random_theme()

# @allure.feature("Store Settings")
# @allure.story("Plugins")
# @allure.title("Verify plugin installation and activation")
# @pytest.mark.smoke
# @pytest.mark.regression
# @pytest.mark.sanity
# @pytest.mark.cross_browser
# def test_plugins(logged_in_setup):
#     driver = logged_in_setup
#     sidebar = Sidebar(driver)
#     sidebar.navigate_to_plugins()
#     plugins_page = Plugins(driver)
#     plugins_page.plugins()
#     plugins_page.install_plugins()
#     plugins_page.activate_plugin()

# @allure.feature("Store Settings")
# @allure.story("Staff")
# @allure.title("Verify staff assignment and role management")
# @pytest.mark.smoke
# @pytest.mark.regression
# @pytest.mark.sanity
# @pytest.mark.cross_browser
# def test_staff(logged_in_setup):
#     driver = logged_in_setup
#     sidebar = Sidebar(driver)
#     sidebar.navigate_to_staff()
#     staff_page = Staff(driver)

#     f_name= full_name_staff()
#     email = email_staff()
#     phone = phone_staff()
#     address = address_staff()

#     staff_page.add_staff(f_name, email, phone,address)

#     f_name1 = full_name_staff()
#     address1 = address_staff()
#     staff_page.edit_staff(f_name1, address1)

#     staff_page.delete_staff()

#     staff_page.add_role_permission()

# @allure.feature("Store Settings")
# @allure.story("Payments")
# @allure.title("Verify payment method configuration")
# @pytest.mark.smoke
# @pytest.mark.regression
# @pytest.mark.sanity
# @pytest.mark.cross_browser
# def test_payments(logged_in_setup):
#     driver = logged_in_setup
#     sidebar = Sidebar(driver)
#     sidebar.navigate_to_payments()
#     payments_page = Payments(driver)
#     payments_page.payments_cash_on_delivery()
#     payments_page.payments_manual_payment(get_qr_image())

# @allure.feature("Store Settings")
# @allure.story("Settings(Themes,Site Information,Company Details,Contact Information,Social Media Links,Return Policy,Refund Policy,Privacy Policy,Terms & Conditions)")
# @allure.title("Verify overall site information, settings and policies")
# @pytest.mark.smoke
# @pytest.mark.regression
# @pytest.mark.sanity
# @pytest.mark.cross_browser
# def test_settings(logged_in_setup):
#     driver = logged_in_setup
#     sidebar = Sidebar(driver)
#     sidebar.navigate_to_settings()
#     settings_page = Settings(driver)
#     settings_page.theme_settings()

#     organization_name = organization()
#     logo = get_logo()
#     favicon = get_favicon()
#     profile = get_profile()
#     slogan_lines = slogan()
#     settings_page.site_information(organization_name,logo,favicon,profile,slogan_lines,map_link)

#     vat_num = vat_number()
#     vat_pct = vat_percentage()
#     addr = address()
#     about = about_us()
    
#     settings_page.company_details(addr, about)
#     settings_page.tax_information(vat_num, vat_pct)

#     contact = contact_number()
#     alternate_contact = alternate_contact_number()
#     email_address = email()
#     alt_email_address = alternate_email()
#     whatsapp_number = whatsapp()
#     viber_number = viber()
#     settings_page.contact_information(contact, alternate_contact, email_address, alt_email_address, whatsapp_number, viber_number)
#     time.sleep(1)

#     facebook = facebook_link()
#     instagram = instagram_link()
#     twitter = twitter_link()
#     linkedin = linkedin_link()
#     youtube = youtube_link()
#     tiktok = tiktok_link()
#     settings_page.social_media_links(facebook, instagram, twitter, linkedin, youtube, tiktok)
#     time.sleep(1)

#     return_policy_val = return_policy()
#     settings_page.return_policy(return_policy_val)
#     time.sleep(1)

#     privacy_policy_val = privacy_policy()
#     settings_page.privacy_policy(privacy_policy_val)

#     time.sleep(1)
#     terms_and_conditions_val = terms_and_conditions()
#     settings_page.terms_and_conditions(terms_and_conditions_val)


    
if __name__ == "__main__":
    pytest.main(["tests/test_soprada.py"])