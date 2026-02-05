import requests
import re
import random
import time
import json
import concurrent.futures
import os

CACHE_FILE = "core/proxies_cache.json"

class ProxyScraper:
    def __init__(self):
        self.sources = [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
            "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
            "https://raw.githubusercontent.com/clketlow/proxy-list/master/http.txt",
            "https://www.proxy-list.download/api/v1/get?type=http"
        ]
        self.proxies = []
        self.geo_cache = {} # IP -> CountryCode
        self.last_scrape_time = 0
        self.golden_cache_file = "core/golden_proxies.json"
        self._load_cache()

    def _load_cache(self):
        """Loads verified proxies from local cache."""
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, "r") as f:
                    self.proxies = json.load(f)
                if self.proxies:
                    print(f"  📦 Caché cargada: {len(self.proxies)} proxies guardados.")
            except: self.proxies = []

    def _save_cache(self):
        """Saves current verified proxies to local cache."""
        try:
            # Keep only unique and non-empty
            clean = list(set([p for p in self.proxies if p]))
            with open(CACHE_FILE, "w") as f:
                json.dump(clean, f)
            
            # Save "Golden" (known good ES) proxies separately for faster reuse
            if hasattr(self, 'golden_proxies') and self.golden_proxies:
                with open(self.golden_cache_file, "w") as f:
                    json.dump(list(self.golden_proxies)[:50], f)
        except: pass

    def _batch_filter_country(self, proxies, country_code, stop_signal=None):
        """Filters a chunk of proxies by country using multiple Geo-IP APIs with caching."""
        valid_proxies = []
        clean_proxies = [p for p in proxies if ":" in p]
        
        # 1. Check Cache first
        uncached = []
        for p in clean_proxies:
            ip = p.split(':')[0]
            if ip in self.geo_cache:
                if self.geo_cache[ip] == country_code:
                    valid_proxies.append(p)
            else:
                uncached.append(p)
        
        if not uncached: return valid_proxies

        # 2. Process uncached in chunks (Batch API)
        chunks = [uncached[i:i + 100] for i in range(0, len(uncached), 100)]
        
        def process_chunk(chunk):
            if stop_signal and stop_signal(): return []
            matches = []
            ips = [p.split(':')[0] for p in chunk]
            
            # STRATEGY A: ip-api.com (Batch)
            try:
                data = [{"query": ip, "fields": "countryCode"} for ip in ips]
                r = requests.post("http://ip-api.com/batch", json=data, timeout=10)
                if r.status_code == 200:
                    results = r.json()
                    for idx, res in enumerate(results):
                        cc = res.get('countryCode', 'XX')
                        self.geo_cache[ips[idx]] = cc
                        if cc == country_code:
                            matches.append(chunk[idx])
                    return matches
                elif r.status_code == 429:
                    # Rate limited -> Sleep briefly and continue to fallback
                    time.sleep(1)
            except: pass

            # STRATEGY B: Turbo Resilient Fallback (v2.2.23 - Parallelized)
            # Parallelize individual checks to avoid linear delays
            sub_chunk = chunk[:30] # Check up to 30 candidates per batch failure
            
            def check_single_candidate(p):
                if stop_signal and stop_signal(): return None
                ip = p.split(':')[0]
                if ip in self.geo_cache:
                    return p if self.geo_cache[ip] == country_code else None

                try:
                    # Use a short timeout for turbo mode
                    r = requests.get(f"https://ipapi.co/{ip}/country/", timeout=3)
                    if r.status_code == 200:
                        cc = r.text.strip().upper()
                        self.geo_cache[ip] = cc
                        return p if cc == country_code else None
                    elif r.status_code == 429:
                        r2 = requests.get(f"http://ip-api.com/json/{ip}?fields=countryCode", timeout=2)
                        cc = r2.json().get("countryCode", "XX")
                        self.geo_cache[ip] = cc
                        return p if cc == country_code else None
                except: pass
                return None

            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor: # Dropped from 20 to 5 for CPU
                results = list(executor.map(check_single_candidate, sub_chunk))
                matches.extend([r for r in results if r])
            
            return matches

        # TURBO GEO-FILTER: Increased from 40 to 50 workers for v2.2.19
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(process_chunk, chunk) for chunk in chunks]
            for future in concurrent.futures.as_completed(futures):
                found = future.result()
                if found: valid_proxies.extend(found)

        return valid_proxies

    def _scrape_html_tables(self, stop_signal=None):
        """Scrapes Spanish proxies from HTML tables on specialized sites."""
        found = set()
        targets = [
            ("https://www.proxynova.com/proxy-server-list/country-es/", r'document\.write\(\'(\d+\.\d+\.\d+\.\d+)\'\);'),
            ("https://proxy-list.org/spanish/index.php", r'\d+\.\d+\.\d+\.\d+:\d+'),
            ("https://proxydb.net/?country=ES", r'\d+\.\d+\.\d+\.\d+:\d+'),
            ("https://www.proxyserverlist24.top/search/label/Spain", r'\d+\.\d+\.\d+\.\d+:\d+'),
            ("https://free-proxy-list.net/spanish-proxy.html", r'\d+\.\d+\.\d+\.\d+:\d+')
        ]
        
        for url, pattern in targets:
            if stop_signal and stop_signal(): break
            try:
                print(f"  🕸️ Deep Scraping: {url}...")
                r = requests.get(url, timeout=12, headers={"User-Agent": "Mozilla/5.0"})
                if r.status_code == 200:
                    # ProxyNova uses JS obfuscation for the IP
                    if "proxynova" in url:
                        ips = re.findall(pattern, r.text)
                        # Ports are in a separate span usually, or hardcoded
                        for ip in ips:
                            found.add(f"{ip}:80") # ProxyNova default common
                            found.add(f"{ip}:8080")
                    else:
                        matches = re.findall(pattern, r.text)
                        found.update(matches)
            except: pass
        return list(found)

    def scrape(self, country=None, allow_fallback=False, stop_signal=None):
        """Mass Scrapes and HUNTS for valid proxies using a TIERED approach."""
        target_country = country if country else "Global"
        print(f"ℹ️ Escaneando proxies ({target_country})...")
        
        if stop_signal and stop_signal(): return []

        # --- SOURCES DEFINITION ---
        
        # TIER 1: THE SPANISH ARMADA 5.0 (v2.2.22) - Elite Targeted
        es_sources = [
            "https://api.proxyscrape.com/v4/free-proxy-list/get?request=displayproxies&protocol=http&country=es",
            "https://api.proxyscrape.com/v4/free-proxy-list/get?request=displayproxies&protocol=socks4&country=es",
            "https://api.proxyscrape.com/v4/free-proxy-list/get?request=displayproxies&protocol=socks5&country=es",
            "https://www.proxy-list.download/api/v1/get?type=http&country=ES",
            "https://www.proxy-list.download/api/v1/get?type=https&country=ES",
            "https://www.proxy-list.download/api/v1/get?type=socks4&country=ES",
            "https://www.proxy-list.download/api/v1/get?type=socks5&country=ES",
            "https://raw.githubusercontent.com/mmpx12/proxy-list/master/proxies/es.txt",
            "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/countries/es.txt",
            "https://raw.githubusercontent.com/vakhov/free-proxy-list/master/proxies/es.txt",
            "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/es.txt",
            "https://raw.githubusercontent.com/officialputuid/free-proxy-list/master/proxies/es.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/ES_RAW.txt",
            "https://www.proxyscan.io/api/proxy?country=es&format=txt",
            "https://proxyspace.pro/spain.txt",
            "https://raw.githubusercontent.com/Anonymouse-prox/free-proxy-list/master/proxies/es.txt",
            "https://raw.githubusercontent.com/Zaeem20/free-proxy-list/master/proxies/es.txt",
            "https://raw.githubusercontent.com/ObcbS/free-proxy-list/master/proxies/es.txt",
            "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt", # High speed
            "https://github.com/ErcinDedeoglu/proxies/raw/main/proxies/http.txt", # Spanish heavy
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt", # Filtered
            "https://api.openproxylist.xyz/http.txt"
        ]
        
        # TIER 2: MASSIVE HAYSTACK (Polluted lists move here)
        global_sources = [
            "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-all.txt",
            "https://spys.me/proxy.txt",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
            "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/http.txt",
            "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks5.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
            "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt",
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
        ]

        # Helper to fetch a list of URLs
        def fetch_sources(urls, label=""):
            print(f"  📡 Descargando {len(urls)} fuentes {label}...")
            collected = set()
            
            def fetch_one(url):
                if stop_signal and stop_signal(): return []
                try:
                    r = requests.get(url, timeout=6)
                    if r.status_code == 200:
                        return re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', r.text)
                except: pass
                return []

            import concurrent.futures
            # COOLING MODE: Throttled to 20 workers to avoid 100% CPU spikes
            with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                futures = [executor.submit(fetch_one, u) for u in urls]
                for future in concurrent.futures.as_completed(futures):
                    if stop_signal and stop_signal():
                        executor.shutdown(wait=False, cancel_futures=True)
                        return set()
                    found = future.result()
                    if found: collected.update(found)
            return collected

        # =========================================================================
        # PHASE 0: PERSISTENCE & CACHE CHECK (Instant Startup)
        # =========================================================================
        current_time = time.time()
        
        # PERSISTENCE: If we scraped less than 5 minutes ago and we still have proxies, use them.
        # This prevents infinite loops if a single proxy rotation is requested quickly.
        if self.proxies and (current_time - self.last_scrape_time) < 300:
             print(f"🚀 FASE 0: Usando cola persistente ({len(self.proxies)} proxies restantes).")
             return self.proxies

        if self.proxies:
            print(f"🚀 FASE 0: Verificando proxies en caché...")
            cached_live = self._check_proxies_live(self.proxies, stop_signal)
            if cached_live:
                self.proxies = cached_live
                print(f"  ✅ FASE 0 ÉXITO: {len(self.proxies)} proxies de caché operativos.")
                if len(self.proxies) >= 3: # Goal: 3
                    self.last_scrape_time = current_time
                    return self.proxies
            else:
                self.proxies = [] # Clear stale cache
        
        self.proxies = [] # Reset for fresh scrape

        # =========================================================================
        # PHASE 1: TIER 1 (TARGETED) - Fast & High Quality
        # =========================================================================
        if country == "ES":
            print(f"🚀 FASE 1: Buscando en fuentes ES específicas (Prioridad Alta)...")
            tier1_candidates = list(fetch_sources(es_sources, "(ES/Targeted)"))
            print(f"  📥 Recolectedos {len(tier1_candidates)} candidatos ES.")
            
            if tier1_candidates:
                # v2.2.20: MANDATORY Geo-Check re-enabled. No more trust loops.
                print(f"  🛡️ Guardia ES: Verificando procedencia geográfica de {len(tier1_candidates)} candidatos...")
                geo_es = self._batch_filter_country(tier1_candidates, "ES", stop_signal)
                if geo_es:
                    print(f"    📥 {len(geo_es)} proxys confirmados como ESPAÑOLES reales.")
                    live_matches = self._check_proxies_live(geo_es, stop_signal)
                    if live_matches:
                        self.proxies.extend(live_matches)
                        print(f"  ✅ FASE 1 ÉXITO: {len(self.proxies)} proxies ES 100% reales.")
            
            # EARLY EXIT if we found enough
            # v2.2.4: If we have even ONE good targeted proxy, we START.
            # No need to wait for massive mining.
            # EMERGENCY: Check HTML Tables if Tier 1 lists are dry
            if not self.proxies:
                print("  🛰️ Fase 1.5: Deep Scrape de Tablas HTML...")
                html_candidates = self._scrape_html_tables(stop_signal)
                if html_candidates:
                    geo_matches = self._batch_filter_country(html_candidates, "ES", stop_signal)
                    live_matches = self._check_proxies_live(geo_matches, stop_signal)
                    if live_matches:
                        self.proxies.extend(live_matches)

            if len(self.proxies) >= 3:
                 print(f"✅ LISTA FINAL: {len(self.proxies)} proxies operativos (FASE 1/1.5).")
                 self.last_scrape_time = time.time()
                 return self.proxies
            else:
                 print(f"⚠️ Fase 1 insuficiente ({len(self.proxies)}/3). Activando FASE 2 para completar...")
                 # DO NOT RETURN, CONTINUE TO PHASE 2 to collect more.

        # =========================================================================
        # PHASE 2: TIER 2 (MASSIVE) - The Haynes Stack
        # =========================================================================
        
        # If ES, use global sources. If Global, use global sources.
        target_list = global_sources
        
        print(f"🚀 FASE 2: Minería Masiva Global (Esto puede tardar)...")
        tier2_candidates = list(fetch_sources(target_list, "(Global)"))
        random.shuffle(tier2_candidates)
        print(f"  📥 Recolectados {len(tier2_candidates)} candidatos crudos.")
        
        # If we are in "Global Mode", just verify and return a chunk
        if country != "ES": 
             # Logic for global...
             self.proxies = tier2_candidates[:100] # Simplified for now
             return self.proxies

        # HUNTING LOOP for ES in Tier 2
        BATCH_SIZE = 1500 # Smaller batches for more frequent updates
        GOAL = 3
        MAX_SCAN = 60000 
        START_TIME = time.time()
        
        scanned = 0
        print(f"  🦅 Iniciando Caza de Proxies (Meta: {GOAL} Vivos | Límite: {MAX_SCAN})...")
        
        for i in range(0, len(tier2_candidates), BATCH_SIZE):
            if stop_signal and stop_signal(): break
            
            # DESPERATION MODE (v2.2.19): If we have at least 1 and 60s passed, GO.
            elapsed = time.time() - START_TIME
            if elapsed > 60 and len(self.proxies) >= 1:
                print(f"  ⚠️ MODO DESESPERACIÓN: {int(elapsed)}s transcurridos. Arrancando con {len(self.proxies)} proxies.")
                break

            if scanned >= MAX_SCAN: 
                print("  ⚠️ Límite de escaneo alcanzado.")
                break
            
            chunk = tier2_candidates[i:i+BATCH_SIZE]
            print(f"    🔍 Analizando lote {i//BATCH_SIZE + 1} ({len(chunk)} IPs)...")
            
            # 1. Geo Filter
            geo_matches = self._batch_filter_country(chunk, "ES", stop_signal)
            if geo_matches:
                print(f"      🌍 Encontrados {len(geo_matches)} candidatos ES. Verificando vida...")
                # 2. Live Check
                live_matches = self._check_proxies_live(geo_matches, stop_signal)
                if live_matches:
                        self.proxies.extend(live_matches)
                        print(f"      ✅ +{len(live_matches)} Vivos. Total: {len(self.proxies)}/{GOAL}")
            
            scanned += len(chunk)
            
            if len(self.proxies) >= GOAL:
                print("  🎯 Meta de proxies alcanzada.")
                break

        print(f"✅ LISTA FINAL: {len(self.proxies)} proxies operativos.")
        self.last_scrape_time = time.time()
        self._save_cache()
        return self.proxies

    def _check_proxies_live(self, proxies, stop_signal=None):
        """Verifies if proxies are actually ALIVE before using them."""
        print(f"  ⚡ Verificando conectividad de {len(proxies)} candidatos españoles...")
        alive = []
        
        def is_alive(proxy):
            if stop_signal and stop_signal(): return None
            
            # Triple-Check Logic (v2.2.19)
            # A proxy is alive if it passes at least 2 checks
            checks_passed = 0
            proto = "http"
            actual_proxy = proxy
            if "|" in proxy:
                proto, actual_proxy = proxy.split("|", 1)
            
            proxy_dict = {proto: f"{proto}://{actual_proxy}"}
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            
            # Check 1: Google (The OSINT standard)
            try:
                r = requests.get("https://clients3.google.com/generate_204", 
                                 proxies=proxy_dict, timeout=12, headers=headers)
                if r.status_code == 204: checks_passed += 1
            except: pass

            # Check 2: Icanhazip (Reliable IP reflector)
            try:
                r = requests.get("https://ipv4.icanhazip.com", 
                                 proxies=proxy_dict, timeout=10, headers=headers)
                if r.status_code == 200 and len(r.text.strip()) <= 15: checks_passed += 1
            except: pass

            # Check 3: Bing (Backup search engine)
            if checks_passed < 2:
                try:
                    r = requests.get("https://www.bing.com", 
                                     proxies=proxy_dict, timeout=10, headers=headers)
                    if r.status_code == 200: checks_passed += 1
                except: pass

            if checks_passed >= 2:
                return proxy
            return None

        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(is_alive, p) for p in proxies]
            for future in concurrent.futures.as_completed(futures):
                if stop_signal and stop_signal(): 
                    executor.shutdown(wait=False, cancel_futures=True)
                    return []
                res = future.result()
                if res: alive.append(res)
        
        print(f"  ✅ {len(alive)} proxies funcionan de verdad (Alive Check).")
        return alive

    def blacklist_proxy(self, proxy):
        """Removes a bad proxy from the active list."""
        if proxy in self.proxies:
            print(f"  🚫 Blacklisting Proxy: {proxy}")
            self.proxies.remove(proxy)
            self._save_cache() # Persist the removal

    def get_random_proxy(self):
        if not self.proxies:
            self.scrape(country="ES") # Auto-default to ES for safety
        
        if self.proxies:
            return random.choice(self.proxies)
        return None

    def verify_proxy(self, proxy_str, check_country=None):
        """Verifies if a proxy is working and not blocked by Google. Optional: Checks country."""
        proxies = {
            "http": f"http://{proxy_str}",
            "https": f"http://{proxy_str}"
        }
        try:
            # First check: Basic connectivity
            r = requests.get("https://ipv4.icanhazip.com", proxies=proxies, timeout=5)
            if r.status_code == 200:
                
                # OPTIONAL: Strict Country Check (Geo-Guard)
                if check_country:
                    try:
                        # query ip-api for country code
                        geo = requests.get(f"http://ip-api.com/json/{r.text.strip()}?fields=countryCode", timeout=5).json()
                        real_cc = geo.get("countryCode", "XX").upper()
                        
                        if real_cc != check_country.upper():
                            print(f"  ⚠️ Proxy funcional pero país incorrecto ({real_cc} != {check_country}). Rechazado.")
                            return False
                        print(f"  🌍 Geo-Guard: Proxy confirmado en {real_cc}.")
                    except Exception as e: 
                        # STRICT MODE: If we can't verify country, we assume it's NOT Spain.
                        print(f"  ⚠️ Geo-Guard Falló (Timeout/Error): {e} -> RECHAZADO por seguridad.")
                        return False

                # Second check: Google connectivity (Strict check for OSINT)
                r2 = requests.get("https://www.google.com/gen_204", proxies=proxies, timeout=5)
                if r2.status_code == 204 or r2.status_code == 200:
                    print(f"  ✅ Proxy OK: {proxy_str}")
                    return True
                else:
                    print(f"  ⚠️ Proxy funcional pero bloqueado por Google: {proxy_str}")
        except:
            pass
        return False

    def get_valid_proxy(self, max_attempts=10, prefer_es=True, check_country=None, stop_signal=None):
        """Gets a proxy that actually works. Prioritizes ES if requested. Optional strict country check."""
        if not self.proxies:
            self.scrape(country="ES" if prefer_es else None, stop_signal=stop_signal)
            
        attempts = 0
        while attempts < max_attempts:
            if stop_signal and stop_signal(): return None
            
            proxy = self.get_random_proxy()
            if not proxy: break
            
            if self.verify_proxy(proxy, check_country=check_country):
                return proxy
            
            # Remove bad proxy
            if proxy in self.proxies:
                self.proxies.remove(proxy)
            attempts += 1
            
        return None

def scrape_proxies():
    """Helper function to scrape and save proxies to a file."""
    scraper = ProxyScraper()
    proxies = scraper.scrape()
    with open("proxies.txt", "w", encoding="utf-8") as f:
        for p in proxies:
            f.write(f"{p}\n")
    return len(proxies)

if __name__ == "__main__":
    count = scrape_proxies()
    print(f"Scraped {count} proxies and saved to proxies.txt")
