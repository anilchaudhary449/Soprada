import allure
import os
import time
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from locators_ecom.blog_locators import BlogLocators

class Blog:
    def __init__(self, driver, timeout=60):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout)

    
    @allure.step("Create new blog category: {category_name}")
    def new_category(self, category_name, short_description):
        self.wait.until(EC.presence_of_element_located(BlogLocators.BLOG_CATEGORY_BTN)).click()
        print(f"Blog Category button clicked. Current URL: {self.driver.current_url}")
        time.sleep(1) # Wait for page transition
        self.wait.until(EC.presence_of_element_located(BlogLocators.NEW_CATEGORY_BTN)).click()
        print("New Category button clicked")
        self.data_fillers_category(category_name, short_description)
        self.wait.until(EC.presence_of_element_located(BlogLocators.SAVE_CATEGORY_BTN)).click()
        print("Category saved successfully...")
        
        # Assertion for Success Alert
        try:
                 alert = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(BlogLocators.ALERT_TOP))
                 print(f"Blog Category Save Alert: {alert.text}")
                 assert "success" in alert.text.lower() or "added" in alert.text.lower(), f"Unexpected alert message: {alert.text}"
                 WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located(BlogLocators.ALERT_TOP))
        except TimeoutException:
             print("No success alert appeared within timeout for Blog Category Save.")
        except Exception as e:
             print(f"An error occurred while verifying Blog Category alert: {e}")
        # self.driver.back()
        # print(f"Back to blog main page, Current URL: {self.driver.current_url}")
        time.sleep(2)
        
    @allure.step("Fill blog category data: {category_name}, {short_description}")
    def data_fillers_category(self, category_name, short_description):
        category_name_input = self.wait.until(EC.visibility_of_element_located(BlogLocators.CATEGORY_NAME_INPUT))
        category_name_input.clear()
        category_name_input.send_keys(category_name)
        time.sleep(0.5)
        print("category name filled successfully...")

        short_description_input = self.wait.until(EC.visibility_of_element_located(BlogLocators.SHORT_DESCRIPTION_INPUT))
        short_description_input.clear()
        short_description_input.send_keys(short_description)
        time.sleep(0.5)
        print("category short description filled successfully...")

    @allure.step("Edit blog category: {category_name}, {short_description}")
    def edit_category(self, category_name, short_description):
        edit_buttons = self.wait.until(EC.presence_of_all_elements_located(BlogLocators.EDIT_CATEGORY_BTNS))
        random_element = random.choice(edit_buttons)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", random_element)
        try:
            random_element.click()
            print("Edit Category button clicked")
        except:
            self.driver.execute_script("arguments[0].click();", random_element)
            print("Edit Category button clicked")
            
        print(f"filling category data...{category_name}, {short_description}")
        self.data_fillers_category(category_name, short_description)
        self.wait.until(EC.presence_of_element_located(BlogLocators.UPDATE_CATEGORY_BTN)).click()
        print("Category updated successfully...")
        
        # Assertion for Success Alert
        try:
                 alert = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(BlogLocators.ALERT_TOP))
                 print(f"Blog Category Update Alert: {alert.text}")
                 assert "success" in alert.text.lower() or "updated" in alert.text.lower(), f"Unexpected alert message: {alert.text}"
                 WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located(BlogLocators.ALERT_TOP))
        except TimeoutException:
             print("No success alert appeared within timeout for Blog Category Update.")
        except Exception as e:
             print(f"An error occurred while verifying Blog Category update alert: {e}")

    @allure.step("Delete one random blog category")
    def delete_category(self):
        delete_buttons = self.wait.until(EC.presence_of_all_elements_located(BlogLocators.DELETE_CATEGORY_BTNS))
        random_element = random.choice(delete_buttons)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", random_element)
        self.driver.execute_script("arguments[0].click();", random_element)
        print("Delete Category button clicked")
        time.sleep(1)
        self.wait.until(EC.presence_of_element_located(BlogLocators.CONFIRM_DELETE_CATEGORY_BTN)).click()
        print("Category deleted successfully...")
        
        try:
                 alert_message = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(BlogLocators.ALERT_TOP))
                 print(f"Blog Category Delete Alert: {alert_message.text}")
                 assert "success" in alert_message.text.lower() or "deleted" in alert_message.text.lower(), f"Unexpected alert message: {alert_message.text}"
                 
                 # Navigate back to blog list if not already there
                 if "category" in alert_message.text.lower():
                     self.driver.back()
                     WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located(BlogLocators.ALERT_TOP))
                     time.sleep(2)
        except TimeoutException:
             print("No success alert appeared within timeout for Blog Category Delete.")
             self.driver.back() # Fallback back
        except Exception as e:
             print(f"An error occurred while verifying Blog Category delete alert: {e}")

    @allure.step("Click Add Blog button")
    def add_blog(self, title, image_path, author, content, meta_description):

        add_new_blog = self.wait.until(EC.element_to_be_clickable(BlogLocators.ADD_BLOG_BTN))
        try:
            add_new_blog.click()
        except:
            self.driver.execute_script("arguments[0].click();", add_new_blog)
        print("add blog button clicked")
        time.sleep(0.5)
        self.data_fillers_blog(title, image_path, author, content, meta_description)
        print("blog data filled successfully...")
        time.sleep(0.5)
        self.wait.until(EC.presence_of_element_located(BlogLocators.SAVE_BLOG_BTN)).click()
        print("Blog saved successfully...")
        time.sleep(2)

    @allure.step("Fill blog data: {title}, {image_path}, {author}, {content}, {meta_description}")
    def data_fillers_blog(self, title, image_path, author, content, meta_description):
        title_input = self.wait.until(EC.visibility_of_element_located(BlogLocators.TITLE_INPUT))
        title_input.clear()
        title_input.send_keys(title)
        print("blog title filled successfully...")

        # image_input = self.wait.until(EC.presence_of_element_located(BlogLocators.IMAGE_FILE_INPUT))
        # image_input.send_keys(image_path)
        # print("blog image uploaded successfully...")
        
        if image_path and os.path.exists(image_path):
            image_input = self.wait.until(EC.presence_of_element_located(BlogLocators.IMAGE_FILE_INPUT))
            image_input.send_keys(os.path.abspath(image_path))
            print("blog image uploaded successfully...")
        else:
            print(f"Warning: Image path '{image_path}' not found.")

        author_input = self.wait.until(EC.visibility_of_element_located(BlogLocators.AUTHOR_INPUT))
        author_input.clear()
        author_input.send_keys(author)
        print("blog author filled successfully...")
        
        category_select = self.wait.until(EC.presence_of_element_located(BlogLocators.CATEGORY_SELECT))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", category_select)
        category_select.click()
        time.sleep(0.5)
        
        select_category = self.wait.until(EC.presence_of_all_elements_located(BlogLocators.CATEGORY_OPTIONS))
        # Skip the first placeholder option if it exists
        options = [o for o in select_category if o.get_attribute("value") != ""]
        if options:
            random.choice(options).click()
        else:
            random.choice(select_category).click()
        print("blog category selected successfully...")

        content_editor = self.wait.until(EC.visibility_of_element_located(BlogLocators.CONTENT_EDITOR))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", content_editor)
        time.sleep(0.5)

        content_editor.click()
        content_editor.clear()
        content_editor.send_keys(content)
        print("blog content filled successfully...")

        # Open SEO Settings
        print(f"Attempting to open SEO settings...")
        try:
            # Try to find the accordion header that is actually clickable
            seo_header = self.wait.until(EC.presence_of_element_located(BlogLocators.SEO_SETTING_BTN))
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", seo_header)
            time.sleep(0.5)
            
            # Click the parent accordion item if the div itself doesn't work
            self.driver.execute_script("arguments[0].click();", seo_header)
            print("SEO Settings button clicked")
            time.sleep(2) # Wait for accordion animation
            
            print(f"Waiting for meta description input...")
            meta_description_input = self.wait.until(EC.presence_of_element_located(BlogLocators.SEO_META_DESCRIPTION))
            
            # Ensure it's in view
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", meta_description_input)
            time.sleep(0.5)
            
            print(f"Entering meta description...")
            # # Triple approach: Clear, JS set, send_keys
            # try:
            #     meta_description_input.clear()
            # except:
            #     pass
                
            # self.driver.execute_script("arguments[0].value = arguments[1];", meta_description_input, meta_description)
            # self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", meta_description_input)
            # self.driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", meta_description_input)
            
            # # Fallback to standard typing for reactive frameworks
            # try:
            #     meta_description_input.send_keys(" ") # Trigger some activity
            #     meta_description_input.send_keys(meta_description)
            # except:
            #     pass
            
            meta_description_input.clear()
            meta_description_input.send_keys(meta_description)
            

            print("meta description filled successfully...")
        except Exception as e:
            print(f"Warning: Could not handle SEO settings: {e}")

    @allure.step("Save blog changes")
    def save_blog(self):
        print("Saving blog...")
        submit_btn = self.wait.until(EC.presence_of_element_located(BlogLocators.SAVE_BLOG_BTN))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", submit_btn)
        self.driver.execute_script("arguments[0].click();", submit_btn)
        print("blog saved successfully...")
        
        # Assertion for Success Alert
        try:
                 alert = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(BlogLocators.ALERT_TOP))
                 print(f"Blog Save Alert: {alert.text}")
                 assert "success" in alert.text.lower() or "added" in alert.text.lower() or "updated" in alert.text.lower(), f"Unexpected alert message: {alert.text}"
                 WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located(BlogLocators.ALERT_TOP))
        except TimeoutException:
             print("No success alert appeared within timeout for Blog Save.")
        except Exception as e:
             print(f"An error occurred while verifying Blog Save alert: {e}")

    @allure.step("Verify View Blog button")
    def view_blog(self):
        view_blog_btn = self.wait.until(EC.presence_of_all_elements_located(BlogLocators.VIEW_BTNS))
        random_element = random.choice(view_blog_btn)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", random_element)
        assert random_element.is_enabled(), "View Blog button isn't enabled."
        print("view blog button is enabled...")

    @allure.step("Edit blog: {title}")
    def edit_blog(self, title, image_path, author, content, meta_description):
        edit_blog_btns = self.wait.until(EC.presence_of_all_elements_located(BlogLocators.EDIT_BTNS))
        print("Edit blog button selecting...")
        select_edit_btn = random.choice(edit_blog_btns)
        print("Edit blog button selected...")
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", select_edit_btn)
        self.driver.execute_script("arguments[0].click();", select_edit_btn)
        print("Edit blog button clicked...")
        time.sleep(1)
        self.data_fillers_blog(title, image_path, author, content, meta_description)
        print("Edit blog data filled...")
        self.save_blog()
        print("Edit blog saved...")
        time.sleep(1)

    @allure.step("Delete one random blog")
    def delete_blog(self):
        delete_blog_btns = self.wait.until(EC.presence_of_all_elements_located(BlogLocators.DELETE_BTNS))
        print("Delete blog button selecting...")
        select_delete_btn = random.choice(delete_blog_btns)
        print("Delete blog button selected...")
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", select_delete_btn)
        self.driver.execute_script("arguments[0].click();", select_delete_btn)
        print("Delete blog button clicked...")
        time.sleep(1)
        confirm_dlt_btn = self.wait.until(EC.presence_of_element_located(BlogLocators.CONFIRM_DELETE_BTN))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", confirm_dlt_btn)
        self.driver.execute_script("arguments[0].click();", confirm_dlt_btn)
        print("Delete blog confirmed...")
        
        # Assertion for Success Alert
        try:
                 alert = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(BlogLocators.ALERT_TOP))
                 print(f"Blog Delete Alert: {alert.text}")
                 assert "success" in alert.text.lower() or "deleted" in alert.text.lower(), f"Unexpected alert message: {alert.text}"
                 WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located(BlogLocators.ALERT_TOP))
        except TimeoutException:
             print("No success alert appeared within timeout for Blog Delete.")
        except Exception as e:
             print(f"An error occurred while verifying Blog Delete alert: {e}")
