from services.base_service import BaseService, ServiceType
from selenium.webdriver.common.by import By
import time

class SicorService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Sicor Alarmas"
        self.types = [ServiceType.CALL]
        self.url = "https://www.sicor.com/es/hogar-y-negocios/"

    def run(self):
        try:
            self.browser.set_page_load_timeout(30)
            if not self.navigate(): return
        except: return
        
        self.accept_cookies("//button[contains(@id, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')]")
        
        try:
            # Locate generic form or "Te llamamos"
            self.fill("//input[@type='tel']", self.data['phone'])
            
            # Checkbox
            try:
                self.click("//input[@type='checkbox']")
            except: pass
            
            # Button "Llamadme"
            self.click("//button[contains(., 'llama') or contains(., 'Enviar')]")
            self.log("Solicitud enviada", "OK")
            time.sleep(2)
        except Exception as e:
             # Fallback if selectors changed
             try:
                 # Try a more broad search
                 inputs = self.browser.find_elements(By.CSS_SELECTOR, "input[type='tel']")
                 if inputs:
                     inputs[0].send_keys(self.data['phone'])
                     self.click("//button[contains(., 'llama') or contains(., 'Enviar')]")
                     self.log("Solicitud enviada (Fallback)", "OK")
                     return
             except: pass
             self.log(f"Error: {e}", "ERROR")
