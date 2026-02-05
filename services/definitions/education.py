from services.base_service import BaseService, ServiceType
import time

class UdimaService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "UDIMA"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.udima.es/'

    def run(self):
        try:
            self.browser.set_page_load_timeout(30)
            if not self.navigate(): return
        except: return

        self.accept_cookies("//a[contains(@class, 'ok') or contains(text(), 'Aceptar')]")
        
        try:
            # Look for "Solicita información" or similar form
            # Usually on potential students pages or landing
            # We try to find a phone input in the main page or header callback
            
            # UDIMA often has a "Te llamamos gratis" button or form on lateral
            self.fill("//input[contains(@id, 'edit-field-telefono') or contains(@name, 'telefono')]", self.data['phone'])
            
            # Checkbox for privacy if needed (approximated)
            try:
                self.click("//input[contains(@id, 'edit-policy') or @type='checkbox']")
            except: pass
            
            self.click("//input[@type='submit' and (@id='edit-submit' or contains(@value, 'Enviar'))]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')

class UniversidadEuropeaService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "U.Europea"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://universidadeuropea.com/'

    def run(self):
        try:
             self.browser.set_page_load_timeout(30)
             if not self.navigate(): return
        except: return
        
        self.accept_cookies("//button[contains(text(), 'Aceptar') or contains(@id, 'onetrust-accept')]")
        try:
            self.click("//*[contains(text(), 'Te llamamos') or contains(@class, 'phone')]")
            time.sleep(1)
            self.fill("//input[@type='tel' or contains(@name, 'phone')]", self.data['phone'])
            
             # Try name too if requested
            try:
                self.fill("//input[contains(@name, 'firstname')]", self.data['name'])
                self.fill("//input[contains(@name, 'lastname')]", self.data['surname'])
            except: pass

            self.click("//button[contains(text(), 'Llamadme') or contains(text(), 'Enviar')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
             self.log(f'Error: {e}', status='ERROR')

class IsabelIService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "U.Isabel I"
        self.types = [ServiceType.CALL]
        self.url = 'https://www.ui1.es/'

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

class UAXService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "UAX"
        self.types = [ServiceType.CALL]
        self.url = 'https://www.uax.com/'

    def run(self):
        try:
            self.browser.set_page_load_timeout(30)
            if not self.navigate(): return
        except: return
        self.accept_cookies("//button[contains(text(), 'Aceptar')]")
        try:
            self.click("//*[contains(text(), 'Te llamamos') or contains(@class, 'phone')]")
            time.sleep(1)
            self.fill("//input[contains(@name, 'phone') or @type='tel']", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme') or contains(text(), 'Enviar')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')
