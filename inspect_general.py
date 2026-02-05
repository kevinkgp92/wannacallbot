import time
from core.browser import BrowserManager
from selenium.webdriver.common.by import By

def inspect_url(url, name):
    print(f"\n--- INSPECTING {name} : {url} ---")
    manager = BrowserManager(headless=True)
    driver = manager.get_driver()
    try:
        driver.set_page_load_timeout(30)
        driver.get(url)
        time.sleep(5) 
        
        # Check Cookies
        try:
             cookies = driver.find_elements(By.XPATH, "//*[contains(text(), 'Accept') or contains(text(), 'Aceptar') or contains(@id, 'onetrust-accept')]")
             if cookies:
                 print(f"Found cookie keys: {[c.get_attribute('id') for c in cookies]}")
        except: pass

        # Look for inputs
        inputs = driver.find_elements(By.TAG_NAME, "input")
        print(f"Found {len(inputs)} inputs:")
        for i in inputs[:10]:
            try:
                print(f"  Input: id='{i.get_attribute('id')}', name='{i.get_attribute('name')}'")
            except: pass

    except Exception as e:
        print(f"Error inspecting {name}: {e}")
    finally:
        manager.close()
    print("--------------------------------------------------")

if __name__ == "__main__":
    inspect_url("https://www.mapfre.es/boi/inicio.do?origen=autos_portalmapfre&destino=sgc_new&producto=autos", "Mapfre")
    inspect_url("https://www.genesis.es/modal/c2c", "Genesis")
