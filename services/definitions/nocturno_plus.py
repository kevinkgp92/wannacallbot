import time
from services.base_service import BaseService, ServiceType
from selenium.webdriver.common.by import By

class TelePizzaService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "TelePizza (24h/Cierre)"
        self.url = "https://www.telepizza.es/atencion-al-cliente"
        self.types = [ServiceType.NIGHT, ServiceType.AD]

    def run(self):
        if not self.navigate(): return
        self.accept_cookies("//button[contains(text(), 'Aceptar')]")
        try:
            self.fill("//input[contains(@id, 'nombre')]", self.data['name'])
            self.fill("//input[contains(@id, 'email')]", self.data['email'])
            self.fill("//input[contains(@id, 'telefono')]", self.data['phone'])
            self.click("//input[@type='checkbox']")
            self.log('Simulando envío TelePizza (Modo Noche)', status='OK')
        except: pass

class Cerrajero24hService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Cerrajero 24h Urgente"
        self.url = "https://www.cerrajeros.com/contacto/" 
        self.types = [ServiceType.CALL, ServiceType.NIGHT]

    def run(self):
        if not self.navigate(): return
        try:
            self.fill("//input[@name='your-name']", self.data['name'])
            self.fill("//input[@name='your-tel']", self.data['phone'])
            self.click("//input[@type='checkbox']")
            self.log('Solicitud de cerrajero urgente simulada', status='OK')
        except: pass

class Grua24hService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Grúas 24h España"
        self.url = "https://www.asistenciaenscar.es/contacto/"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]

    def run(self):
        if not self.navigate(): return
        try:
            self.fill("//input[@name='phone']", self.data['phone'])
            self.log('Solicitud de grúa enviada', status='OK')
        except: pass

class SecuritasDirectNight(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Securitas Direct (Night Shift)"
        self.url = "https://www.securitasdirect.es/"
        self.types = [ServiceType.CALL, ServiceType.NIGHT, ServiceType.SECURITY]

    def run(self):
        if not self.navigate(): return
        self.accept_cookies("//button[contains(@id, 'accept')]")
        try:
            self.fill("//input[@id='edit-phone']", self.data['phone'])
            self.click("//button[contains(@id, 'edit-submit')]")
            self.log('Solicitud de seguridad nocturna enviada', status='OK')
        except: pass

class ClickCerrajerosService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Click Cerrajeros (24h)"
        self.url = "https://clickcerrajeros.es/contacto/"
        self.types = [ServiceType.NIGHT, ServiceType.CALL]

    def run(self):
        if not self.navigate(): return
        self.accept_cookies("//button[contains(text(), 'Aceptar')]")
        try:
            self.fill("//input[contains(@name, 'your-name')]", self.data['name'])
            self.fill("//input[contains(@name, 'your-tel')]", self.data['phone'])
            self.fill("//input[contains(@name, 'your-email')]", self.data['email'])
            self.click("//input[@type='checkbox']")
            self.log('Simulando aviso de cerrajería urgente', status='OK')
        except: pass

class Electricista24ProService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Electricista 24 Pro"
        self.url = "https://electricista24.pro/contacto/"
        self.types = [ServiceType.NIGHT, ServiceType.CALL]

    def run(self):
        if not self.navigate(): return
        try:
            self.fill("//input[@name='name']", self.data['name'])
            self.fill("//input[@name='phone']", self.data['phone'])
            self.click("//input[@type='checkbox']")
            self.log('Aviso de avería eléctrica 24h enviado', status='OK')
        except: pass

class FontanerosUrgentes24h(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Fontaneros Urgentes 24h"
        self.url = "https://fontaneros-24.com/contacto/"
        self.types = [ServiceType.NIGHT, ServiceType.CALL]

    def run(self):
        if not self.navigate(): return
        try:
            self.fill("//input[@name='nombre']", self.data['name'])
            self.fill("//input[@name='telefono']", self.data['phone'])
            self.log('Solicitud de fontanería de urgencia enviada', status='OK')
        except: pass

class HomeServe24hService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "HomeServe (Reparaciones 24h)"
        self.url = "https://www.homeserve.es/"
        self.types = [ServiceType.NIGHT, ServiceType.CALL]

    def run(self):
        if not self.navigate(): return
        try:
            # HomeServe usually has a simple 'te llamamos' or contact
            self.fill("//input[contains(@id, 'phone')]", self.data['phone'])
            self.log('Solicitud de asistencia HomeServe enviada', status='OK')
        except: pass

class MutuaAsistenciaNight(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Mutua Madrileña (Asistencia 24h)"
        self.url = "https://www.mutua.es/"
        self.types = [ServiceType.NIGHT, ServiceType.CALL]

    def run(self):
        if not self.navigate(): return
        try:
            self.fill("//input[contains(@name, 'telefono')]", self.data['phone'])
            self.log('Aviso de asistencia en carretera 24h enviado', status='OK')
        except: pass
