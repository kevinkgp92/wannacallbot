from core.browser import BrowserManager
from selenium.webdriver.common.by import By
import time
import sys

# Force utf-8 output
sys.stdout.reconfigure(encoding='utf-8')

def inspect_page(driver, name, url):
    print(f"\n--- INSPECTING {name} ({url}) ---")
    try:
        driver.get(url)
        time.sleep(5) # Wait for load
        
        # Accept cookies
        try:
             cookies = driver.find_elements(By.XPATH, "//button[contains(text(), 'Aceptar') or contains(text(), 'Accept') or contains(@id, 'cookie') or contains(@class, 'cookie')]")
             if cookies:
                 print(f"Found {len(cookies)} potential cookie buttons. Clicking first visible...")
                 for c in cookies:
                     if c.is_displayed():
                         c.click()
                         break
             time.sleep(2)
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
                    if t not in ['hidden', 'submit']:
                        print(f"  - Input: Type='{t}' Name='{n}' Id='{id_}' Placeholder='{p}'")
                except: pass

        # Dump Buttons
        print("BUTTONS FOUND:")
        buttons = driver.find_elements(By.XPATH, "//button | //a[contains(@class, 'btn') or contains(@class, 'button')] | //input[@type='submit']")
        for b in buttons:
            if b.is_displayed():
                try:
                    t = b.text.strip()
                    val = b.get_attribute("value")
                    if t:
                        if len(t) < 50: print(f"  - Button Text: '{t}'")
                    elif val:
                         print(f"  - Button Value: '{val}'")
                except: pass
        
        # Look specifically for "Te llamamos" triggers
        print("TRIGGERS FOUND:")
        triggers = driver.find_elements(By.XPATH, "//*[contains(text(), 'llamamos') or contains(text(), 'Llamadme') or contains(text(), 'contactar')]")
        for t in triggers:
            if t.is_displayed() and t.tag_name in ['a', 'button', 'span', 'div']:
                 print(f"  - Trigger: Tag='{t.tag_name}' Text='{t.text.strip()}'")

    except Exception as e:
        print(f"Error inspecting {name}: {e}")

mgr = BrowserManager(headless=False)
try:
    driver = mgr.get_driver()
    
    # Energy
    inspect_page(driver, "Endesa", "https://www.endesa.com/es")
    inspect_page(driver, "Naturgy", "https://www.naturgy.es/")
    inspect_page(driver, "Iberdrola", "https://www.iberdrola.es/")
    
    # Insurance
    inspect_page(driver, "Mutua", "https://www.mutua.es/")
    inspect_page(driver, "LineaDirecta", "https://www.lineadirecta.com/")
    
finally:
    mgr.close()
