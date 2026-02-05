from services.base_service import BaseService, ServiceType
import time

class LegalitasService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Legalitas"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.legalitas.com/'

    def run(self):
        if not self.navigate(): return
        self.accept_cookies("//button[contains(text(), 'Aceptar')]")
        try:
            self.fill("//input[@type='tel' or contains(@name, 'phone')]", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme') or contains(text(), 'Te llamamos')]")
            self.log('Solicitud enviada (Legalitas)', status='OK')
        except: pass

class MutuaService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Mutua Madrileña"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.mutua.es/'

    def run(self):
        if not self.navigate(): return
        self.accept_cookies("//button[contains(text(), 'Aceptar')]")
        try:
            self.fill("//input[contains(@name, 'telefono')]", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme')]")
            self.log('Solicitud enviada (Mutua)', status='OK')
        except: pass

class SanitasService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Sanitas"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.sanitas.es/'

    def run(self):
        if not self.navigate(): return
        self.accept_cookies("//button[contains(text(), 'Aceptar')]")
        try:
            self.fill("//input[@type='tel']", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme') or contains(text(), 'Te llamamos')]")
            self.log('Solicitud enviada (Sanitas)', status='OK')
        except: pass

class AdeslasService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Adeslas"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.segurcaixaadeslas.es/'

    def run(self):
        if not self.navigate(): return
        self.accept_cookies("//button[contains(text(), 'Aceptar')]")
        try:
            self.fill("//input[contains(@name, 'phone')]", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme')]")
            self.log('Solicitud enviada (Adeslas)', status='OK')
        except: pass

class LineaDirectaService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Linea Directa"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.lineadirecta.com/'

    def run(self):
        if not self.navigate(): return
        self.accept_cookies("//button[contains(text(), 'Aceptar')]")
        try:
            self.fill("//input[contains(@name, 'telefono')]", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme')]")
            self.log('Solicitud enviada (Linea Directa)', status='OK')
        except: pass

class IberdrolaService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Iberdrola"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.iberdrola.es/'

    def run(self):
        if not self.navigate(): return
        self.accept_cookies("//button[contains(@id, 'accept')]")
        try:
            self.fill("//input[@type='tel']", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme')]")
            self.log('Solicitud enviada (Iberdrola)', status='OK')
        except: pass

class NaturgyService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Naturgy"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.naturgy.es/'

    def run(self):
        if not self.navigate(): return
        self.accept_cookies("//button[contains(text(), 'Aceptar')]")
        try:
            self.fill("//input[contains(@name, 'phone')]", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme')]")
            self.log('Solicitud enviada (Naturgy)', status='OK')
        except: pass

class PelayoService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Pelayo"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.pelayo.com/'

    def run(self):
        if not self.navigate(): return
        self.accept_cookies("//button[contains(text(), 'Aceptar')]")
        try:
            self.fill("//input[contains(@name, 'phone')]", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme')]")
            self.log('Solicitud enviada (Pelayo)', status='OK')
        except: pass

class LowiService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Lowi"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.lowi.es/'

    def run(self):
        if not self.navigate(): return
        self.accept_cookies("//button[contains(text(), 'Aceptar')]")
        try:
            self.fill("//input[@type='tel']", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme')]")
            self.log('Solicitud enviada (Lowi)', status='OK')
        except: pass

class AxaService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Axa"
        self.types = [ServiceType.CALL, ServiceType.NIGHT]
        self.url = 'https://www.axa.es/'

    def run(self):
        if not self.navigate(): return
        self.accept_cookies("//button[contains(text(), 'Aceptar')]")
        try:
            self.fill("//input[contains(@name, 'phone')]", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme')]")
            self.log('Solicitud enviada (Axa)', status='OK')
        except: pass
