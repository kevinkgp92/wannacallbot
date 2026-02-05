import time
from services.base_service import BaseService, ServiceType
from selenium.webdriver.common.by import By

class IdealistaService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Idealista (Inmobiliaria)"
        self.url = "https://www.idealista.com/" # Simplified placeholder
        self.types = [ServiceType.CALL, ServiceType.NIGHT, ServiceType.ESTATE]

    def run(self):
        print(f"  [Idealista] Simulando solicitud de contacto para: {self.data['phone']}")
        # En una implementación real, navegaríamos a un anuncio y rellenaríamos el contacto
        time.sleep(2)
        self.status = 'WARN' # Marked as WARN because it's a seed implementation

class FotocasaService(BaseService):
    def __init__(self, browser, user_data):
        super().__init__(browser, user_data)
        self.name = "Fotocasa (Inmobiliaria)"
        self.url = "https://www.fotocasa.es/"
        self.types = [ServiceType.CALL, ServiceType.ESTATE, ServiceType.AD]

    def run(self):
        print(f"  [Fotocasa] Simulando lead comercial para: {self.data['phone']}")
        time.sleep(2)
        self.status = 'WARN'
