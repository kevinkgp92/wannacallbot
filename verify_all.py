import time
from services.definitions import security as sec
from services.definitions import general as gen
from core.browser import BrowserManager
from selenium.webdriver.common.by import By

def verify_service(ServiceClass):
    print(f"\n--- VERIFYING {ServiceClass.__name__} ---")
    manager = BrowserManager(headless=True)
    driver = manager.get_driver()
    service = ServiceClass(driver, {'phone':'000','name':'test','email':'test@test.com','surname':'test','zipcode':'28001'})
    
    try:
        print(f"Navigating to {service.url}...")
        driver.get(service.url)
        time.sleep(5)
        
        # Check Cookies
        print("Checking cookies...")
        # (We can't easily verify the cookie click without potentially closing the popup, so we just try to find it)
        # Using the logic from the class itself would be ideal but we want to verify existence first.
        
        # We will parse the 'run' method logic via inspection or just check typical elements?
        # Better: let's try to FIND the elements defined in the service class.
        # Since we can't easily parse Python code at runtime to get the XPaths, 
        # I will manually replicate the checks here based on the known XPaths in the files I just read.
        
        if "Securitas" in service.name:
             check_xpath(driver, '//*[@id="edit-telefono1"]', "Phone Input")
             check_xpath(driver, '//*[@id="edit-submit"]', "Submit Button")
        
        elif "Prosegur" in service.name:
             # Check for either design
             d1 = check_xpath(driver, '//*[@id="formulario-hero-composicion-prosegur-spain-cc-activo"]/div[2]/div[2]/div/input', "Phone Input D1", fatal=False)
             if not d1:
                 check_xpath(driver, '/html/body/main/div/section/div/div/div[2]/section[2]/div/div/div/div/div[1]/div[2]/form/div[2]/div[2]/div/input', "Phone Input D2")

        elif "MasMovil" in service.name:
             check_xpath(driver, "//*[starts-with(@id, 'BysidePhoneBySideData_')]", "Phone Input")
        
        elif "Mapfre" in service.name:
             check_xpath(driver, '//*[@id="nombre"]', "Name Input")
             check_xpath(driver, '//*[@id="tlfn"]', "Phone Input")

        elif "Genesis" in service.name:
             check_xpath(driver, '//*[@id="edit-phone"]', "Phone Input")

        elif "Euroinnova" in service.name:
             check_xpath(driver, '//*[@id="tel"]', "Phone Input")
        
        elif "Racctel" in service.name:
             check_xpath(driver, "//input[@name='phone_number']", "Phone Input")

        elif "Ford" in service.name:
             check_xpath(driver, "//input[@name='MobilePhone' or contains(@placeholder, 'Teléfono')]", "Phone Input (Generic)")

        elif "Vodafone" in service.name:
             check_xpath(driver, "//input[@name='phone' or @type='tel']", "Phone Input")

        elif "Euskaltel" in service.name:
             check_xpath(driver, "//input[@name='phone_number' or contains(@placeholder, 'Telé')]", "Phone Input")

        elif "Pelayo" in service.name:
             check_xpath(driver, "//input[contains(@id, 'phone') or contains(@name, 'telefono')]", "Phone Input")

    except Exception as e:
        print(f"EXCEPTION: {e}")
    finally:
        manager.close()

def check_xpath(driver, xpath, name, fatal=True):
    try:
        els = driver.find_elements(By.XPATH, xpath)
        if len(els) > 0:
            print(f"[OK] Found {name}")
            return True
        else:
            msg = f"[FAIL] Could not find {name} with xpath: {xpath}"
            print(msg)
            return False
    except Exception as e:
        print(f"[ERROR] checking {name}: {e}")
        return False

if __name__ == "__main__":
    classes = [
        sec.SecuritasService,
        sec.ProsegurService,
        sec.MasMovilAlarmasService,
        gen.EuroinnovaService,
        gen.MapfreService,
        gen.GenesisService,
        gen.RacctelPlusService,
        gen.FordService,
        gen.VodafoneService,
        gen.EuskaltelService,
        gen.PelayoService
    ]
    
    for C in classes:
        verify_service(C)
