from services.base_service import BaseService, ServiceType
from selenium.webdriver.common.by import By
import time

class RaceService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "RACE"
        self.types = [ServiceType.CALL]
        self.url = "https://www.race.es/te-llamamos-gratis"

    def run(self):
        try:
            self.browser.set_page_load_timeout(30)
            if not self.navigate(): return
        except: return
        
        self.accept_cookies("//button[contains(@id, 'didomi-notice-agree-button')]")
        
        try:
            # Form should be visible
            self.fill("//input[@name='phone' or @type='tel']", self.data['phone'])
            
            # Checkbox
            try:
                self.click("//input[@type='checkbox']")
            except: pass
            
            self.click("//button[@type='submit' or contains(text(), 'Enviar')]")
            self.log("Solicitud enviada", "OK")
            time.sleep(2)
        except Exception as e:
             # Try trigger if form not direct
             try:
                 self.click("//*[contains(text(), 'Te llamamos')]")
                 time.sleep(1)
                 self.fill("//input[@name='phone' or @type='tel']", self.data['phone'])
                 self.click("//button[@type='submit' or contains(text(), 'Enviar')]")
                 self.log("Solicitud enviada (Trigger Mode)", "OK")
                 return
             except: pass
             self.log(f"Error: {e}", "ERROR")
