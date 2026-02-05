from abc import ABC, abstractmethod
from enum import Enum, auto
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ServiceType(Enum):
    CALL = auto()           # Request a call back
    NIGHT = auto()          # Works at night (automated or message)
    PHYSICAL = auto()       # Sends physical mail
    SMS = auto()            # Sends SMS verification
    INSURANCE = auto()
    ENERGY = auto()
    SOLAR = auto()
    SECURITY = auto()
    EDUCATION = auto()
    AD = auto()             # Advertising/Commercial leads
    ESTATE = auto()         # Real Estate portals

class BaseService(ABC):
    def __init__(self, browser, user_data):
        self.browser = browser
        self.data = user_data
        self.name = "Unknown Service"
        self.types = []
        self.url = ""
        self.status = None # To track outcome (OK, ERROR, WARN)
        self.stealth_level = 1 # 0: Fast, 1: Balanced, 2: Slow

    @abstractmethod
    def run(self):
        pass

    def log(self, message, status=None):
        # Critical Fix: Update the instance status so Manager can count it
        if status:
            self.status = status
            
        try:
            from colorama import Fore, Style, init
            from core.history import HistoryManager # Lazy import
            
            init(autoreset=True)
            prefix = f"[{self.name}]"
            
            if status == 'OK':
                print(f"{Fore.GREEN}✔ {prefix} {message}")
                # Save to history on success
                if self.data.get('phone'):
                     hm = HistoryManager()
                     hm.add_record(str(self.data['phone']), self.name)
            elif status == 'ERROR':
                 print(f"{Fore.RED}✘ {prefix} {message}")
            elif status == 'WARN':
                 print(f"{Fore.YELLOW}⚠ {prefix} {message}")
            else:
                 print(f"{Fore.CYAN}ℹ {prefix} {message}")
        except:
             print(f"[{self.name}] {message}")

    def check_history(self):
        from core.history import HistoryManager
        if not self.data.get('phone'): return False
        
        hm = HistoryManager()
        if hm.is_registered(str(self.data['phone']), self.name):
            self.log("Ya registrado anteriormente. Saltando...", status='WARN')
            return True
        return False
        
    def human_delay(self, min_s=0.5, max_s=1.5):
        import random
        # Stealth multipliers: 0 -> 0.5x (Fast), 1 -> 1.0x (Normal), 2 -> 2.0x (Slow)
        multiplier = [0.5, 1.0, 2.0][self.stealth_level]
        time.sleep(random.uniform(min_s, max_s) * multiplier)

    def navigate(self):
        if self.check_history(): return False # Skip navigation if done
        
        try:
            self.browser.get(self.url)
            self.human_delay(1.5, 3.0) # Privacy: wait for initial load
            return True
        except Exception:
            self.log(f"Error de navegacion (Timeout/Bloqueo)", status='ERROR')
            return False

    def accept_cookies(self, xpath):
        try:
            self.human_delay(1, 2)
            # Short wait for cookie banner
            element = WebDriverWait(self.browser, 5).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            element.click()
            self.human_delay(0.5, 1.2)
        except:
            pass # Cookies not found or already accepted

    def fill(self, xpath, value):
        try:
            self.human_delay(0.2, 0.8)
            el = self.browser.find_element(By.XPATH, xpath)
            self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
            self.human_delay(0.3, 0.7)
            el.clear()
            
            # Simulate real typing with variability and bursts
            multiplier = [0.5, 1.0, 2.0][self.stealth_level]
            for char in value:
                el.send_keys(char)
                # Random delay between characters
                base_delay = random.uniform(0.05, 0.2) * multiplier
                
                # Occasional "thinking" delay or burst
                if random.random() < 0.1: # 10% chance of a longer pause
                    time.sleep(random.uniform(0.3, 0.8) * multiplier)
                else:
                    time.sleep(base_delay)
                    
        except:
            # Fallback: JS set value
            try:
                el = self.browser.find_element(By.XPATH, xpath)
                self.browser.execute_script("arguments[0].value = arguments[1];", el, value)
            except:
                pass

    def click(self, xpath):
        try:
            self.human_delay(0.5, 1.2)
            el = self.browser.find_element(By.XPATH, xpath)
            
            # Subtle mouse movement simulation via JS (hover)
            try:
                self.browser.execute_script("arguments[0].dispatchEvent(new MouseEvent('mouseover', {bubbles: true}));", el)
                self.human_delay(0.2, 0.5)
            except: pass

            self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
            self.human_delay(0.4, 0.9)
            
            # Try normal click, then JS click if fails
            try:
                el.click()
            except:
                self.browser.execute_script("arguments[0].click();", el)
        except:
             pass
    def verify_success(self, success_indicators=["gracias", "enviado", "confirmado", "recibido", "success"]):
        """Check the page source for success keywords."""
        try:
            self.human_delay(2, 4) # Wait for page reaction
            page_text = self.browser.page_source.lower()
            if any(indicator in page_text for indicator in success_indicators):
                return True
            return False
        except:
            return False
