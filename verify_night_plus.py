import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from services.manager import discover_services, ServiceType

def verify():
    classes = discover_services()
    night_services = [cls for cls in classes if any(ServiceType.NIGHT == t for t in getattr(cls(None, {}), 'types', []))]
    
    print(f"\n--- VERIFICACIÓN DE MODO NOCTURNO ---")
    print(f"Total servicios descubiertos: {len(classes)}")
    print(f"Total servicios NOCTURNOS: {len(night_services)}")
    print("\nLista de servicios Nocturnos:")
    for cls in night_services:
        print(f" - {cls.__name__}")

if __name__ == "__main__":
    verify()
