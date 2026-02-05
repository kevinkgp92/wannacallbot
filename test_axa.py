from services.manager import BrowserManager
from services.definitions.insurance_new import AxaService
import time

def test_axa():
    print("Testing Axa Service...")
    mgr = BrowserManager(headless=False)
    browser = mgr.get_driver()
    
    data = {"phone": "600000000", "name": "Test"}
    service = AxaService(browser, data)
    
    # Override URL to test
    service.url = "https://www.axa.es/seguros-coche"
    print(f"Navigating to {service.url}")
    
    try:
        service.run()
        print("Test finished.")
    except Exception as e:
        print(f"Test failed: {e}")
    finally:
        input("Press Enter to close...")
        mgr.close()

if __name__ == "__main__":
    test_axa()
