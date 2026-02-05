from services.base_service import BaseService, ServiceType
import time

class TecnocasaService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Tecnocasa"
        self.types = [ServiceType.CALL]
        self.url = 'https://www.tecnocasa.es/'

    def run(self):
        try:
            self.browser.set_page_load_timeout(30)
            if not self.navigate(): return
        except: return
        
        # Cookie acceptance
        self.accept_cookies("//button[contains(@class, 'cc-btn') or contains(@class, 'cookie')]")
        
        try:
            # Navigate to valuation or contact if needed, but often quick contact is available
            # Or "Valorar casa gratis"
            self.click("//a[contains(text(), 'Valoración gratuita') or contains(@href, 'valoracion')]")
            time.sleep(2)
            
            self.fill("//input[@name='telefono' or @id='telefono']", self.data['phone'])
            self.fill("//input[@name='nombre']", self.data['name'])
            
            # Privacy check
            try:
                self.click("//input[@type='checkbox' and contains(@name, 'privacy')]")
            except: pass

            self.click("//button[@type='submit' and contains(., 'Enviar')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')
