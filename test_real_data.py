import sys
from services.manager import ServiceManager

# Force utf-8
sys.stdout.reconfigure(encoding='utf-8')

user_data = {
    'phone': '658771582',
    'name': 'ivan', # Normalized usually
    'surname': 'oliva',
    'email': 'ivan.oliva@gmail.com',
    'address': '',
    'number': '',
    'floor': '',
    'city': '',
    'province': '',
    'zipcode': '28001' # Default for testing
}

from services.manager import SERVICE_CLASSES
from core.browser import BrowserManager

print("--- STARTING ISOLATED TEST WITH REAL DATA ---")

for ServiceClass in SERVICE_CLASSES:
    print(f"\nTesting {ServiceClass.__name__}...")
    mgr = BrowserManager(headless=True) # Run headless for speed/stability during test
    try:
        driver = mgr.get_driver()
        service = ServiceClass(driver, user_data)
        service.run()
    except Exception as e:
        print(f"CRASH in {ServiceClass.__name__}: {e}")
    finally:
        mgr.close()

print("--- TEST FINISHED ---")
