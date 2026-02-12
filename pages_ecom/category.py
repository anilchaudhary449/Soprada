import allure
import os
import time
import random
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from resources.resources import *
from locators_ecom.category_locators import CategoryLocators


class Category:
    def __init__(self, driver, timeout=60):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout)
        
    @allure.step("Add new category: {title}")
    def category(self, title):
        # Extract the base title from the concatenated title
        base_title = title.split('+')[0]

        category_icon = self.wait.until(EC.presence_of_element_located(CategoryLocators.SIDEBAR_CATEGORY))
        assert category_icon.is_enabled(), f"category isn't enabled."
        category_icon.click()
        time.sleep(2)

        add_new_category = self.wait.until(EC.presence_of_element_located(CategoryLocators.ADD_NEW_CATEGORY_BTN))
        assert add_new_category.is_enabled(), f"Add New Category isn't enabled."
        
        # Try to click, handling interception
        try:
            add_new_category.click()
        except ElementClickInterceptedException:
            print("Click intercepted, trying JS click or waiting...")
            time.sleep(3) # Wait for toast to disappear
            try:
                add_new_category.click()
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", add_new_category)
        time.sleep(1)

        add_category_title = self.wait.until(EC.visibility_of_element_located(CategoryLocators.TITLE_INPUT))
        add_category_title.send_keys(title)
        print("Category title entered...")
        image_path = None
        for ext in IMAGE_EXTENSIONS:
            temp_path = os.path.join(IMAGES_DIR, f"{base_title}{ext}")
            if os.path.exists(temp_path):
                image_path = temp_path
                break

        if image_path:
            file_input = self.wait.until(EC.presence_of_element_located(CategoryLocators.IMAGE_FILE_INPUT))
            file_input.send_keys(image_path)
            print("Category image uploaded...")
        else:
            print(f"Image for category '{base_title}' not found in resources.")

        time.sleep(1)

        seo_setting = self.wait.until(EC.visibility_of_element_located(CategoryLocators.SEO_SETTING_TAB))
        time.sleep(1)
        assert seo_setting.is_enabled(), f"SEO setting isn't enabled."
        
        # Force JS click for reliability
        self.driver.execute_script("arguments[0].click();", seo_setting)
        
        # Get taxonomy value from map using base_title
        if base_title in google_taxonomy_map:
            taxonomy_value = google_taxonomy_map[base_title]
            input_taxonomy = self.wait.until(EC.visibility_of_element_located(CategoryLocators.TAXONOMY_INPUT))
            input_taxonomy.send_keys(taxonomy_value)
            print("Category taxonomy entered...")
        else:
            raise ValueError(f"No Google Taxonomy mapping found for category title: {base_title}")
        time.sleep(1)

        # Get meta description from map using base_title
        if base_title in meta_description_map:
            meta_desc_value = meta_description_map[base_title]
            meta_description = self.wait.until(EC.visibility_of_element_located(CategoryLocators.META_DESC_INPUT))
            meta_description.send_keys(meta_desc_value)
            print("Category meta description entered...")
        else:
            raise ValueError(f"No Meta Description mapping found for category title: {base_title}")

        add_category_btn = self.wait.until(EC.element_to_be_clickable(CategoryLocators.ADD_CATEGORY_SUBMIT_BTN))
        add_category_btn.click()
        print("Category added...")
        
        # Assertion for Success Alert
        try:
             alert = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(CategoryLocators.ALERT_TOP))
             print(f"Category Save Alert: {alert.text}")
             assert "success" in alert.text.lower() or "added" in alert.text.lower(), f"Unexpected alert message: {alert.text}"
             WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located(CategoryLocators.ALERT_TOP))
        except TimeoutException:
             print("No success alert appeared within timeout for Category Add.")
        except Exception as e:
             print(f"An error occurred while verifying Category alert: {e}")
        self.wait.until(EC.invisibility_of_element_located(CategoryLocators.ACTIVE_MODAL))
        self.wait.until(EC.invisibility_of_element_located(CategoryLocators.ALERT_TOP))
        return 1


    @allure.step("Add sub-category: {title}")
    def add_sub_category(self, title):
        base_title = title.split('+')[0]
        time.sleep(2)
        
        add_sub_category_btns = self.wait.until(EC.presence_of_all_elements_located(CategoryLocators.ADD_SUB_CATEGORY_BTNS))
        select_add_sub_category_btn = random.choice(add_sub_category_btns)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", select_add_sub_category_btn)
        time.sleep(1)
        
        # Try normal click first, then JS
        print("Clicking sub-category Add button...")
        try:
             select_add_sub_category_btn.click()
             print("Sub-category Add button clicked...")
        except:
             self.driver.execute_script("arguments[0].click();", select_add_sub_category_btn)
             print("Sub-category Add button clicked...")
        
        time.sleep(2)

        try:
            add_sub_category_title = self.wait.until(EC.visibility_of_element_located(CategoryLocators.TITLE_INPUT))
            add_sub_category_title.send_keys(title)
            print("Sub-category title entered...")
        except TimeoutException:
            print("Failed to find sub-category title input. Retrying click...")
            self.driver.execute_script("arguments[0].click();", select_add_sub_category_btn)
            time.sleep(2)
            add_sub_category_title = self.wait.until(EC.visibility_of_element_located(CategoryLocators.TITLE_INPUT))
            add_sub_category_title.send_keys(title)
            print("Sub-category title entered...")

        image_path = None
        for ext in IMAGE_EXTENSIONS:
            temp_path = os.path.join(IMAGES_DIR, f"{base_title}{ext}")
            if os.path.exists(temp_path):
                image_path = temp_path
                break

        if image_path:
            file_input = self.wait.until(EC.presence_of_element_located(CategoryLocators.SUB_CATEGORY_FILE_INPUT))
            file_input.send_keys(image_path)
            print("Sub-category image uploaded...")
        else:
            print(f"Image for sub_category '{base_title}' not found in resources.")

        time.sleep(1)

        seo_setting = self.wait.until(EC.presence_of_element_located(CategoryLocators.SEO_SETTING_TAB))
        time.sleep(1)
        assert seo_setting.is_enabled(), f"SEO setting isn't enabled."
        
        try:
            seo_setting.click()
            print("SEO setting clicked...")
        except ElementClickInterceptedException:
            print("Click intercepted, trying JS click...")
            time.sleep(3)
            try:
                seo_setting.click()
                print("SEO setting clicked...")
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", seo_setting)
        time.sleep(1)

        if base_title in google_taxonomy_map:
            taxonomy_value = google_taxonomy_map[base_title]
            input_taxonomy = self.wait.until(EC.presence_of_element_located(CategoryLocators.TAXONOMY_INPUT))
            input_taxonomy.send_keys(taxonomy_value)
            print("Sub-category taxonomy entered...")
        else:
            raise ValueError(f"No Google Taxonomy mapping found for sub_category title: {base_title}")
        time.sleep(1)

        if base_title in meta_description_map:
            meta_desc_value = meta_description_map[base_title]
            meta_description = self.wait.until(EC.presence_of_element_located(CategoryLocators.META_DESC_INPUT))
            meta_description.send_keys(meta_desc_value)
            print("Sub-category meta description entered...")
        else:
            raise ValueError(f"No Meta Description mapping found for sub_category title: {base_title}")

        add_sub_category_btn = self.wait.until(EC.element_to_be_clickable(CategoryLocators.ADD_SUB_CATEGORY_SUBMIT_BTN))
        add_sub_category_btn.click()
        print("Sub-category added...")
        
        # Assertion for Success Alert
        alert = self.wait.until(EC.visibility_of_element_located(CategoryLocators.ALERT_TOP))
        print(f"Sub-category Add Alert: {alert.text}")
        assert "success" in alert.text.lower() or "added" in alert.text.lower(), f"Unexpected alert message: {alert.text}"
        
        self.wait.until(EC.invisibility_of_element_located(CategoryLocators.ACTIVE_MODAL))
        self.wait.until(EC.invisibility_of_element_located(CategoryLocators.ALERT_TOP))
        return 1

    @allure.step("Edit sub-category: {title}")
    def edit_sub_category(self, title):
        self.wait.until(EC.invisibility_of_element_located(CategoryLocators.ALERT_TOP))
        edit_sub_category_btns = self.wait.until(EC.presence_of_all_elements_located(CategoryLocators.EDIT_SUB_CATEGORY_BTNS))
        select_edit_sub_category_btn = random.choice(edit_sub_category_btns)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", select_edit_sub_category_btn)
        time.sleep(1)
        try:
            select_edit_sub_category_btn.click()
            print("Sub-category edit button clicked...")
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", select_edit_sub_category_btn)
            print("Sub-category edit button clicked...")
        time.sleep(1)
        
        # Update title
        edit_title = self.wait.until(EC.presence_of_element_located(CategoryLocators.TITLE_INPUT))
        edit_title.clear()
        edit_title.send_keys(title + "_updated")
        
        # Update button
        update_btn = self.wait.until(EC.element_to_be_clickable(CategoryLocators.UPDATE_CATEGORY_SUBMIT_BTN))
        update_btn.click()
        
        # Assertion for Success Alert
        try:
             alert = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(CategoryLocators.ALERT_TOP))
             print(f"Category Update Alert: {alert.text}")
             assert "success" in alert.text.lower() or "updated" in alert.text.lower(), f"Unexpected alert message: {alert.text}"
             WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located(CategoryLocators.ALERT_TOP))
        except TimeoutException:
             print("No success alert appeared within timeout for Category Update.")
        except Exception as e:
             print(f"An error occurred while verifying Category update alert: {e}")
        self.wait.until(EC.invisibility_of_element_located(CategoryLocators.ACTIVE_MODAL))
        self.wait.until(EC.invisibility_of_element_located(CategoryLocators.ALERT_TOP))

    @allure.step("Delete sub-category")
    def delete_sub_category(self):
        delete_sub_category_btns = self.wait.until(EC.presence_of_all_elements_located(CategoryLocators.DELETE_SUB_CATEGORY_BTNS))
        select_delete_sub_btn = random.choice(delete_sub_category_btns)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", select_delete_sub_btn)
        time.sleep(1)
        try:
            select_delete_sub_btn.click()
            print("Sub-category delete button clicked...")
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", select_delete_sub_btn)
            print("Sub-category delete button clicked...")
        time.sleep(1)
        delete_sub_category_confirm_btn = self.wait.until(EC.element_to_be_clickable(CategoryLocators.CONFIRM_DELETE_SUB_BTN))
        delete_sub_category_confirm_btn.click()
        print("Sub-category delete button clicked...")
        alert_message = self.wait.until(EC.visibility_of_element_located(CategoryLocators.ALERT_TOP))
        print("\n", alert_message.text)
        time.sleep(1)

    @allure.step("Delete category")
    def delete_category(self):
        self.wait.until(EC.invisibility_of_element_located(CategoryLocators.ALERT_TOP)) 
        delete_category_btns = self.wait.until(EC.presence_of_all_elements_located(CategoryLocators.DELETE_CATEGORY_BTNS))
        select_delete_category_btn = random.choice(delete_category_btns)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", select_delete_category_btn)
        time.sleep(1)
        try:
            select_delete_category_btn.click()
            print("Category delete button clicked...")
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", select_delete_category_btn)
            print("Category delete button clicked...")
        time.sleep(0.5)
        delete_category_confirm_btn = self.wait.until(EC.element_to_be_clickable(CategoryLocators.CONFIRM_DELETE_CAT_BTN))
        delete_category_confirm_btn.click()
        print("Category delete button clicked...")
        alert_message = self.wait.until(EC.visibility_of_element_located(CategoryLocators.ALERT_TOP))
        print("\n", alert_message.text)
        assert "deleted" in alert_message.text.lower(), f"delete category alert message not found."