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
        time.sleep(4) 
        
        # Accept cookies
        try:
             cookies = driver.find_elements(By.XPATH, "//button[contains(text(), 'Aceptar') or contains(text(), 'Accept') or contains(@id, 'cookie')]")
             if cookies:
                 print(f"  > Clicking cookie button...")
                 for c in cookies:
                     if c.is_displayed():
                         c.click()
                         break
             time.sleep(1)
        except: pass

        # Dump "Te llamamos" triggers
        print("TRIGGERS FOUND:")
        triggers = driver.find_elements(By.XPATH, "//*[contains(text(), 'llamamos') or contains(text(), 'Llamadme') or contains(text(), 'contactar') or contains(text(), 'gratis')]")
        for t in triggers:
            if t.is_displayed() and t.tag_name in ['a', 'button', 'span']:
                 print(f"  - Trigger: Tag='{t.tag_name}' Text='{t.text.strip()}'")

        # Inputs
        print("INPUTS:")
        inputs = driver.find_elements(By.TAG_NAME, "input")
        for i in inputs:
             if i.is_displayed() and i.get_attribute('type') not in ['hidden', 'checkbox', 'radio']:
                 print(f"  - Input: Name='{i.get_attribute('name')}' Id='{i.get_attribute('id')}' Type='{i.get_attribute('type')}'")

    except Exception as e:
        print(f"Error inspecting {name}: {e}")

mgr = BrowserManager(headless=False)
try:
    driver = mgr.get_driver()
    
    # Telco
    inspect_page(driver, "O2", "https://o2online.es/")
    inspect_page(driver, "Simyo", "https://www.simyo.es/")
    
    # Insurance
    inspect_page(driver, "Allianz", "https://www.allianz.es/")
    inspect_page(driver, "Generali", "https://www.generali.es/")
    
    # Education
    inspect_page(driver, "Adams", "https://www.adams.es/")

finally:
    mgr.close()
