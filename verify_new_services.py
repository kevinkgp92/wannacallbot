import sys
import os

# Add the project root to sys.path
sys.path.append(os.getcwd())

from services.manager import ServiceManager

def test_new_services():
    user_data = {
        'name': 'Test',
        'surname': 'User',
        'email': 'test@example.com',
        'phone': '600000000',
        'zipcode': '28001'
    }
    
    manager = ServiceManager(user_data)
    
    new_service_names = [
        "Legalitas", "Arriaga Asociados", "Solar360", "Otovo", "Alterna",
        "Sanitas", "Adeslas", "Aura Seguros", "U.Isabel I", "UAX"
    ]
    
    print(f"Total services registered: {len(manager.services)}")
    
    found_services = [s for s in manager.services if s.name in new_service_names]
    
    print("\nVerifying new services:")
    for s in found_services:
        print(f"[OK] Found service: {s.name} ({s.url})")
    
    if len(found_services) < len(new_service_names):
        print("\n[WARNING] Some services were not found in the manager!")
        existing_names = [s.name for s in manager.services]
        for name in new_service_names:
            if name not in existing_names:
                print(f"[MISSING] {name}")
    else:
        print("\n[SUCCESS] All new services are correctly registered.")

    # Close browser opened by manager
    manager.browser_manager.close()

if __name__ == "__main__":
    test_new_services()
