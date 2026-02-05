import sys
import os

# Add the project root to sys.path
sys.path.append(os.getcwd())

from services.manager import ServiceManager

def verify_v3_expansion():
    user_data = {
        'name': 'Test',
        'surname': 'User',
        'email': 'test@example.com',
        'phone': '600000000',
        'zipcode': '28001'
    }
    
    print("Initializing ServiceManager to check discovery...")
    # force_chrome=True if you want to avoid browser check issues in some environments, 
    # but here we just want to check the list of services.
    manager = ServiceManager(user_data)
    
    new_services_v3 = [
        "Direct Seguros", "Reale", "Gana Energía", "Carglass", 
        "HomeServe", "MasterD", "IMF", "Occident"
    ]
    
    print(f"\nTotal services registered: {len(manager.services)}")
    
    found_v3 = [s for s in manager.services if s.name in new_services_v3]
    
    print("\nVerifying Expansion V3 services:")
    for name in new_services_v3:
        service = next((s for s in manager.services if s.name == name), None)
        if service:
            print(f"[OK] Found service: {name} ({service.url})")
        else:
            print(f"[MISSING] {name}")
    
    if len(found_v3) == len(new_services_v3):
        print("\n[SUCCESS] All 8 new services from Expansion V3 are correctly registered.")
    else:
        print(f"\n[WARNING] Only {len(found_v3)}/8 services were found.")

    # Close browser opened by manager
    manager.browser_manager.close()

if __name__ == "__main__":
    verify_v3_expansion()
