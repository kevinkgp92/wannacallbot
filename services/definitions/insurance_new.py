from services.base_service import BaseService, ServiceType
import time

class LineaDirectaService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Linea Directa"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.lineadirecta.com/'

    def run(self):
        try:
             self.browser.set_page_load_timeout(45)
             if not self.navigate(): return
        except: return
        
        self.accept_cookies("//button[contains(text(), 'Aceptar') or contains(text(), 'Permitir')]")
        try:
            # Based on debug: has 'Llamadme gratis' button and 'nameInput'
            try:
                self.click("//*[contains(text(), 'Llamadme gratis') or contains(text(), 'Te llamamos')]")
                time.sleep(1)
            except: pass
            
            self.fill("//input[@id='nameInput' or contains(@name, 'telefono')]", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme') or contains(text(), 'Enviar')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')

class CaserService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Caser"
        self.types = [ServiceType.CALL]
        self.url = 'https://www.caser.es/'

    def run(self):
        try:
             self.browser.set_page_load_timeout(30)
             if not self.navigate(): return
        except: return
        
        self.accept_cookies("//button[contains(text(), 'Aceptar') or contains(@id, 'onetrust-accept')]")
        try:
            self.click("//*[contains(text(), 'Te llamamos gratis') or contains(@class, 'c-header__phone')]")
            time.sleep(1)
            # Caser often opens a sidebar or modal
            self.fill("//input[@name='telefono' or contains(@id, 'phone')]", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme') or contains(text(), 'Solicitar')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
             self.log(f'Error: {e}', status='ERROR')

class MutuaService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Mutua Madrileña"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.mutua.es/'

    def run(self):
        try:
             self.browser.set_page_load_timeout(30)
             if not self.navigate(): return
        except: return

        self.accept_cookies("//button[contains(text(), 'Aceptar') or contains(@id, 'onetrust-accept')]")
        try:
             # Look for sticky phone callback
            self.click("//*[contains(text(), 'Te llamamos') or contains(@class, 'call-me')]")
            time.sleep(1)
            self.fill("//input[contains(@name, 'telefono')]", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')

class AxaService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Axa"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.axa.es/seguros-coche'

    def run(self):
        try:
            self.browser.set_page_load_timeout(60)
            from selenium.common.exceptions import TimeoutException
            try:
                self.browser.get(self.url)
            except TimeoutException:
                pass # Proceed even if timeout occurs
            time.sleep(5) # Give it time to render
        except: return
        
        self.accept_cookies("//button[contains(@id, 'onetrust-accept')]")
        
        try:
            self.click("//*[contains(text(), 'Te llamamos') or contains(@class, 'icon-phone')]")
            time.sleep(1)
            
            self.fill("//input[contains(@name, 'telefono') or contains(@id, 'phone')]", self.data['phone'])
            # Sometimes asks for name too
            try:
                self.fill("//input[contains(@name, 'nombre')]", self.data['name'])
            except: pass
            
            self.click("//button[contains(text(), 'Llamadme') or contains(text(), 'Enviar')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')

class SantaluciaService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Santalucia"
        self.types = [ServiceType.CALL]
        self.url = 'https://www.santalucia.es/'

    def run(self):
        try:
             self.browser.set_page_load_timeout(30)
             if not self.navigate(): return
        except: return
        
        self.accept_cookies("//button[contains(text(), 'Aceptar') or contains(@id, 'onetrust-accept')]")
        try:
            self.click("//*[contains(text(), 'Te llamamos') or contains(@class, 'phone')]")
            time.sleep(1)
            self.fill("//input[@type='tel' or contains(@name, 'telefono')]", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme') or contains(text(), 'Enviar')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
             self.log(f'Error: {e}', status='ERROR')

class AllianzService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Allianz"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.allianz.es/'

    def run(self):
        try:
             self.browser.set_page_load_timeout(30)
             if not self.navigate(): return
        except: return
        
        self.accept_cookies("//button[contains(text(), 'Aceptar') or contains(@id, 'onetrust-accept')]")
        try:
            self.click("//*[contains(text(), 'Te llamamos') or contains(@title, 'Te llamamos')]")
            time.sleep(1)
            self.fill("//input[contains(@name, 'phone')]", self.data['phone'])
            self.click("//button[contains(text(), 'Te llamamos')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
             self.log(f'Error: {e}', status='ERROR')

class SanitasService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Sanitas"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.sanitas.es/'

    def run(self):
        try:
            self.browser.set_page_load_timeout(30)
            if not self.navigate(): return
        except: return
        self.accept_cookies("//button[contains(text(), 'Aceptar')]")
        try:
            self.click("//*[contains(text(), 'Te llamamos') or contains(@class, 'phone')]")
            time.sleep(2)
            self.fill("//input[contains(@name, 'tlf') or contains(@name, 'phone')]", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme') or contains(text(), 'Enviar')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')

class AdeslasService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Adeslas"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.segurcaixaadeslas.es/'

    def run(self):
        try:
            self.browser.set_page_load_timeout(30)
            if not self.navigate(): return
        except: return
        self.accept_cookies("//button[contains(text(), 'Aceptar')]")
        try:
            self.fill("//input[contains(@name, 'phone') or contains(@id, 'phone')]", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme') or contains(text(), 'Enviar')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')

class AuraSegurosService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Aura Seguros"
        self.types = [ServiceType.CALL]
        self.url = 'https://www.auraseguros.com/'

    def run(self):
        try:
            self.browser.set_page_load_timeout(30)
            if not self.navigate(): return
        except: return
        self.accept_cookies("//button[contains(text(), 'Aceptar')]")
        try:
            self.fill("//input[contains(@name, 'phone') or contains(@id, 'phone')]", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme') or contains(text(), 'Enviar')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')
