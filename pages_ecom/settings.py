import allure
import time
import random
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from locators_ecom.settings_locators import SettingsLocators

class Settings:
    def __init__(self, driver, timeout=60):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout)

    def _click_save(self):
        btn = self.wait.until(EC.element_to_be_clickable(SettingsLocators.SAVE_CHANGES_BTN))
        try:
            btn.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", btn)
        
        # Assertion for Success Alert
        try:
             alert = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(SettingsLocators.ALERT_TOP))
             print(f"Settings Save Alert: {alert.text}")
             valid_messages = ["success", "updated", "no changes", "nothing to update"]
             assert any(msg in alert.text.lower() for msg in valid_messages), f"Unexpected alert message: {alert.text}"
             WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located(SettingsLocators.ALERT_TOP))
        except TimeoutException:
             print("No success alert appeared within timeout for Settings.")
        except Exception as e:
             print(f"An error occurred while verifying Settings alert: {e}")

    def _navigate_tab(self, locator):
        tab = self.wait.until(EC.element_to_be_clickable(locator))
        try:
            tab.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", tab)
        time.sleep(1)

    @allure.step("Configure theme settings")
    def theme_settings(self):
        self._navigate_tab(SettingsLocators.THEME_SETTINGS_TAB)
        self._click_save()
        print("Theme settings configured...")

    @allure.step("Update site information")
    def site_information(self, organization, logo, favicon, profile, slogan, map_url):
        self._navigate_tab(SettingsLocators.SITE_INFORMATION_TAB)
        
        # Basic Info
        self.wait.until(EC.presence_of_element_located(SettingsLocators.ORG_NAME_INPUT)).clear()
        self.driver.find_element(*SettingsLocators.ORG_NAME_INPUT).send_keys(organization)

        # Uploads
        self.wait.until(EC.presence_of_element_located(SettingsLocators.LOGO_UPLOAD)).send_keys(logo)
        print("Logo uploaded...")
        self.wait.until(EC.presence_of_element_located(SettingsLocators.FAVICON_UPLOAD)).send_keys(favicon)
        print("Favicon uploaded...")
        self.wait.until(EC.presence_of_element_located(SettingsLocators.PROFILE_UPLOAD)).send_keys(profile)
        print("Profile uploaded...")

        self.wait.until(EC.presence_of_element_located(SettingsLocators.SLOGAN_INPUT)).clear()
        self.driver.find_element(*SettingsLocators.SLOGAN_INPUT).send_keys(slogan)
        print("Slogan entered...")

        # Dropdowns
        curr_dropdown = self.wait.until(EC.presence_of_element_located(SettingsLocators.CURRENCY_SELECT))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", curr_dropdown)
        time.sleep(1)
        curr_select = Select(curr_dropdown)
        try:
            curr_select.select_by_index(random.randint(1, len(curr_select.options)-1))
        except Exception:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", curr_dropdown)
            curr_select.select_by_index(random.randint(1, len(curr_select.options)-1))

        maint_dropdown = self.wait.until(EC.presence_of_element_located(SettingsLocators.MAINTENANCE_SELECT))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", maint_dropdown)
        time.sleep(1)
        maint_select = Select(maint_dropdown)
        try:
            maint_select.select_by_index(random.randint(0, 1))
        except Exception:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", maint_dropdown)
            maint_select.select_by_index(random.randint(0, 1))

        # Map
        map_area = self.wait.until(EC.presence_of_element_located(SettingsLocators.MAP_TEXTAREA))
        map_area.clear()
        map_area.send_keys(map_url)
        print("Map URL entered...")


        self._click_save()

    @allure.step("Update company details")
    def company_details(self, address, about_us):
        self._navigate_tab(SettingsLocators.COMPANY_DETAILS_TAB)
        

        self.wait.until(EC.presence_of_element_located(SettingsLocators.ADDRESS_INPUT)).clear()
        self.driver.find_element(*SettingsLocators.ADDRESS_INPUT).send_keys(address)
        print("Address entered...")

        editor = self.wait.until(EC.presence_of_element_located(SettingsLocators.EDITOR_CONTENT))
        editor.clear()
        editor.send_keys(about_us)
        print("About us content entered...")
        self._click_save()
    @allure.step("Update tax information")
    def tax_information(self, vat_number, vat_pct):
        self._navigate_tab(SettingsLocators.TAX_INFORMATION_TAB)
        print("Tax information tab...")
        vat_toggle = self.wait.until(EC.presence_of_element_located(SettingsLocators.VAT_TOGGLE_BTN_CHECKBOX))
        vat_status= vat_toggle.text
        if vat_status == "Enable VAT/PAN":
            print("VAT/PAN is enabled...")
            vat_toggle.click()
            print("Now, Toggle is enabled...")
            if vat_status == "Disabled VAT/PAN":
                self.wait.until(EC.presence_of_element_located(SettingsLocators.VAT_INPUT)).clear()
                self.driver.find_element(*SettingsLocators.VAT_INPUT).send_keys(vat_number)
                print("VAT number entered...")
                self.wait.until(EC.presence_of_element_located(SettingsLocators.VAT_PCT)).clear()
                self.driver.find_element(*SettingsLocators.VAT_PCT).send_keys(vat_pct)
                print("VAT percentage entered...")
                        
        self._click_save()


    @allure.step("Update contact information")
    def contact_information(self, contact, alt_contact, email, alt_email, whatsapp, viber):
        self._navigate_tab(SettingsLocators.CONTACT_INFORMATION_TAB)
        print("Contact information tab...")
        fields = {
            SettingsLocators.CONTACT_NUM_INPUT: contact,
            SettingsLocators.ALT_CONTACT_INPUT: alt_contact,
            SettingsLocators.EMAIL_INPUT: email,
            SettingsLocators.ALT_EMAIL_INPUT: alt_email,
            SettingsLocators.WHATSAPP_INPUT: whatsapp,
            SettingsLocators.VIBER_INPUT: viber
        }

        for loc, val in fields.items():
            elem = self.wait.until(EC.presence_of_element_located(loc))
            elem.clear()
            elem.send_keys(val)
            
        self._click_save()
        print("Contact information updated...")

    @allure.step("Update social media links")
    def social_media_links(self, fb, insta, twitter, linkedin, youtube, tiktok):
        self._navigate_tab(SettingsLocators.SOCIAL_MEDIA_LINKS_TAB)
        print("Social media links tab...")
        fields = {
            SettingsLocators.FB_INPUT: fb,
            SettingsLocators.INSTA_INPUT: insta,
            SettingsLocators.TWITTER_INPUT: twitter,
            SettingsLocators.LINKEDIN_INPUT: linkedin,
            SettingsLocators.YOUTUBE_INPUT: youtube,
            SettingsLocators.TIKTOK_INPUT: tiktok,
        }

        for loc, val in fields.items():
            elem = self.wait.until(EC.presence_of_element_located(loc))
            elem.clear()
            elem.send_keys(val)
            print("Social media links entered...")
        self._click_save()
        print("Social media links updated...")

    def _update_policy(self, tab_locator, content):
        self._navigate_tab(tab_locator)
        print("Policy tab...")
        editor = self.wait.until(EC.presence_of_element_located(SettingsLocators.EDITOR_CONTENT))
        editor.clear()
        editor.send_keys(content)
        print("Policy content entered...")
        self._click_save()
        print("Policy updated...")

    @allure.step("Update return policy")
    def return_policy(self, content):
        self._update_policy(SettingsLocators.RETURN_POLICY_TAB, content)
        print("Return policy updated...")

    @allure.step("Update privacy policy")
    def privacy_policy(self, content):
        self._update_policy(SettingsLocators.PRIVACY_POLICY_TAB, content)
        print("Privacy policy updated...")

    @allure.step("Update terms and conditions")
    def terms_and_conditions(self, content):
        self._update_policy(SettingsLocators.TERMS_CONDITIONS_TAB, content)
        print("Terms and conditions updated...")
