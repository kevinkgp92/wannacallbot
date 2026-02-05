import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
# REMOVED: selenium_stealth (Caused path errors in bundled EXE)
import undetected_chromedriver as uc
from core.proxy_scraper import ProxyScraper

class BrowserManager:
    _CACHED_GECKO = None
    _CACHED_CHROME = None

    def __init__(self, headless=False, proxy=None, auto_proxy=False, user_agent=None, stop_check=None):
        self.headless = headless
        self.proxy = proxy 
        self.auto_proxy = auto_proxy
        self.user_agent = user_agent
        self.stop_check = stop_check
        self.scraper = ProxyScraper()
        self.driver = None
        self._kill_zombies() # Clean start

    def _kill_zombies(self):
        """Nuclear cleanup of orphaned browser processes."""
        if os.name == 'nt':
            try:
                # Kill any orphaned drivers that eat CPU
                subprocess.run("taskkill /F /IM chromedriver.exe /T", capture_output=True, shell=True)
                subprocess.run("taskkill /F /IM geckodriver.exe /T", capture_output=True, shell=True)
                # Note: We don't kill chrome.exe/firefox.exe here because the user might be watching YouTube
                # We only kill the automation drivers.
            except: pass

    def _get_proxy(self):
        if self.proxy:
            if isinstance(self.proxy, list):
                import random
                return random.choice(self.proxy)
            return self.proxy
        
        if self.auto_proxy:
            print(f"🌐 Buscando proxy automático (Firefox Mode)...")
            # GEO-GUARD: Force strict country check ("ES") to filter out Romanian/Russian proxies
            p = self.scraper.get_valid_proxy(max_attempts=15, check_country="ES", stop_signal=self.stop_check)
            self.current_proxy = p
            return p
        return None

    def mark_current_proxy_bad(self):
        if hasattr(self, 'current_proxy') and self.current_proxy:
            print(f"🔥 Quemando proxy actual: {self.current_proxy}")
            self.scraper.blacklist_proxy(self.current_proxy)
            self.current_proxy = None

    def get_driver(self, force_chrome=False):
        if self.driver: return self.driver

        # POLICY CHANGE: FIREFOX IS NOW PRIMARY (Lighter, better Captcha handling)
        if not force_chrome:
            try:
                print("🦊 Iniciando Firefox (Modo Ligero)...")
                self.driver = self._setup_firefox()
                return self.driver
            except Exception as e:
                print(f"⚠️ Firefox falló ({e}). Intentando Chrome...")

        # Fallback or Forced Chrome
        try:
            print("⚪ Iniciando Chrome (Modo Compatibilidad)...")
            self.driver = self._setup_chrome()
            return self.driver
        except Exception as e:
             # Last resort: Undetected Chrome (Unstable)
             try:
                 print(f"⚠️ Chrome estándar falló. Intentando UC ({e})...")
                 self.driver = self._setup_chrome(is_osint=True)
                 return self.driver
             except Exception as final_e:
                 print(f"❌ CRITICAL ERROR: Ningún navegador pudo iniciarse: {final_e}")
                 raise final_e

    def _get_random_user_agent(self):
        import random
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0"
        ]
        return random.choice(user_agents)

    def _setup_firefox(self):
        options = webdriver.FirefoxOptions()
        options.page_load_strategy = 'eager' # Load faster
        
        if self.headless:
            options.add_argument("--headless")
        
        # Proxy (Supports HTTP, SOCKS4, SOCKS5)
        proxy_str = self._get_proxy()
        if proxy_str:
            proto = "http"
            actual_proxy = proxy_str
            if "|" in proxy_str:
                proto, actual_proxy = proxy_str.split("|", 1)
            
            host, port = actual_proxy.split(':')
            options.set_preference("network.proxy.type", 1)
            
            if proto.startswith("socks"):
                options.set_preference("network.proxy.socks", host)
                options.set_preference("network.proxy.socks_port", int(port))
                options.set_preference("network.proxy.socks_version", 5 if proto == "socks5" else 4)
                options.set_preference("network.proxy.socks_remote_dns", True)
            else:
                options.set_preference("network.proxy.http", host)
                options.set_preference("network.proxy.http_port", int(port))
                options.set_preference("network.proxy.ssl", host)
                options.set_preference("network.proxy.ssl_port", int(port))
            
            print(f"  🔗 Usando Proxy ({proto.upper()}): {actual_proxy}")

        # SSL / Security Bypass (Nuclear Mode)
        options.accept_insecure_certs = True
        options.set_preference("network.stricttransportsecurity.preloadlist.mode", 2)
        options.set_preference("security.enterprise_roots.enabled", True)
        options.set_preference("security.cert_pinning.enforcement_level", 0)

        # Native Firefox Stealth & Spanish Locale
        ua = self.user_agent if self.user_agent else self._get_random_user_agent()
        options.set_preference("general.useragent.override", ua)
        options.set_preference("intl.accept_languages", "es-ES,es")
        options.set_preference("general.useragent.locale", "es-ES")
        options.set_preference("dom.webdriver.enabled", False)
        options.set_preference("useAutomationExtension", False)
        # Disable tracking to reduce overhead involved with blocking lists
        options.set_preference("privacy.trackingprotection.enabled", False) 
        
        # Optimize RAM & Speed: SLIM MODE (v2.2.23)
        options.set_preference("browser.sessionhistory.max_entries", 2)
        options.set_preference("browser.cache.disk.enable", False)
        options.set_preference("browser.cache.memory.enable", True)
        options.set_preference("browser.cache.memory.capacity", 51200) # 50MB cap
        
        # NUCLEAR RAM SAVER: Disable Images and Media
        options.set_preference("permissions.default.image", 2) # 1=Allow, 2=Block
        options.set_preference("media.autoplay.enabled", False)
        options.set_preference("media.process.enabled", False)
        options.set_preference("media.audio_video.enabled", False)
        options.set_preference("pdfjs.disabled", True)
        

        # HARDENED REGION: Force Spain regardless of IP
        options.set_preference("browser.search.region", "ES")
        options.set_preference("browser.search.countryCode", "ES")
        options.set_preference("browser.search.isUS", False)
        options.set_preference("browser.region.network.url", "")  # Disable network region check
        options.set_preference("browser.search.geoip.url", "")    # Disable GeoIP lookup
        options.set_preference("intl.accept_languages", "es-ES")  # STRICT Spanish only

        path = None
        if BrowserManager._CACHED_GECKO:
            path = BrowserManager._CACHED_GECKO
        else:
            try:
                if os.path.exists("geckodriver.exe"):
                    path = os.path.abspath("geckodriver.exe")
                else:
                    path = GeckoDriverManager().install()
                BrowserManager._CACHED_GECKO = path
            except: path = None

        if path:
            service = FirefoxService(executable_path=path)
        else:
            service = FirefoxService()
        
        driver = webdriver.Firefox(service=service, options=options)
        driver.set_page_load_timeout(35) # Policy: Max 35s per page
        driver.set_script_timeout(10)
        self._force_spain_context(driver)
        return driver
    
    def _force_spain_context(self, driver):
        """Forces Spanish geolocation, timezone, and regional signals."""
        try:
            # For Chrome/Edge (CDP)
            if hasattr(driver, "execute_cdp_cmd"):
                # 1. Madrid Geolocation
                driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
                    "latitude": 40.4168,
                    "longitude": -3.7038,
                    "accuracy": 100
                })
                # 2. Timezone Madrid
                driver.execute_cdp_cmd("Emulation.setTimezoneOverride", {
                    "timezoneId": "Europe/Madrid"
                })
                # 3. Network Locale
                driver.execute_cdp_cmd("Network.setUserAgentOverride", {
                    "userAgent": driver.execute_script("return navigator.userAgent"),
                    "acceptLanguage": "es-ES,es;q=0.9",
                    "platform": "Win32"
                })

            # 4. Javascript Overrides (Universal)
            # This masks navigator.language and prevents WebRTC leaks
            stealth_js = """
            Object.defineProperty(navigator, 'language', {get: () => 'es-ES'});
            Object.defineProperty(navigator, 'languages', {get: () => ['es-ES', 'es']});
            Object.defineProperty(navigator, 'platform', {get: () => 'Win32'});
            
            // WebRTC Leak Protection
            const pc = window.RTCPeerConnection || window.mozRTCPeerConnection || window.webkitRTCPeerConnection;
            if (pc) {
                const shadow = pc.prototype.createOffer;
                pc.prototype.createOffer = function() { return shadow.apply(this, arguments); };
            }
            """
            # If using UC, we can inject on every new document
            if hasattr(driver, "add_script_to_evaluate_on_new_document"):
                 driver.add_script_to_evaluate_on_new_document(stealth_js)
            else:
                 driver.execute_script(stealth_js)
        except: pass

    def _setup_chrome(self, is_osint=False):
        # Only used as fallback
        proxy_str = self._get_proxy()
        
        if is_osint:
            import undetected_chromedriver as uc
            opt = uc.ChromeOptions()
            if self.headless: opt.add_argument("--headless")
            if proxy_str:
                proto = "http"
                actual_proxy = proxy_str
                if "|" in proxy_str:
                    proto, actual_proxy = proxy_str.split("|", 1)
                
                proxy_url = f"{proto}://{actual_proxy}"
                opt.add_argument(f'--proxy-server={proxy_url}')
            # OSINT Force Spanish
            opt.add_argument("--lang=es-ES")
            opt.add_argument("--accept-lang=es-ES,es")
            # SSL Bypass UC
            opt.add_argument("--ignore-certificate-errors")
            opt.add_argument("--ignore-ssl-errors")
            
            driver = uc.Chrome(options=opt)
            self._force_spain_context(driver)
            return driver

        options = webdriver.ChromeOptions()
        if self.headless: 
            print("  👻 Modo Fantasma (Headless) activo en Chrome.")
            options.add_argument("--headless")
        
        if proxy_str:
            proto = "http"
            actual_proxy = proxy_str
            if "|" in proxy_str:
                proto, actual_proxy = proxy_str.split("|", 1)
            
            # Chrome uses schemes like socks5:// or http:// for the proxy server flag
            proxy_url = f"{proto}://{actual_proxy}"
            options.add_argument(f'--proxy-server={proxy_url}')
        
        # Simple native stealth & Spanish Locale
        ua = self.user_agent if self.user_agent else "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        options.add_argument(f"user-agent={ua}")
        options.add_argument("--lang=es-ES")
        options.add_argument("--accept-lang=es-ES,es")
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        # SLIM & COOLING MODE Chrome (v2.2.24)
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--blink-settings=imagesEnabled=false")
        options.add_argument("--disable-background-networking")
        options.add_argument("--no-sandbox")
        
        
        # SSL Bypass Chrome
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--allow-insecure-localhost")
        options.add_argument("--ignore-ssl-errors")
        
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        path = None
        if BrowserManager._CACHED_CHROME:
            path = BrowserManager._CACHED_CHROME
        else:
            try:
                if os.path.exists("chromedriver.exe"):
                    path = os.path.abspath("chromedriver.exe")
                else:
                    path = ChromeDriverManager().install()
                BrowserManager._CACHED_CHROME = path
            except: path = None

        service = ChromeService(executable_path=path) if path else ChromeService()
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(35)
        driver.set_script_timeout(10)
        self._force_spain_context(driver)
        return driver

    def rotate(self):
        """Forces a proxy rotation by clearing the current driver and requesting a new proxy."""
        print("🔄 SISTEMA: Rotando proxy por bloqueo/bajo rendimiento...")
        if self.driver:
            self.close()
        # The next time any setup method is called, it will call _get_proxy() which picks a new one
        return True

    def close(self):
        if self.driver:
            try: self.driver.quit()
            except: pass
            self.driver = None
