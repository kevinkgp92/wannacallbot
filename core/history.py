import json
import os

import sys

class HistoryManager:
    def __init__(self, filename="history.json"):
        # Determine base path (exe dir or script dir)
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.getcwd()
            
        self.filename = os.path.join(base_path, filename)
        self.history = self._load()
        print(f"🛡️ SEGURIDAD: Sistema Anti-Duplicados ACTIVO")
        print(f"📁 RUTA HISTORIAL: {self.filename}")
        
        if "Temp" in self.filename or "AppData" in self.filename:
            print(f"🔥🔥🔥 AVISO IMPORTANTE 🔥🔥🔥")
            print(f"Parece que estás ejecutando el bot desde dentro de un ZIP o en una carpeta Temporal.")
            print(f"SI NO LO EXTRAES, PERDERÁS EL HISTORIAL AL CERRAR.")
            print(f"Solución: Mueve el .exe al Escritorio o Descargas y ejecútalo desde ahí.")
            print(f"🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥")

        print(f"🛡️ NÚMEROS PROTEGIDOS: {len(self.history)}")

    def _normalize(self, phone):
        """Standardize phone to just digits"""
        if not phone: return ""
        return "".join(c for c in str(phone) if c.isdigit())

    def _load(self):
        if not os.path.exists(self.filename):
            print(f"🛡️ INFO: Creando nuevo archivo de historial.")
            return {}
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"[History] Error loading: {e}")
            return {}

    def _save(self):
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.history, f, indent=4)
        except Exception as e:
            print(f"[History] Error saving: {e}")

    def is_registered(self, phone, service_name):
        self.history = self._load() # Force reload to get latest updates from other threads
        
        phone = self._normalize(phone)
        if not phone: return False
        
        # History structure: { "PHONE": ["ServiceA", "ServiceB"] }
        if phone not in self.history:
            return False
        return service_name in self.history[phone]

    def add_record(self, phone, service_name):
        self.history = self._load() # Force reload before modifying
        
        phone = self._normalize(phone)
        if not phone: return
        
        if phone not in self.history:
            self.history[phone] = []
        
        if service_name not in self.history[phone]:
            self.history[phone].append(service_name)
            self._save()
