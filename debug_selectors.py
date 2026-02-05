from core.browser import BrowserManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys

# Force utf-8 output
sys.stdout.reconfigure(encoding='utf-8')

def inspect_page(driver, name, url):
    print(f"\n--- INSPECTING {name} ({url}) ---")
    try:
        driver.get(url)
        time.sleep(5) # Wait for load
        
        # Accept cookies attempts
        try:
             cookies = driver.find_elements(By.XPATH, "//button[contains(text(), 'Aceptar') or contains(text(), 'Accept') or contains(@id, 'cookie')]")
             if cookies:
                 print(f"Found {len(cookies)} potential cookie buttons. Clicking first visible...")
                 for c in cookies:
                     if c.is_displayed():
                         c.click()
                         break
             time.sleep(1)
        except: pass

        # Dump Inputs
        print("INPUTS FOUND:")
        inputs = driver.find_elements(By.TAG_NAME, "input")
        for i in inputs:
            if i.is_displayed():
                try:
                    p = i.get_attribute("placeholder")
                    n = i.get_attribute("name")
                    id_ = i.get_attribute("id")
                    t = i.get_attribute("type")
                    if t != 'hidden':
                        print(f"  - Input: Type='{t}' Name='{n}' Id='{id_}' Placeholder='{p}'")
                except: pass

        # Dump Buttons with text
        print("BUTTONS FOUND:")
        buttons = driver.find_elements(By.XPATH, "//button | //a[contains(@class, 'btn') or contains(@class, 'button')] | //input[@type='submit']")
        for b in buttons:
            if b.is_displayed():
                try:
                    t = b.text.strip()
                    val = b.get_attribute("value")
                    if t:
                        print(f"  - Button Text: '{t}'")
                    elif val:
                        print(f"  - Button Value: '{val}'")
                except: pass
                
    except Exception as e:
        print(f"Error inspecting {name}: {e}")

mgr = BrowserManager(headless=False)
try:
    driver = mgr.get_driver()
    
    # Check the failing ones
    inspect_page(driver, "Prosegur", "https://www.prosegur.es/")
    inspect_page(driver, "Racctel+", "https://www.racctelplus.com/")
    inspect_page(driver, "Ford", "https://www.ford.es/")
    inspect_page(driver, "Vodafone", "https://www.vodafone.es/c/particulares/es/")
    inspect_page(driver, "Euskaltel", "https://www.euskaltel.com/")
    inspect_page(driver, "Pelayo", "https://www.pelayo.com/")
    
finally:
    mgr.close()
