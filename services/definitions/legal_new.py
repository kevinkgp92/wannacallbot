from services.base_service import BaseService, ServiceType
import time

class LegalitasService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Legalitas"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.legalitas.com/'

    def run(self):
        try:
            self.browser.set_page_load_timeout(30)
            if not self.navigate(): return
        except: return
        
        self.accept_cookies("//button[contains(text(), 'Aceptar') or contains(@id, 'onetrust-accept')]")
        
        try:
            # Legalitas often has a sticky header or hero form
            # Looking for common callback selectors
            self.fill("//input[contains(@name, 'phone') or contains(@id, 'phone')]", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme') or contains(text(), 'Te llamamos')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')

class ArriagaService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Arriaga Asociados"
        self.types = [ServiceType.CALL]
        self.url = 'https://www.arriagaasociados.com/'

    def run(self):
        try:
            self.browser.set_page_load_timeout(30)
            if not self.navigate(): return
        except: return
        
        self.accept_cookies("//button[contains(text(), 'Aceptar') or contains(@id, 'cookie')]")
        
        try:
            self.fill("//input[contains(@name, 'telefono') or @type='tel']", self.data['phone'])
            self.click("//button[contains(text(), 'Te llamamos') or contains(text(), 'Enviar')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')
