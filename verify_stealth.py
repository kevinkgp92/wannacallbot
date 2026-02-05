from core.browser import BrowserManager
import time

def verify_stealth():
    print("Testing browser stealth mode (forcing Chrome)...")
    bm = BrowserManager(headless=True)
    # Force chrome for this test
    driver = bm._setup_chrome()
    
    # Check navigator.webdriver
    result = driver.execute_script("return navigator.webdriver")
    print(f"navigator.webdriver: {result}")
    
    # Check user agent
    ua = driver.execute_script("return navigator.userAgent")
    print(f"User Agent: {ua}")
    
    if result is None or result is False:
        print("SUCCESS: Stealth mode active!")
    else:
        print("WARNING: Stealth mode might be detected.")
        
    driver.quit()

if __name__ == "__main__":
    verify_stealth()
