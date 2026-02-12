import allure
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from locators_ecom.sidebar_locators import SidebarLocators

class Sidebar:
    def __init__(self, driver, timeout=60):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout)

    @allure.step("Navigate to {text}")
    def navigate(self, text):
        # Wait for any potential blocking modals to disappear
        try:
            WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located(SidebarLocators.ACTIVE_MODAL))
        except:
            pass

        # Get locator from SidebarLocators
        locator = SidebarLocators.SIDEBAR_ITEM(text)
        
        for i in range(3):
            try:
                elem = self.wait.until(EC.element_to_be_clickable(locator))
                
                # Ensure element is not obscured by a header or footer
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", elem)
                time.sleep(1)
                
                try:
                    elem.click()
                except:
                    self.driver.execute_script("arguments[0].click();", elem)
                
                # Wait for URL to change or at least a small delay for navigation
                time.sleep(2)
                
                # Verify navigation (optional but helpful)
                print(f"Navigated to {text}. Current URL: {self.driver.current_url}")
                return
            except StaleElementReferenceException:
                print(f"Stale sidebar element for {text}, retrying...")
                time.sleep(1)
            except Exception as e:
                if i == 2: raise e
                time.sleep(1)

    def navigate_to_dashboard(self):
        self.navigate('Dashboard')

    def navigate_to_custom_domain(self):
        self.navigate('Custom Domain')

    def navigate_to_category(self):
        self.navigate('Category')

    def navigate_to_product(self):
        self.navigate('Products')
    
    def navigate_to_inventory_management(self):
        self.navigate('Inventory Management')

    def navigate_to_variant(self):
        self.navigate('Variants')

    def navigate_to_order(self):
        self.navigate('Orders')

    def navigate_to_shipping_charge_settings(self):
        self.navigate('Shipping Charge Settings')

    def navigate_to_customer(self):
        self.navigate('Customers')

    def navigate_to_review(self):
        self.navigate('Reviews')

    def navigate_to_enquiry(self):
        self.navigate('Enquiries')

    def navigate_to_support_case(self):
        self.navigate('Support Case')

    def navigate_to_blog(self):
        self.navigate('Blogs')

    def navigate_to_marketing(self):
        self.navigate('Marketing')

    def navigate_to_sliders(self):
        self.navigate('Sliders')

    def navigate_to_themes(self):
        self.navigate('Themes')

    def navigate_to_plugins(self):
        self.navigate('Plugins')

    def navigate_to_staff(self):
        self.navigate('Staff')

    def navigate_to_payments(self):
        self.navigate('Payments')

    def navigate_to_settings(self):
        self.navigate('Settings')
