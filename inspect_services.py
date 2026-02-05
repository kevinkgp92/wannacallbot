import time
from core.browser import BrowserManager
from selenium.webdriver.common.by import By

def inspect_url(url, name):
    print(f"\n--- INSPECTING {name} : {url} ---")
    manager = BrowserManager(headless=True)
    driver = manager.get_driver()
    try:
        driver.get(url)
        time.sleep(8) # Longer wait
        
        # Check for cookies first
        try:
            cookies = driver.find_elements(By.XPATH, "//*[contains(text(), 'Accept') or contains(text(), 'Aceptar') or contains(@id, 'onetrust-accept')]")
            if cookies:
                print(f"Found cookie button candidates: {[c.get_attribute('id') for c in cookies]}")
        except: pass

        # Inputs
        inputs = driver.find_elements(By.TAG_NAME, "input")
        print(f"Found {len(inputs)} inputs:")
        for i in inputs[:15]: # Limit output
            try:
                print(f"  Input: id='{i.get_attribute('id')}', name='{i.get_attribute('name')}', placeholder='{i.get_attribute('placeholder')}'")
            except: pass
            
        # Buttons (looking for submit/call me)
        buttons = driver.find_elements(By.TAG_NAME, "button")
        print(f"Found {len(buttons)} buttons:")
        for b in buttons[:15]:
            try:
                print(f"  Button: text='{b.text[:30]}', id='{b.get_attribute('id')}'")
            except: pass
            
        # Iframes (Ford/Others)
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        if iframes:
            print(f"Found {len(iframes)} iframes. Taking a peek...")
            for frame in iframes:
                try:
                    print(f"  Iframe src: {frame.get_attribute('src')}")
                except: pass

    except Exception as e:
        print(f"Error inspecting {name}: {e}")
    finally:
        manager.close()
    print("--------------------------------------------------")

if __name__ == "__main__":
    inspect_url("https://www.racctelplus.com/", "Racctel+")
    inspect_url("https://www.ford.es/", "Ford")
    inspect_url("https://www.vodafone.es/c/particulares/es/", "Vodafone")
    inspect_url("https://www.euskaltel.com/", "Euskaltel")
    inspect_url("https://www.pelayo.com/seguros-coche", "Pelayo")
