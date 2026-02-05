from services.base_service import BaseService, ServiceType
import time
from selenium.webdriver.common.by import By

class DirectSegurosService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Direct Seguros"
        self.types = [ServiceType.INSURANCE, ServiceType.CALL]
        self.url = "https://www.directseguros.es/te-llamamos.html"

    def run(self):
        if not self.navigate(): return
        self.accept_cookies("//button[contains(@id, 'onetrust-accept')]")
        try:
            self.fill("//input[@id='telefono']", self.data['phone'])
            self.click("//input[@id='privacidad']")
            self.click("//button[contains(text(), 'Llamadme')]")
            self.log("Solicitud enviada", "OK")
        except Exception as e:
            self.log(f"Error: {e}", "ERROR")

class RealeService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Reale"
        self.types = [ServiceType.INSURANCE, ServiceType.CALL]
        self.url = "https://www.reale.es/te-llamamos"

    def run(self):
        if not self.navigate(): return
        self.accept_cookies("//button[contains(text(), 'Aceptar')]")
        try:
            self.fill("//input[contains(@name, 'phone')]", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme')]")
            self.log("Solicitud enviada", "OK")
        except Exception as e:
            self.log(f"Error: {e}", "ERROR")

class GanaEnergiaService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Gana Energía"
        self.types = [ServiceType.ENERGY, ServiceType.CALL]
        self.url = "https://ganaenergia.com/contacto"

    def run(self):
        if not self.navigate(): return
        self.accept_cookies("//button[contains(text(), 'Aceptar')]")
        try:
            self.fill("//input[@name='name']", self.data['name'])
            self.fill("//input[@name='phone']", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme')]")
            self.log("Solicitud enviada", "OK")
        except Exception as e:
            self.log(f"Error: {e}", "ERROR")

class CarglassService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Carglass"
        self.types = [ServiceType.CALL]
        self.url = "https://www.carglass.es/contacto"

    def run(self):
        if not self.navigate(): return
        self.accept_cookies("//button[contains(text(), 'Aceptar')]")
        try:
            self.fill("//input[contains(@name, 'phone')]", self.data['phone'])
            self.click("//button[contains(text(), 'Llamadme')]")
            self.log("Solicitud enviada", "OK")
        except Exception as e:
            self.log(f"Error: {e}", "ERROR")

class HomeServeService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "HomeServe"
        self.types = [ServiceType.CALL]
        self.url = "https://www.homeserve.es/"

    def run(self):
        if not self.navigate(): return
        self.accept_cookies("//button[contains(text(), 'Aceptar')]")
        try:
            self.click("//*[contains(text(), 'Te llamamos')]")
            time.sleep(1)
            self.fill("//input[contains(@name, 'phone')]", self.data['phone'])
            self.click("//button[contains(text(), 'Enviar')]")
            self.log("Solicitud enviada", "OK")
        except Exception as e:
            self.log(f"Error: {e}", "ERROR")

class MasterDService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "MasterD"
        self.types = [ServiceType.CALL]
        self.url = "https://www.masterd.es/"

    def run(self):
        if not self.navigate(): return
        self.accept_cookies("//button[contains(text(), 'Aceptar')]")
        try:
            self.fill("//input[contains(@name, 'nombre')]", self.data['name'])
            self.fill("//input[contains(@name, 'telefono')]", self.data['phone'])
            self.click("//button[contains(text(), 'Informarme')]")
            self.log("Solicitud enviada", "OK")
        except Exception as e:
            self.log(f"Error: {e}", "ERROR")

class IMFService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "IMF"
        self.types = [ServiceType.CALL]
        self.url = "https://www.imf-formacion.com/"

    def run(self):
        if not self.navigate(): return
        self.accept_cookies("//button[contains(text(), 'Aceptar')]")
        try:
            self.fill("//input[contains(@name, 'nombre')]", self.data['name'])
            self.fill("//input[contains(@name, 'phone')]", self.data['phone'])
            self.click("//button[contains(text(), 'Solicitar')]")
            self.log("Solicitud enviada", "OK")
        except Exception as e:
            self.log(f"Error: {e}", "ERROR")

class OccidentService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Occident"
        self.types = [ServiceType.INSURANCE, ServiceType.CALL]
        self.url = "https://www.occident.com/"

    def run(self):
        if not self.navigate(): return
        self.accept_cookies("//button[contains(text(), 'Aceptar')]")
        try:
            self.click("//*[contains(text(), 'Te llamamos')]")
            time.sleep(1)
            self.fill("//input[contains(@name, 'telefono')]", self.data['phone'])
            self.click("//button[contains(text(), 'Enviar')]")
            self.log("Solicitud enviada", "OK")
        except Exception as e:
            self.log(f"Error: {e}", "ERROR")
