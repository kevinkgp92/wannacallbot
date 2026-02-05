import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()

TARGETS = [
    ("Sanitas", "https://www.sanitas.es/"),
    ("Adeslas", "https://www.segurcaixaadeslas.es/"),
    ("iSalud", "https://www.isalud.com/"),
    ("Holaluz", "https://www.holaluz.com/"),
    ("CEAC", "https://www.ceac.es/")
]

def detailed_inspect(driver, name):
    print(f"\n--- INSPECTING: {name} ---")
    
    # Try to find common "Call me" keywords
    keywords = ["llamamos", "teléfono", "telefono", "gratis", "contactar", "llamar"]
    
    # Dump all input fields
    inputs = driver.find_elements(By.TAG_NAME, "input")
    print(f"Found {len(inputs)} input fields.")
    for i in inputs[:15]: # Limit to first 15 to avoid spam
        try:
            t = i.get_attribute("type")
            nid = i.get_attribute("id")
            name_attr = i.get_attribute("name")
            placeholder = i.get_attribute("placeholder")
            print(f"INPUT: Type='{t}' ID='{nid}' Name='{name_attr}' Placeholder='{placeholder}'")
        except: pass

    # Dump buttons
    buttons = driver.find_elements(By.TAG_NAME, "button")
    print(f"Found {len(buttons)} buttons.")
    for b in buttons:
        try:
            txt = b.text.lower()
            if any(k in txt for k in keywords):
                print(f"BUTTON (MATCH): Text='{b.text}' Class='{b.get_attribute('class')}'")
        except: pass
        
    # Check iframes
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    print(f"Found {len(iframes)} iframes.")
    for i, frame in enumerate(iframes):
        print(f"  IFRAME {i}: Src='{frame.get_attribute('src')}'")

def run_inspection():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    # options.add_argument("--headless") # Headless might hide some overlays
    
    driver = webdriver.Chrome(options=options)
    
    for name, url in TARGETS:
        try:
            print(f"Navigating to {name} ({url})...")
            driver.get(url)
            time.sleep(5) # Give it time to load dynamic content
            detailed_inspect(driver, name)
        except Exception as e:
            print(f"Error inspecting {name}: {e}")
            
    driver.quit()

if __name__ == "__main__":
    run_inspection()
