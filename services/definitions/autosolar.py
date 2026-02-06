from services.base_service import BaseService, ServiceType
from selenium.webdriver.common.by import By
import time

class AutoSolarService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "AutoSolar"
        self.types = [ServiceType.CALL]
        self.url = "https://autosolar.es/contact" 

    def run(self):
        try:
            self.browser.set_page_load_timeout(30)
            if not self.navigate(): return
        except: return
        
        self.accept_cookies("//button[contains(@class, 'cc-btn-accept-all')]")
        
        try:
            self.fill("//input[@name='nombre']", self.data['name'])
            self.fill("//input[@name='email']", self.data['email'])
            self.fill("//input[@name='telefono']", self.data['phone'])
            
            # Privacy check
            try:
                self.click("//input[@name='privacidad']")
            except: pass

            self.click("//button[@type='submit']")
            self.log("Solicitud enviada", "OK")
            time.sleep(2)
        except Exception as e:
            self.log(f"Error: {e}", "ERROR")
