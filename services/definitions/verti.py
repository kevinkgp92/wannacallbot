from services.base_service import BaseService, ServiceType
from selenium.webdriver.common.by import By
import time

class VertiService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Verti Seguros"
        self.types = [ServiceType.CALL]
        self.url = "https://www.verti.es/te-llamamos/"

    def run(self):
        try:
            self.browser.set_page_load_timeout(30)
            if not self.navigate(): return
        except: return
        
        self.accept_cookies("//button[contains(@id, 'onetrust-accept')]")
        
        try:
            # Look for the phone input
            self.fill("//input[@name='telefono' or @type='tel']", self.data['phone'])
            
            # Checkbox for privacy (usually required)
            try:
                self.click("//input[@type='checkbox']")
            except: pass

            self.click("//button[@type='submit' or contains(text(), 'Llamadme')]")
            self.log("Solicitud enviada", "OK")
            time.sleep(2)
        except Exception as e:
            self.log(f"Error: {e}", "ERROR")
