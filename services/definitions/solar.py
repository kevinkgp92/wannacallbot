from services.base_service import BaseService, ServiceType
import time

class Solar360Service(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Solar360"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.solar360.es/'

    def run(self):
        try:
            self.browser.set_page_load_timeout(30)
            if not self.navigate(): return
        except: return
        
        self.accept_cookies("//button[contains(text(), 'Aceptar') or contains(@id, 'onetrust-accept')]")
        
        try:
            self.fill("//input[contains(@name, 'phone') or @type='tel']", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme') or contains(text(), 'Te llamamos')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')

class OtovoService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Otovo"
        self.types = [ServiceType.CALL]
        self.url = 'https://www.otovo.es/'

    def run(self):
        try:
            self.browser.set_page_load_timeout(30)
            if not self.navigate(): return
        except: return
        
        self.accept_cookies("//button[contains(text(), 'Aceptar')]")
        
        try:
            self.fill("//input[contains(@name, 'phone') or @type='tel']", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme') or contains(text(), 'Solicitar')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')

class AlternaService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Alterna"
        self.types = [ServiceType.CALL]
        self.url = 'https://alterna.online/'

    def run(self):
        try:
            self.browser.set_page_load_timeout(30)
            if not self.navigate(): return
        except: return
        
        self.accept_cookies("//button[contains(text(), 'Aceptar')]")
        
        try:
            self.fill("//input[contains(@name, 'phone') or @type='tel']", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme') or contains(text(), 'Enviar')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')
