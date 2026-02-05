from services.base_service import BaseService, ServiceType
import time

class EuroinnovaService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Euroinnova"
        self.types = [ServiceType.CALL, ServiceType.PHYSICAL, ServiceType.NIGHT]
        self.url = 'https://www.euroinnova.com/'

    def run(self):
        try:
             self.browser.set_page_load_timeout(60) # Increased for Euroinnova
             if not self.navigate(): return
        except:
             self.log("Skipeado (Timeout)", status='WARN')
             return

        self.accept_cookies("//button[contains(@id, 'cookies') or contains(text(), 'Aceptar') or contains(text(), 'Accept')]")
        
        try:
            self.fill('//*[@id="name"]', self.data['name'])
            self.fill('//*[@id="mail"]', self.data['email'])
            self.fill('//*[@id="tel"]', self.data['phone'])
            try:
                # Try to select the first option in the study level dropdown if it exists
                self.click("//select[contains(@id, 'estudios')]/option[2]")
            except: pass 
            self.click("//input[contains(@id, 'privacidad') or contains(@id, 'check')]")
            self.click("//button[contains(@id, 'enviar') or contains(text(), 'Enviar')]")
            self.human_delay(2, 4)
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')

class RacctelPlusService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Racctel+"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.racctelplus.com/'

    def run(self):
        try:
            self.browser.set_page_load_timeout(20)
            if not self.navigate(): return
        except:
            self.log("Skipeado (Timeout)", status='WARN')
            return
            
        self.accept_cookies("//button[contains(@id, 'onetrust-accept')]")
        
        try:
            self.fill("//input[contains(@id, 'phone') or contains(@name, 'phone')]", self.data['phone'])
            self.click("//button[contains(text(), 'TRUCA') or contains(text(), 'Gratis')]")
            self.human_delay(2, 3)
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')

class FordService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Ford"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.ford.es/'

    def run(self):
        try:
            self.browser.set_page_load_timeout(20)
            if not self.navigate(): return
        except:
             self.log("Skipeado (Timeout)", status='WARN')
             return
             
        self.accept_cookies("//button[contains(@id, 'onetrust-accept')]")
        
        try:
            self.click("//*[contains(text(), 'Ponte en contacto') or contains(text(), 'Solicitar') or contains(text(), 'Prueba')]")
            time.sleep(2)
            try:
                self.fill("//input[@name='MobilePhone']", self.data['phone'])
            except:
                self.fill("//input[contains(@placeholder, 'Teléfono') or @type='tel']", self.data['phone'])
            self.click("//button[contains(text(), 'Enviar') or contains(text(), 'Solicitar')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')

class VodafoneService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Vodafone"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.vodafone.es/c/particulares/es/'

    def run(self):
        try:
            self.browser.set_page_load_timeout(20)
            if not self.navigate(): return
        except:
            self.log("Skipeado (Timeout)", status='WARN')
            return

        self.accept_cookies("//button[contains(@id, 'onetrust-accept')]")
        
        try:
            self.click("//*[contains(text(), 'Te llamamos') or contains(text(), 'Llamadme')]")
            time.sleep(2)
            self.fill("//input[@name='phone']", self.data['phone'])
            try:
                self.click("//label[contains(text(), 'privacidad')]") 
            except:
                self.click("//input[@type='checkbox']")
            self.click("//button[contains(text(), 'Llamadme')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')

class EuskaltelService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Euskaltel"
        self.types = [ServiceType.CALL]
        self.url = 'https://www.euskaltel.com/'

    def run(self):
        try:
            self.browser.set_page_load_timeout(20)
            if not self.navigate(): return
        except:
            self.log("Skipeado (Timeout)", status='WARN')
            return
            
        self.accept_cookies("//button[contains(@id, 'onetrust-accept')]")
        
        try:
            self.fill("//input[@id='phone']", self.data['phone'])
            self.click("//button[contains(text(), 'GRATIS')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')

class PelayoService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Pelayo"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.pelayo.com/'

    def run(self):
        try:
            self.browser.set_page_load_timeout(60) # Increased for Pelayo
            if not self.navigate(): return
        except:
             self.log("Skipeado (Timeout)", status='WARN')
             return
        self.accept_cookies("//button[contains(text(), 'Aceptar') or contains(@id, 'cookies')]")
        try:
            try:
                self.click("//*[contains(text(), 'Te llamamos')]")
                time.sleep(1)
            except: pass
            self.fill("//input[contains(@id, 'phone')]", self.data['phone'])
            try:
                self.click("//input[@type='checkbox']")
            except: pass
            self.click("//button[contains(text(), 'Llamadme')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')

class MapfreService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Mapfre"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.mapfre.es/boi/inicio.do?origen=autos_portalmapfre&destino=sgc_new&producto=autos'

    def run(self):
        if not self.navigate(): return
        self.accept_cookies('//*[@id="onetrust-accept-btn-handler"]')
        
        try:
            self.fill('//*[@id="nombre"]', self.data['name'])
            self.fill('//*[@id="primer_apellido"]', self.data['surname'])
            self.fill('//*[@id="codigo_postal"]', self.data['zipcode'])
            self.fill('//*[@id="tlfn"]', self.data['phone'])
            self.click('//*[@id="marca_robinson"]')
            self.click('//*[@id="politicaprivacidad"]')
            self.click('/html/body/div[1]/main/div/div/div[2]/form/fieldset/div[10]/input')
            time.sleep(3)
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')

class GenesisService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Genesis"
        self.types = [ServiceType.CALL, ServiceType.NIGHT] 
        self.url = 'https://www.genesis.es/modal/c2c'

    def run(self):
        try:
            self.browser.set_page_load_timeout(60) # Increased for Genesis
            if not self.navigate(): return
        except:
             self.log("Skipeado (Timeout)", status='WARN')
             return
        self.accept_cookies('//*[@id="onetrust-accept-btn-handler"]')
        try:
             self.fill('//*[@id="edit-phone"]', self.data['phone'])
             self.fill('//*[@id="edit-phone-confirmation"]', self.data['phone'])
             try:
                 self.click('//*[@id="edit-actions-submit"]')
             except:
                 self.click("//button[contains(text(), 'Llamadme')]")
             time.sleep(3)
             self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')


# Jazztel and Yoigo moved to more_telco.py to avoid duplicates

class UnirService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "UNIR"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.unir.net/'

    def run(self):
        try:
            self.browser.set_page_load_timeout(30)
            if not self.navigate(): return
        except: return
        
        self.accept_cookies("//button[contains(@id, 'onetrust-accept')]")
        
        try:
            # Usually strict form on landing or header
            self.click("//*[contains(text(), 'Solicita información') or contains(text(), 'Te llamamos')]")
            time.sleep(1)
            
            self.fill("//input[contains(@name, 'Nombre') or contains(@id, 'name')]", self.data['name'])
            self.fill("//input[contains(@name, 'Apellido') or contains(@id, 'lastname')]", self.data['surname'])
            self.fill("//input[contains(@name, 'Email') or contains(@id, 'email')]", self.data['email'])
            self.fill("//input[contains(@name, 'Movil') or contains(@name, 'Phone')]", self.data['phone'])
            
            try:
                self.click("//input[@type='checkbox']")
            except: pass
            
            self.click("//button[contains(text(), 'Enviar') or contains(text(), 'Solicitar')]")
            self.log('Solicitud enviada', status='OK')
        except Exception as e:
            self.log(f'Error: {e}', status='ERROR')

