from services.base_service import BaseService, ServiceType
import time

class EndesaService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Endesa"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.endesa.com/es'

    def run(self):
        try:
             self.browser.set_page_load_timeout(30)
             if not self.navigate(): return
        except: return
        
        self.accept_cookies("//button[contains(text(), 'Aceptar') or contains(@id, 'cookie')]")
        try:
            self.click("//*[contains(text(), 'Te llamamos')]")
            time.sleep(2)
            self.fill("//input[@name='phone' or contains(@placeholder, 'Teléfono')]", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')

class NaturgyService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Naturgy"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.naturgy.es/'

    def run(self):
        try:
             self.browser.set_page_load_timeout(30)
             if not self.navigate(): return
        except: return
        
        self.accept_cookies("//button[contains(text(), 'Aceptar')]")
        try:
            self.click("//*[contains(text(), '¿Hablamos?') or contains(text(), 'Te llamamos')]")
            time.sleep(2) # Wait for modal
            self.fill("//input[@type='tel' or contains(@name, 'phone')]", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme') or contains(text(), 'Enviar')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
             self.log(f'Error: {e}', status='ERROR')

class IberdrolaService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Iberdrola"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.iberdrola.es/'

    def run(self):
        try:
             self.browser.set_page_load_timeout(30)
             if not self.navigate(): return
        except: return

        self.accept_cookies("//button[contains(text(), 'Aceptar') or contains(text(), 'Permitirlas todas')]")
        try:
            self.click("//*[contains(text(), 'Te llamamos')]")
            time.sleep(2)
            self.fill("//input[contains(@name, 'telefono') or contains(@id, 'phone')]", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')

class TotalEnergiesService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "TotalEnergies"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.totalenergies.es/es/hogares'

    def run(self):
        try:
             self.browser.set_page_load_timeout(30)
             if not self.navigate(): return
        except: return

        self.accept_cookies("//button[contains(@id, 'onetrust-accept')]")
        try:
            self.click("//*[contains(text(), 'Te llamamos') or contains(@class, 'c-contact-header')]")
            time.sleep(1)
            self.fill("//input[@name='phone' or contains(@id, 'phone')]", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme') or contains(text(), 'Enviar')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')

class RepsolService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Repsol"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.repsol.es/'

    def run(self):
        try:
             self.browser.set_page_load_timeout(30)
             if not self.navigate(): return
        except: return

        self.accept_cookies("//button[contains(text(), 'Aceptar') or contains(@id, 'onetrust-accept')]")
        try:
            # Repsol usually has a floating button or in the footer/header
            self.click("//*[contains(text(), 'Te llamamos') or contains(@data-testid, 'callback')]")
            time.sleep(1)
            self.fill("//input[@name='telephone' or contains(@id, 'phone')]", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme') or contains(text(), 'Solicitar')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')

class HolaluzService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Holaluz"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.holaluz.com/'

    def run(self):
        try:
            self.browser.set_page_load_timeout(30)
            if not self.navigate(): return
        except: return
        
        self.accept_cookies("//button[contains(text(), 'Aceptar') or contains(@id, 'onetrust-accept')]")
        
        try:
            self.click("//*[contains(text(), 'Te llamamos') or contains(text(), 'Llámanos')]")
            time.sleep(1)
            
            self.fill("//input[@type='tel' or contains(@name, 'phone')]", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme') or contains(text(), 'Enviar')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')

class FactorEnergiaService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "FactorEnergia"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.factorenergia.com/'

    def run(self):
        try:
            self.browser.set_page_load_timeout(30)
            if not self.navigate(): return
        except: return
        
        self.accept_cookies("//button[@id='onetrust-accept-btn-handler']")
        
        try:
            # Often a floating widget or specific form
            self.fill("//input[@id='phone' or @name='phone' or @type='tel']", self.data['phone'])
            self.click("//button[contains(@class, 'btn') and (contains(., 'Llamadme') or contains(., 'gratis'))]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')

class LuceraService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Lucera"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://lucera.es/'

    def run(self):
        try:
             self.browser.set_page_load_timeout(30)
             if not self.navigate(): return
        except: return
        
        self.accept_cookies("//button[contains(text(), 'Aceptar') or contains(@class, 'cookies')]")
        try:
             # Often has a floating 'Te llamamos'
            self.click("//*[contains(text(), 'Te llamamos gratis')]")
            time.sleep(1)
            self.fill("//input[@type='tel' or contains(@name, 'phone')]", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
             self.log(f'Error: {e}', status='ERROR')
