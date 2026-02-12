import allure
from selenium.webdriver.common.by import By
import os
import time
import random
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from resources.resources import *
from locators_ecom.product_locators import ProductLocators

class Product:
    def __init__(self, driver, timeout=60):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout)

    @allure.step("Click Add Product button")
    def product(self):
        # Sidebar "Product" click is handled by sidebar.navigate_to_product()
        # This method now focuses on clicking "Add Product"
        
        add_product = self.wait.until(EC.presence_of_element_located(ProductLocators.ADD_PRODUCT_BTN))
        assert add_product.is_enabled(), f"Add Product isn't enabled."
        try:
            add_product.click()
            print("Add Product button clicked...")
            time.sleep(2)
        except ElementClickInterceptedException:
            print("Click intercepted, trying JS click or waiting...")
            time.sleep(3) # Wait for toast to disappear
            try:
                add_product.click()
                print("Add Product button clicked...")
            except ElementClickInterceptedException:
                # Fallback to JS click
                self.driver.execute_script("arguments[0].click();", add_product)
                print("Add Product button clicked...")
        time.sleep(2)

    @allure.step("Enter product name: {name_product}")
    def enter_product_name(self, name_product):
        product_input = self.wait.until(EC.presence_of_element_located(ProductLocators.PRODUCT_NAME_INPUT))
        assert product_input.is_enabled(), f"Product Name isn't enabled."
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", product_input)
        product_input.clear()
        product_input.send_keys(name_product)

    @allure.step("Select category: {category_heading}")
    def select_category(self, category_heading):
        # Ensure no lingering modals are blocking the action
        self.wait.until(EC.invisibility_of_element_located(ProductLocators.ACTIVE_MODAL))
        
        category_field = self.wait.until(EC.presence_of_element_located(ProductLocators.CATEGORY_DROPDOWN_HEADER))
        assert category_field.is_enabled(), f"Category field isn't enabled."
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", category_field)
        
        try:
            category_field.click()
            print("Category field clicked...")
        except ElementClickInterceptedException:
            print("Click intercepted on category field, trying JS click...")
            self.driver.execute_script("arguments[0].click();", category_field)
            print("Category field clicked...")
            
        time.sleep(1)

        add_category = self.wait.until(EC.presence_of_element_located(ProductLocators.ADD_NEW_CATEGORY_OPTION))
        assert add_category.is_enabled(), f"Add Category isn't enabled."
        add_category.click()
        print("Add Category button clicked...")
        time.sleep(1)
    
        add_category_title = self.wait.until(EC.presence_of_element_located(ProductLocators.NEW_CATEGORY_TITLE_TEXTAREA))
        add_category_title.send_keys(category_heading)

        base_title = category_heading.split('+')[0]
        image_path = None

        # Use base_title to find the image
        for ext in IMAGE_EXTENSIONS:
            temp_path = os.path.join(IMAGES_DIR, f"{base_title}{ext}")
            if os.path.exists(temp_path):
                image_path = temp_path
                break

        if image_path:
            # When adding a category, a modal opens, so the file input we want is likely the last one
            file_input = self.wait.until(EC.presence_of_element_located(ProductLocators.FILE_INPUT_GENERIC))
            file_input.send_keys(image_path)
        else:
            print(f"Image for category '{base_title}' not found in resources.")

        time.sleep(1)

        seo_setting = self.wait.until(EC.visibility_of_element_located(ProductLocators.SEO_TAB))
        time.sleep(1)
        assert seo_setting.is_enabled(), f"SEO setting isn't enabled."
        
        # Force JS click for reliability
        self.driver.execute_script("arguments[0].click();", seo_setting)
        print("SEO tab clicked...")
        
        # Get taxonomy value from map using base_title
        if base_title in google_taxonomy_map:
            taxonomy_value = google_taxonomy_map[base_title]
            input_taxonomy = self.wait.until(EC.visibility_of_element_located(ProductLocators.TAXONOMY_INPUT))
            input_taxonomy.send_keys(taxonomy_value)
        else:
            raise ValueError(f"No Google Taxonomy mapping found for category title: {base_title}")
        time.sleep(1)

        # Get meta description from map using base_title
        if base_title in meta_description_map:
            meta_desc_value = meta_description_map[base_title]
            meta_description = self.wait.until(EC.visibility_of_element_located(ProductLocators.META_DESC_INPUT))
            meta_description.send_keys(meta_desc_value)
        else:
            raise ValueError(f"No Meta Description mapping found for category title: {base_title}")

        add_category_btn = self.wait.until(EC.element_to_be_clickable(ProductLocators.SUBMIT_CATEGORY_BTN))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", add_category_btn)
        add_category_btn.click()
        print("Add Category button clicked...")        
        # Wait for the modal to disappear before proceeding
        self.wait.until(EC.invisibility_of_element_located(ProductLocators.ACTIVE_MODAL))
        time.sleep(2)

    @allure.step("Select random sale status")
    def select_sale_status(self):
        sale_field = self.wait.until(EC.presence_of_element_located(ProductLocators.SALE_SELECT))
        assert sale_field.is_enabled(), f"Sale field isn't enabled."
        sale_field.click()
        print("Sale field clicked...")
        time.sleep(1)

        sale_select_elem = self.wait.until(EC.presence_of_all_elements_located(ProductLocators.SALE_OPTIONS))
        select = random.choice(sale_select_elem)
        time.sleep(1)
        select.click()
        print("Sale option selected...")
        time.sleep(0.5)
    @allure.step("Select random arrival status")
    def select_arrival_status(self):
        arrival_field = self.wait.until(EC.presence_of_element_located(ProductLocators.ARRIVAL_SELECT))
        assert arrival_field.is_enabled(), f"Arrival field isn't enabled."
        arrival_field.click()
        print("Arrival field clicked...")
        time.sleep(1)

        arrival_select_elem = self.wait.until(EC.presence_of_all_elements_located(ProductLocators.ARRIVAL_OPTIONS))
        select = random.choice(arrival_select_elem)
        time.sleep(1)
        select.click()
        print("Arrival option selected...")
    
    @allure.step("Select product type (variable)")
    def selet_product_type(self):
        product_type = self.wait.until(EC.presence_of_element_located(ProductLocators.TYPE_SELECT))
        product_type.click()
        print("Product type field clicked...")
        time.sleep(1)

        product_type_select_elem = self.wait.until(EC.presence_of_element_located(ProductLocators.TYPE_VARIABLE_OPTION))
        product_type_select_elem.click()
        print("Product type option selected...")
        time.sleep(1)
    @allure.step("Enter product description: {product_description}")
    def enter_product_description(self,product_description):
        product_description_input = self.wait.until(EC.presence_of_element_located(ProductLocators.DESCRIPTION_EDITOR))
        assert product_description_input.is_enabled(), f"Product Description isn't enabled."   
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", product_description_input)
        product_description_input.send_keys(product_description)
        print("Product description entered...")

    @allure.step("Upload product category image: {product_name}")
    def upload_product_category_image(self, product_name):
        image_path = None
        
        # Try to find specific image first
        for ext in IMAGE_EXTENSIONS:
            temp_path = os.path.join(IMAGES_DIR, f"{product_name}{ext}")
            if os.path.exists(temp_path):
                image_path = temp_path
                break
                
        # Fallback: if specific image not found, try to find ANY valid image in images dir
        if not image_path and os.path.exists(IMAGES_DIR):
            print(f"Specific image for '{product_name}' not found. Searching for fallback...")
            for filename in os.listdir(IMAGES_DIR):
                if any(filename.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
                    image_path = os.path.join(IMAGES_DIR, filename)
                    if os.path.isfile(image_path):
                        print(f"Using fallback image: {filename}")
                        break
        
        if not image_path:
            print(f"No valid image files found in resources directory.")
            return

        print(f"Uploading image for product '{product_name}': {image_path}")

        try:
            # We skip clicking the image_field as it often opens a native file dialog 
            # which blocks Selenium. Instead, we send the path directly to the file input.
            # In most Saauzi forms, the first file input on the page is the main one.
            # Using [1] instead of [2] as the main product image is typically the first file input 
            # unless a modal is already open.
            file_input = self.wait.until(EC.presence_of_element_located(ProductLocators.FILE_INPUT_MAIN))
            file_input.send_keys(image_path)
            time.sleep(2) # Give it some time to start the upload/preview
            
            # Check if a modal appeared (e.g., for cropping)
            try:
                # Use a small wait to see if modal appears
                modal_wait = WebDriverWait(self.driver, 5)
                if self.driver.find_elements(*ProductLocators.ACTIVE_MODAL):
                    print("Modal appeared after image selection. Clicking Save/Apply...")
                    save_btn = self.driver.find_elements(*ProductLocators.MODAL_SAVE_BTN)
                    if save_btn:
                        save_btn[0].click()
                        time.sleep(1)
            except Exception:
                # If no modal appears, that's fine too
                pass
                
        except Exception as e:
            print(f"Failed to upload image: {e}")

    @allure.step("Upload variant image: {product_name}")
    def upload_variant_image(self, product_name):
        image_path = None
        
        # Try to find specific image first
        for ext in IMAGE_EXTENSIONS:
            temp_path = os.path.join(IMAGES_DIR, f"{product_name}{ext}")
            if os.path.exists(temp_path):
                image_path = temp_path
                break
                
        # Fallback: if specific image not found, try to find ANY valid image in images dir
        if not image_path and os.path.exists(IMAGES_DIR):
            print(f"Specific image for variant '{product_name}' not found. Searching for fallback...")
            for filename in os.listdir(IMAGES_DIR):
                if any(filename.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
                    image_path = os.path.join(IMAGES_DIR, filename)
                    if os.path.isfile(image_path):
                        print(f"Using variant fallback image: {filename}")
                        break
        
        if not image_path:
            error_msg = f"No valid image files found for variant in resources directory."
            print(error_msg)
            raise FileNotFoundError(error_msg)

        print(f"Uploading variant image for product '{product_name}': {image_path}")

        try:
            # Wait for the variant section to load after selecting product type
            print("Waiting for variant section to load...")
            time.sleep(2)
            
            # Check if the variant image placeholder exists
            variant_placeholders = self.driver.find_elements(*ProductLocators.VARIANT_IMAGE_PLACEHOLDER)
            print(f"Found {len(variant_placeholders)} variant image placeholder(s)")
            
            if not variant_placeholders:
                print("WARNING: No variant image placeholders found. Skipping variant image upload.")
                return
            
            # Scroll to and click the variant image placeholder
            scroll_to_variant_image_btn = self.wait.until(EC.presence_of_element_located(ProductLocators.VARIANT_IMAGE_PLACEHOLDER))
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", scroll_to_variant_image_btn)
            time.sleep(1)
            
            variant_image_btn = self.wait.until(EC.element_to_be_clickable(ProductLocators.VARIANT_IMAGE_PLACEHOLDER_LAST))
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", variant_image_btn)
            time.sleep(1)
            
            # Try clicking normally first
            try:
                variant_image_btn.click()
                print("Variant image button clicked (normal click)...")
            except ElementClickInterceptedException:
                print("Normal click intercepted, using JavaScript click...")
                self.driver.execute_script("arguments[0].click();", variant_image_btn)
                print("Variant image button clicked (JS click)...")
            
            time.sleep(1)
            
            # Check for file input inside the active modal FIRST (most reliable)
            file_inputs = self.driver.find_elements(*ProductLocators.MODAL_FILE_INPUT)
            
            if not file_inputs:
                print("Could not find file input inside active modal. Falling back to global search...")
                # Fallback: check if file input appeared globally using generic ID or type
                file_inputs = self.driver.find_elements(*ProductLocators.IMAGE_FILE_INPUT_ID)
            
            print(f"Found {len(file_inputs)} file input(s)")
            
            if not file_inputs:
                # Try alternative: look for any file input that appeared after the click
                print("Looking for alternative file inputs...")
                all_file_inputs = self.driver.find_elements(By.XPATH, "//input[@type='file']")
                print(f"Found {len(all_file_inputs)} total file input(s)")
                
                if all_file_inputs:
                    # Use the last one (most recently added)
                    upload_image = all_file_inputs[-1]
                    print(f"Using last file input found globally")
                else:
                    raise Exception("No file input found after clicking variant image placeholder")
            else:
                upload_image = file_inputs[-1] # Use the last one found in modal or by ID
            
            # Upload the image
            print(f"Sending keys to file input: {image_path}")
            upload_image.send_keys(image_path)
            
            # Explicitly trigger change event for modern frameworks (Nuxt/Vue)
            # print("Triggering change event via JS... (DISABLED)")
            
            
            print("Variant image uploaded...")
            time.sleep(2)
            
            # Check for any modal (like cropping) that might appear
            if self.driver.find_elements(*ProductLocators.ACTIVE_MODAL):
                print("Modal appeared after variant image selection. Clicking Save...")
                save_btn = self.driver.find_elements(*ProductLocators.MODAL_SAVE_BTN)
                if save_btn:
                    save_btn[0].click()
                    print("Modal save button clicked, waiting for modal to close...")
                    self.wait.until(EC.invisibility_of_element_located(ProductLocators.ACTIVE_MODAL))
                    time.sleep(1)
                    print("Modal closed successfully")
            
            # Verify image upload by checking if img tag replaced the svg/placeholder
            time.sleep(3)
            try:
                # Re-locate the placeholder as DOM might have updated
                updated_placeholder = self.driver.find_elements(*ProductLocators.VARIANT_IMAGE_PLACEHOLDER_LAST)
                if updated_placeholder:
                    img_tag = updated_placeholder[0].find_elements(By.TAG_NAME, "img")
                    if img_tag:
                        print(f"VERIFICATION SUCCESS: Variant image uploaded. Found img with src: {img_tag[0].get_attribute('src')}")
                    else:
                        print("VERIFICATION WARNING: No <img> tag found in placeholder after upload. Upload might have failed.")
            except Exception as v_error:
                print(f"Verification check failed: {v_error}")

        except Exception as e:
            print(f"CRITICAL ERROR: Failed to upload variant image: {e}")
            print(f"Current URL: {self.driver.current_url}")
            # Re-raise the exception to fail the test explicitly
            raise
            
    @allure.step("Save variant (click Done)")
    def save_variant(self):
        try:
            print("Looking for variant Done button...")
            done_btn = self.wait.until(EC.element_to_be_clickable(ProductLocators.VARIANT_DONE_BTN))
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", done_btn)
            time.sleep(1)
            try:
                done_btn.click()
                print("Done button clicked...")
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", done_btn)
                print("Done button clicked (JS)...")
        except TimeoutException:
            print("ERROR: Could not find 'Done' button for variant!")
            print(f"Current URL: {self.driver.current_url}")
            raise
    
    @allure.step("Enter marked price: {mp}")
    def marked_price(self, mp):
        marked_price = self.wait.until(EC.presence_of_element_located(ProductLocators.MARKED_PRICE_INPUT))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", marked_price)
        marked_price.send_keys(mp)
        print("Marked price entered...")
        time.sleep(1)
    @allure.step("Enter selling price: {sp}")
    def selling_price(self, sp):
        selling_price = self.wait.until(EC.presence_of_element_located(ProductLocators.SELLING_PRICE_INPUT))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", selling_price)
        selling_price.send_keys(sp)
        print("Selling price entered...")
        time.sleep(1)
    @allure.step("Enter available quantity: {aq}")
    def available_quantity(self, aq):
        available_quantity = self.wait.until(EC.presence_of_element_located(ProductLocators.QUANTITY_INPUT))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", available_quantity)
        available_quantity.send_keys(aq)
        print("Available quantity entered...")
        time.sleep(1)
    @allure.step("Select random size")
    def size(self):
        select_size_btn = self.wait.until(EC.presence_of_element_located(ProductLocators.SIZE_SELECT_BTN))
        try:
            select_size_btn.click()
            print("Size select button clicked...")
        except:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", select_size_btn)
            self.driver.execute_script("arguments[0].click();", select_size_btn)
        print("Size select button clicked...")
        time.sleep(1)

        sizes = self.wait.until(EC.presence_of_all_elements_located(ProductLocators.SIZE_OPTIONS))
        random_size = random.choice(sizes)
        try:
            random_size.click()
            print("Size option selected...")
        except:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", random_size)
            self.driver.execute_script("arguments[0].click();", random_size)
            print("Size option selected...")
        time.sleep(1)
    @allure.step("Select random color")
    def color(self):
        select_color_btn = self.wait.until(EC.presence_of_element_located(ProductLocators.COLOR_SELECT_BTN))
        try:
            select_color_btn.click()
            print("Color select button clicked...")
        except:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", select_color_btn)
            self.driver.execute_script("arguments[0].click();", select_color_btn)
            print("Color select button clicked...")
        time.sleep(1)

        colors = self.wait.until(EC.presence_of_all_elements_located(ProductLocators.COLOR_OPTIONS))
        random_color=random.choice(colors)
        try:
            random_color.click()
            print("Color option selected...")
        except:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", random_color)
            self.driver.execute_script("arguments[0].click();", random_color)
        time.sleep(1)
    @allure.step("Enter discount percentage: {discount_pct}")
    def discount(self, discount_pct):
        discount = self.wait.until(EC.presence_of_element_located(ProductLocators.DISCOUNT_INPUT))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", discount)
        discount.send_keys(discount_pct)
        print("Discount percentage entered...")
        time.sleep(1)

    @allure.step("Add additional variant: {product_title}")
    def add_additional_variant(self, product_title, mrk_p, sll_p, avl_q, discount_pct):
        add_variant_btn = self.wait.until(EC.element_to_be_clickable(ProductLocators.ADD_VARIANT_LINK))
        try:
            add_variant_btn.click()
            print("Add variant button clicked...")
        except:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", add_variant_btn)
            self.driver.execute_script("arguments[0].click();", add_variant_btn)
            print("Add variant button clicked...")
        time.sleep(1)
        try:
            self.upload_variant_image(product_title)
            self.marked_price(mrk_p)
            self.selling_price(sll_p)
            self.available_quantity(avl_q)
            self.size()
            self.color()
            self.discount(discount_pct)
        except Exception as e:
            print(f"Failed to add variant: {e}")

    @allure.step("Save major product")
    def save_product(self):
        # Click the Save/Add Product button at the bottom of the form
        save_btn = self.wait.until(EC.element_to_be_clickable(ProductLocators.SAVE_PRODUCT_BTN))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", save_btn)
        time.sleep(1)
        try:
            save_btn.click()
            print("Save button clicked...")
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", save_btn)
            print("Save button clicked...")
        
        # Assertion for Success Alert
        try:
             alert = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(ProductLocators.ALERT_TOP))
             print(f"Product Save Alert: {alert.text}")
             assert "success" in alert.text.lower() or "added" in alert.text.lower() or "updated" in alert.text.lower(), f"Unexpected alert message: {alert.text}"
             WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located(ProductLocators.ALERT_TOP))
        except TimeoutException:
             print("No success alert appeared within timeout for Product Save.")
        except Exception as e:
             print(f"An error occurred while verifying Product alert: {e}")