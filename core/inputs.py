import re
import os
from colorama import Fore, Style
from unidecode import unidecode

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

class InputHandler:
    def __init__(self, debug=False, debug_data=None):
        self.debug = debug
        self.debug_data = debug_data or {}
        self.data = {}

    def get_user_data(self):
        if self.debug:
            print(Fore.YELLOW + "DEBUG MODE ON" + Style.RESET_ALL)
            return self._get_debug_data()
        
        return self._ask_user_data()

    def _get_debug_data(self):
        return {
            'phone': '666666666',
            'name': 'NombrePrueba',
            'surname': 'ApellidoPrueba',
            'email': 'CorreoPrueba@gmail.com',
            'address': 'Calle Falsa',
            'number': '123',
            'floor': '1',
            'city': 'Madrid',
            'province': 'Madrid',
            'zipcode': '28001'
        }

    def _ask_user_data(self):
        clear_console()
        print(Fore.MAGENTA + "=== INTRODUZCA LOS DATOS DE LA VÍCTIMA ===" + Style.RESET_ALL)
        
        # Phone
        phone = self._ask("Nº de Teléfono (empieza por 6, 7 o 9)", 
                          validator=lambda x: x.isdigit() and len(x) == 9 and x[0] in '679')
        self.data['phone'] = phone
        self._print_summary()

        # Name
        name = self._ask("Nombre", validator=lambda x: len(x) > 0)
        self.data['name'] = self._normalize(name)
        self._print_summary()

        # Surname
        surname = self._ask("Apellido", validator=lambda x: len(x) > 0)
        self.data['surname'] = self._normalize(surname)
        self._print_summary()

        # Email
        email_default = f"{self.data['name']}.{self.data['surname']}@gmail.com"
        email = self._ask(f"Email (Enter para usar {email_default})", required=False)
        self.data['email'] = email if email else email_default
        self._print_summary()

        # Physical Address (Optional)
        print(Fore.CYAN + "\n--- DATOS DE DIRECCIÓN (Opcional, para modo Contrareembolso) ---" + Style.RESET_ALL)
        
        want_address = self._ask("¿Desea introducir dirección física? (S/N)", required=True, validator=lambda x: x.lower() in ['s', 'n'])
        
        if want_address.lower() == 's':
            self.data['address'] = self._ask("Calle / Dirección", required=True)
            self.data['number'] = self._ask("Número de portal", required=True)
            self.data['floor'] = self._ask("Piso / Puerta", required=False)
            self.data['city'] = self._ask("Ciudad", required=True)
            self.data['province'] = self._ask("Provincia", required=True)
            self.data['zipcode'] = self._ask("Código Postal", validator=lambda x: x.isdigit() and len(x) == 5)
        else:
            # Fill with empty defaults
            self.data['address'] = ""
            self.data['number'] = ""
            self.data['floor'] = ""
            self.data['city'] = ""
            self.data['province'] = ""
            self.data['zipcode'] = ""
        
        clear_console()
        print(Fore.GREEN + "=== DATOS RECOPILADOS ===" + Style.RESET_ALL)
        self._print_full_summary()
        
        return self.data

    def _ask(self, prompt, validator=None, required=True):
        while True:
            val = input(Fore.YELLOW + f"{prompt}: " + Style.RESET_ALL).strip()
            if not val and not required:
                return ""
            if not val and required:
                continue
            if validator and not validator(val):
                print(Fore.RED + "Dato inválido" + Style.RESET_ALL)
                continue
            return val

    def _normalize(self, text):
        return re.sub(r'[^a-zA-Z0-9]', '', unidecode(text)).lower()

    def _print_summary(self):
        clear_console()
        self._print_full_summary()

    def _print_full_summary(self):
        for k, v in self.data.items():
            print(f"{k.capitalize()}: {Fore.WHITE}{v}{Style.RESET_ALL}")
        print("-" * 20)
