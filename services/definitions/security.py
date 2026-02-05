from services.base_service import BaseService, ServiceType
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SecuritasService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Securitas Direct"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.securitasdirect.es/'

    def run(self):
        try:
            self.browser.set_page_load_timeout(20)
            if not self.navigate(): return
        except:
            self.log("Skipeado (Timeout)", status='WARN')
            return

        self.accept_cookies("//button[contains(@id, 'AllowAll') or contains(text(), 'Aceptar') or contains(@id, 'cookie')]")
        
        try:
            self.fill("//input[contains(@id, 'telefono') or contains(@name, 'phone')]", self.data['phone'])
            self.click("//button[contains(@id, 'edit-submit') or contains(text(), 'Llamadme')]")
            self.human_delay(1, 2)
            if self.browser.current_url == 'https://www.securitasdirect.es/error-envio':
                self.log('Skipeado (Limite Excedido)', status='WARN')
            else:
                self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')

class ProsegurService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Prosegur"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.prosegur.es/'

    def run(self):
        try:
            self.browser.set_page_load_timeout(20)
            if not self.navigate(): return
        except:
             self.log("Skipeado (Timeout)", status='WARN')
             return
        
        self.accept_cookies("//button[contains(@id, 'agree') or contains(text(), 'Aceptar')]")
        
        try:
            # Prosegur has different forms depending on landing
            self.fill("//input[contains(@name, 'phone') or contains(@id, 'telef') or @type='tel']", self.data['phone'])
            
            # Button is 'Contratar' or similar
            self.click("//button[contains(text(), 'Contratar') or contains(text(), 'Llamadme') or contains(text(), 'Te llamamos')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')

class MasMovilAlarmasService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "MasMovil Alarmas"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://masmovilalarmas.es/'

    def run(self):
        try:
            self.browser.set_page_load_timeout(20)
            if not self.navigate(): return
        except:
             self.log("Skipeado (Timeout)", status='WARN')
             return

        self.accept_cookies('//*[@id="onetrust-accept-btn-handler"]')
        
        try:
            # Try multiple selectors for the phone field
            phone_selectors = [
                 "//*[starts-with(@id, 'BysidePhoneBySideData_')]",
                 "//input[@name='phone']",
                 "//input[@type='tel']",
                 "//input[contains(@id, 'phone')]",
                 "//input[contains(@class, 'phone')]"
            ]
            
            found = False
            for selector in phone_selectors:
                 try:
                     if self.browser.find_elements(By.XPATH, selector):
                         self.fill(selector, self.data['phone'])
                         found = True
                         break
                 except: continue
                 
            if found:
                 self.click("//*[starts-with(@id, 'BysideCallBtnBySideData_') or contains(text(), 'Llamadme') or contains(text(), 'Solicitar')]")
                 self.log('Solicitud enviada', status='OK')
            else:
                 self.log('No se encontro el formulario', status='ERROR')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')

class ADTService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "ADT"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.adt.com.es/'

    def run(self):
        try:
            self.browser.set_page_load_timeout(30)
            if not self.navigate(): return
        except: return
        
        self.accept_cookies("//button[contains(@id, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')]")
        
        try:
            # Sticky header "Te llamamos gratis" or similar
            self.click("//*[contains(text(), 'Te llamamos') or contains(@class, 'cta')]")
            time.sleep(1)
            
            self.fill("//input[@name='phone' or contains(@id, 'phone')]", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme') or contains(text(), 'Enviar')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')

class SectorAlarmService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Sector Alarm"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.sectoralarm.es/'

    def run(self):
        try:
            self.browser.set_page_load_timeout(30)
            if not self.navigate(): return
        except: return

        self.accept_cookies("//button[contains(@id, 'onetrust-accept')]")

        try:
            # Often has a clear form in hero or "Calcula tu oferta"
            self.fill("//input[@name='phone' or @type='tel']", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme') or contains(text(), 'Enviar') or contains(text(), 'Calcular')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')

class SegurmaService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Segurma"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://segurma.com/'

    def run(self):
        try:
             self.browser.set_page_load_timeout(30)
             if not self.navigate(): return
        except: return
        
        self.accept_cookies("//button[contains(text(), 'Aceptar') or contains(@id, 'cookie')]")
        try:
            # Look for contact form
            self.fill("//input[@type='tel' or contains(@name, 'phone')]", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme') or contains(text(), 'Enviar') or contains(text(), 'Informarme')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
             self.log(f'Error: {e}', status='ERROR')
