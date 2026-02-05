from services.base_service import BaseService, ServiceType
import time
from selenium.webdriver.common.by import By

class LegalionService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Legalion"
        self.types = [ServiceType.CALL]
        self.url = 'https://legalionabogados.com/'

    def run(self):
        try:
             self.browser.set_page_load_timeout(30)
             if not self.navigate(): return
        except: return
        
        self.accept_cookies("//button[contains(text(), 'Aceptar') or contains(@class, 'cookie')]")
        try:
            # Often has a floating button or hero form
            self.click("//*[contains(text(), 'Te llamamos gratis') or contains(@class, 'whatsapp') or contains(@class, 'phone')]")
            time.sleep(1)
            
            self.fill("//input[@type='tel' or contains(@name, 'phone')]", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme') or contains(text(), 'Enviar')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
             self.log(f'Error: {e}', status='ERROR')
