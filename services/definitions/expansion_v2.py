from services.base_service import BaseService, ServiceType
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class VertiService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Verti Seguros"
        self.types = [ServiceType.INSURANCE]
        self.url = "https://www.verti.es/te-llamamos/"

    def run(self):
        self.browser.get(self.url)
        time.sleep(3)
        
        try:
            # Handle cookies
            try:
                self.browser.find_element(By.ID, "onetrust-accept-btn-handler").click()
                time.sleep(1)
            except: pass

            # Look for the phone input
            phone_input = self.browser.find_element(By.NAME, "telefono")
            phone_input.send_keys(self.data['phone'])
            
            # Checkbox for privacy
            try:
                checkbox = self.browser.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
                if not checkbox.is_selected():
                    # Try clicking label or js
                    try:
                        checkbox.click()
                    except:
                        self.browser.execute_script("arguments[0].click();", checkbox)
            except: pass

            submit_btn = self.browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_btn.click()
            self.log("Solicitud enviada", "OK")
            time.sleep(2)
        except Exception as e:
            self.log(f"Error: {e}", "ERROR")

class SicorService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Sicor Alarmas"
        self.types = [ServiceType.SECURITY]
        self.url = "https://www.sicor.com/es/hogar-y-negocios/"

    def run(self):
        self.browser.get(self.url)
        time.sleep(4)
        
        try:
             # Cookies
            try:
                self.browser.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll").click()
                time.sleep(1)
            except: pass

            # Locate generic form or "Te llamamos"
            # Sicor usually has a floating button or a form in the footer/hero
            # Let's try to access the direct form page if possible, or search in homepage
            
            inputs = self.browser.find_elements(By.CSS_SELECTOR, "input[type='tel']")
            if inputs:
                inputs[0].send_keys(self.data['phone'])
                
                # Checkbox
                checks = self.browser.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
                for c in checks:
                    try:
                        if not c.is_selected(): c.click()
                    except: 
                        self.browser.execute_script("arguments[0].click();", c)
                
                # Button "Llamadme"
                btns = self.browser.find_elements(By.CSS_SELECTOR, "button, input[type='submit']")
                for b in btns:
                    if "llama" in b.text.lower() or "enviar" in b.text.lower():
                        b.click()
                        self.log("Solicitud enviada (Home Form)", "OK")
                        return
            
            self.log("Formulario no encontrado", "WARN")

        except Exception as e:
            self.log(f"Error: {e}", "ERROR")

class AutoSolarService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "AutoSolar"
        self.types = [ServiceType.ENERGY, ServiceType.SOLAR]
        self.url = "https://autosolar.es/contact" 

    def run(self):
        self.browser.get(self.url)
        time.sleep(3)
        
        try:
             # Cookies
            try:
                self.browser.find_element(By.CLASS_NAME, "cc-btn-accept-all").click()
            except: pass

            self.browser.find_element(By.NAME, "nombre").send_keys(self.data['name'])
            self.browser.find_element(By.NAME, "email").send_keys(self.data['email'])
            self.browser.find_element(By.NAME, "telefono").send_keys(self.data['phone'])
            
            # Privacy check
            try:
                self.browser.find_element(By.NAME, "privacidad").click()
            except:
                 self.browser.execute_script("document.getElementsByName('privacidad')[0].click();")

            self.browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
            self.log("Solicitud enviada", "OK")
            time.sleep(2)
        except Exception as e:
            self.log(f"Error: {e}", "ERROR")

class RacesService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "RACE"
        self.types = [ServiceType.INSURANCE]
        self.url = "https://www.race.es/te-llamamos-gratis" # Deduced common URL pattern, will try main if fails

    def run(self):
        # Fallback to main page if deep link fails (heuristic)
        self.browser.get("https://www.race.es/")
        time.sleep(3)
        
        try:
            # Cookies
            try:
                 self.browser.find_element(By.ID, "didomi-notice-agree-button").click()
            except: pass

            # Look for "Te llamamos" trigger
            triggers = self.browser.find_elements(By.XPATH, "//*[contains(text(), 'Te llamamos')]")
            if triggers:
                try:
                    triggers[0].click()
                    time.sleep(2)
                except: pass
            
            # Now form should be visible (modal or page)
            phone_in = self.browser.find_element(By.NAME, "phone") # Generic guess
            phone_in.send_keys(self.data['phone'])
            
            chk = self.browser.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
            self.browser.execute_script("arguments[0].click();", chk)
            
            btn = self.browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
            btn.click()
            
            self.log("Solicitud enviada", "OK")
            time.sleep(2)
        except Exception as e:
            # Try specific url if main failed
            self.log(f"Error en flow principal: {e}. Intentando fallback...", "WARN")
