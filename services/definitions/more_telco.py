from services.base_service import BaseService, ServiceType
import time

class O2Service(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "O2"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://o2online.es/'

    def run(self):
        try:
             self.browser.set_page_load_timeout(30)
             if not self.navigate(): return
        except: return
        
        self.accept_cookies("//button[contains(@id, 'onetrust-accept')]")
        try:
            # Sticky button often present
            self.click("//*[contains(text(), 'Te llamamos')]")
            time.sleep(1)
            self.fill("//input[@name='phone' or @type='tel']", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')

class SimyoService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Simyo"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.simyo.es/'

    def run(self):
        try:
             self.browser.set_page_load_timeout(30)
             if not self.navigate(): return
        except: return
        
        self.accept_cookies("//button[contains(text(), 'Aceptar')]")
        try:
            self.click("//*[contains(text(), 'Te llamamos')]")
            time.sleep(1)
            # Simyo often puts the input in a modal
            self.fill("//input[@name='msisdn' or @type='tel']", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')

class YoigoService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Yoigo"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.yoigo.com/'

    def run(self):
        try:
             self.browser.set_page_load_timeout(30)
             if not self.navigate(): return
        except: return
        
        self.accept_cookies("//button[contains(text(), 'Aceptar') or contains(text(), 'Permitir')]")
        try:
            self.click("//*[contains(text(), 'Te llamamos')]")
            time.sleep(1)
            self.fill("//input[@name='phone' or contains(@placeholder, 'Teléfono')]", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme') or contains(text(), 'Solicitar')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')

class JazztelService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Jazztel"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.jazztel.com/'

    def run(self):
        try:
             self.browser.set_page_load_timeout(30)
             if not self.navigate(): return
        except: return
        
        self.accept_cookies("//button[contains(text(), 'Aceptar')]")
        try:
            self.click("//*[contains(text(), 'Te llamamos gratis') or contains(text(), 'Llamadme')]")
            time.sleep(1)
            self.fill("//input[@name='telefono' or contains(@id, 'phone')]", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')

class MasMovilService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "MasMovil"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.masmovil.es/'

    def run(self):
        try:
             self.browser.set_page_load_timeout(30)
             if not self.navigate(): return
        except: return
        
        self.accept_cookies("//button[contains(text(), 'Aceptar') or contains(@id, 'onetrust-accept')]")
        try:
            self.click("//*[contains(text(), 'Te llamamos')]")
            time.sleep(1)
            self.fill("//input[@name='phone' or contains(@id, 'phone')]", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme') or contains(text(), 'Enviar')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')

class LowiService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Lowi"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.lowi.es/'

    def run(self):
        try:
            self.browser.set_page_load_timeout(30)
            if not self.navigate(): return
        except: return
        
        self.accept_cookies("//button[contains(@id, 'onetrust-accept')]")
        
        try:
            self.click("//*[contains(text(), 'Te llamamos') or contains(text(), 'Llámanos')]")
            time.sleep(1)
            
            self.fill("//input[@type='tel' or contains(@name, 'phone')]", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme') or contains(text(), 'Enviar')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')

class AdamoService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Adamo"
        self.types = [ServiceType.CALL]
        self.url = 'https://adamo.es/'

    def run(self):
        try:
             self.browser.set_page_load_timeout(30)
             if not self.navigate(): return
        except: return
        
        self.accept_cookies("//button[contains(text(), 'Aceptar')]")
        try:
            self.click("//*[contains(text(), 'Te llamamos') or contains(@class, 'c-header-phone')]")
            time.sleep(1)
            self.fill("//input[@type='tel']", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
             self.log(f'Error: {e}', status='ERROR')
