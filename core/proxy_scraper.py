import requests
import re
import random
import time
import json
import concurrent.futures
import threading # v2.2.35: Storm Shield Lock
import os

CACHE_FILE = "core/proxies_cache.json"
GEO_CACHE_FILE = "core/geo_cache.json"

# v2.2.36.2: Restored Spanish Armada Source Lists & Fetcher
global_sources = [
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    "https://raw.githubusercontent.com/clketlow/proxy-list/master/http.txt",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://www.proxyscan.io/download?type=http"
]

# v2.2.58: Titan Finality - Source Purge (UHQ Only)
def get_es_sources():
    today = time.strftime("%Y-%m-%d")
    return [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=es&ssl=all&anonymity=all",
        "https://www.proxyscan.io/download?type=http&country=es",
        "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&country=ES&protocols=http",
        "https://api.openproxy.space/v1/proxies?country=ES&type=http",
        "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/es.txt", # Targeted ES
        "https://raw.githubusercontent.com/yemixzy/proxy-list/main/proxies/http.txt", 
        "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/http.txt",
        "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt", # Filtered by country below anyway
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=10000&country=es&ssl=all&anonymity=all",
        "https://www.proxyscan.io/download?type=socks5&country=es",
        "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt", # High-Freq ES often appears
        "https://raw.githubusercontent.com/Zaeem20/Free-Proxy-List/master/socks5.txt", # Deep ES
        "https://raw.githubusercontent.com/officialputuid/free-proxy-list/master/proxies/http.txt",
        "https://raw.githubusercontent.com/clketlow/proxy-list/master/http.txt",
        f"https://checkerproxy.net/api/archive/{today}"
    ]

es_sources = get_es_sources()

def fetch_sources(urls, label="", stop_signal=None):
    """v2.2.36.2: Restored Parallel fetcher with Arctic Throttling."""
    all_proxies = set()
    
    def fetch_one(url):
        if stop_signal and stop_signal(): return set()
        try:
            r = requests.get(url, timeout=12, headers={"User-Agent": "Mozilla/5.0"})
            if r.status_code == 200:
                matches = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', r.text)
                return set(matches)
        except: pass
        return set()

    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(fetch_one, u) for u in urls]
        for future in concurrent.futures.as_completed(futures):
            time.sleep(0.01) # v2.2.36.3: Reduced from 0.1s to 0.01s for smoother UI
            if stop_signal and stop_signal():
                executor.shutdown(wait=False, cancel_futures=True)
                return set()
            try:
                all_proxies.update(future.result())
            except: pass
    
    return all_proxies

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
        self.last_full_scrape_time = 0 # v2.2.35: Cooldown for source download
        self.scrape_lock = threading.Lock() # v2.2.35: Prevent parallel storm
        self.session_blacklist = set() # v2.2.44: Global session blacklist for RO_FAKE/M247
        # v2.2.57: Titan Zenith - Atomic ASN Whitelist (Unforgeable)
        # v2.2.60: Titan Ultimatum - Expanded Residential Whitelist
        self.residential_asns = [
            "as3352",   # Telefonica / Movistar
            "as12430",  # Vodafone Spain
            "as11831",  # Orange / MasMovil
            "as6739",   # Orange Spain
            "as15704",  # Digi Spain
            "as13134",  # Jazztel
            "as204229", # Avatel
            "as30722",  # Vodafone Enabler
            "as12348",  # Euskaltel
            "as57269",  # Adamo
            "as200902", # MasMovil Broadband
            "as201264", # MasMovil
            "as206411", # Digi Spain v2
            "as213327"  # Digi Spain v3
        ]
        
        self.residential_isps = [
            "movistar", "telefonica", "orange", "vodafone", "digi", 
            "masmovil", "yoigo", "jazztel", "euskaltel", "pepephone", 
            "adamo", "lowi", "simyo", "r cable", "telecable", "guuk"
        ]
        
        # v2.2.64: ZENITH OMEGA API LOCKS
        self.api_locks = {} # {api_name: lock_until_timestamp}
        
        # v2.2.65: TITAN PRIME - Removed Cache Purge for persistence
        self._load_cache()

    def _load_cache(self):
        """Loads verified proxies and geo results from local cache."""
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, "r") as f:
                    self.proxies = json.load(f)
                if self.proxies:
                    print(f"  📦 Caché cargada: {len(self.proxies)} proxies guardados.")
            except: self.proxies = []
        
        # Load Geo Cache (v2.2.53 Persistence)
        if os.path.exists(GEO_CACHE_FILE):
            try:
                with open(GEO_CACHE_FILE, "r") as f:
                    self.geo_cache = json.load(f)
                # print(f"  🌍 Geo-Caché cargado: {len(self.geo_cache)} registros.")
            except: self.geo_cache = {}

    def is_ip_golden(self, ip):
        """v2.2.62: Zenith Trust - Allows external modules to check if an IP is already verified as GOLDEN."""
        res = self.geo_cache.get(ip)
        return res == "GOLDEN"

    def _save_cache(self):
        """Saves current verified proxies and geo results to local cache."""
        try:
            # Keep only unique and non-empty
            clean = list(set([p for p in self.proxies if p]))
            with open(CACHE_FILE, "w") as f:
                json.dump(clean, f)
            
            # Save Geo Cache (v2.2.53 Persistence)
            with open(GEO_CACHE_FILE, "w") as f:
                json.dump(self.geo_cache, f)

            # Save "Golden" (known good ES) proxies separately for faster reuse
            if hasattr(self, 'golden_proxies') and self.golden_proxies:
                with open(self.golden_cache_file, "w") as f:
                    json.dump(list(self.golden_proxies)[:50], f)
        except: pass

    def _is_api_locked(self, name):
        """v2.2.64: Multi-API Lock Manager."""
        lock_time = self.api_locks.get(name, 0)
        return time.time() < lock_time

    def _lock_api(self, name, seconds=60):
        """v2.2.64: Locks an API after receiving a 429."""
        print(f"  🛑 API {name} bloqueada por 429. Tiempo de espera: {seconds}s")
        self.api_locks[name] = time.time() + seconds

    def _check_ip_residence(self, ip, country_code="ES", stop_signal=None):
        """v2.2.64: ZENITH OMEGA - Ultra-Resilient Individual Check with Rotation."""
        if stop_signal and stop_signal(): return None
        
        # 1. Double check cache
        if ip in self.geo_cache:
            cc = self.geo_cache[ip]
            return "GOLDEN" if (cc == country_code or cc == "GOLDEN") else None

        # 2. Rotation Chain (v2.2.65 Expanded to 6 Providers)
        strategies = [
            ("ip-api", f"http://ip-api.com/json/{ip}?fields=status,countryCode,as"),
            ("ipapi-is", f"https://api.ipapi.is/?ip={ip}"),
            ("ipapi-co", f"https://ipapi.co/{ip}/json/"),
            ("ipwho-is", f"https://ipwho.is/{ip}"),
            ("freeipapi", f"https://freeipapi.com/api/json/{ip}"),
            ("findip", f"https://api.findip.net/{ip}/?token=free")
        ]

        for name, url in strategies:
            if self._is_api_locked(name): continue
            if stop_signal and stop_signal(): break
            
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
                r = requests.get(url, timeout=5, headers=headers)
                
                if r.status_code == 429:
                    self._lock_api(name, 60)
                    continue
                
                if r.status_code == 200:
                    data = r.json()
                    cc = "XX"
                    as_org = ""

                    # Specific Parsers
                    if name == "ip-api" and data.get("status") == "success":
                        cc = data.get("countryCode")
                        as_org = str(data.get("as", "")).lower()
                    elif name == "ipapi-is":
                        cc = data.get("location", {}).get("country_code")
                        as_org = str(data.get("asn", {}).get("org", "")).lower()
                    elif name == "ipapi-co":
                        cc = data.get("country_code")
                        as_org = str(data.get("org", "")).lower()
                    elif name == "ipwho-is":
                        cc = data.get("country_code")
                        as_org = str(data.get("connection", {}).get("isp", "")).lower()
                    elif name == "freeipapi":
                        cc = data.get("countryCode")
                        as_org = str(data.get("as_name", "")).lower()
                    elif name == "findip":
                        cc = data.get("country", {}).get("iso_code")
                        as_org = str(data.get("traits", {}).get("autonomous_system_organization", "")).lower()

                    if cc:
                        is_golden_asn = any(asn in as_org for asn in self.residential_asns)
                        is_residential_name = any(x in as_org for x in self.residential_isps)
                        
                        # NUCLEAR BLACKLIST (v2.2.64 Enhanced)
                        bad_dc = ["m247", "romania", "datacenter", "hosting", "cloud", "as9009", "as16276"]
                        if any(x in as_org for x in bad_dc):
                            self.geo_cache[ip] = "BAD_DC"
                            return None
                        
                        if (is_golden_asn or is_residential_name) and (cc == country_code or cc == "ES"):
                            self.geo_cache[ip] = "GOLDEN"
                            return "GOLDEN"
                        else:
                            self.geo_cache[ip] = cc
                            return cc if cc == country_code else None
            except: pass
            time.sleep(0.2)
        
        return None

    def _batch_filter_country(self, proxies, country_code, stop_signal=None):
        """v2.2.64: Zenith Omega Batch Handler - Fixed Scopes and Redundant Checks."""
        valid_proxies = []
        clean_proxies = [p for p in proxies if ":" in p]
        
        uncached = []
        for p in clean_proxies:
            if p in self.session_blacklist: continue
            ip = p.split(':')[0]
            cc = self.geo_cache.get(ip)
            if cc == country_code or cc == "GOLDEN":
                valid_proxies.append(p)
            elif cc in ["RO_FAKE", "FAIL", "BAD_DC"]:
                self.session_blacklist.add(p)
            else:
                uncached.append(p)
        
        if not uncached: return valid_proxies

        # Split into chunks of 100
        chunks = [uncached[i:i + 100] for i in range(0, len(uncached), 100)]
        
        def process_chunk(chunk):
            if stop_signal and stop_signal(): return []
            res_matches = []
            ips = [p.split(':')[0] for p in chunk]
            
            # 1. BATCH STRATEGY (ip-api)
            if not self._is_api_locked("ip-api"):
                try:
                    p_data = [{"query": ip, "fields": "status,countryCode,as"} for ip in ips]
                    r = requests.post("http://ip-api.com/batch", json=p_data, timeout=10)
                    if r.status_code == 200:
                        results = r.json()
                        for idx, res in enumerate(results):
                            if idx >= len(ips): break
                            ip_key = ips[idx]
                            if res.get("status") == "success":
                                as_org = res.get('as', '').lower()
                                cc = res.get('countryCode')
                                if any(asn in as_org for asn in self.residential_asns) and cc == country_code:
                                    self.geo_cache[ip_key] = "GOLDEN"
                                    res_matches.append(chunk[idx])
                                elif "m247" in as_org or "romania" in as_org:
                                    self.geo_cache[ip_key] = "BAD_DC"
                                    self.session_blacklist.add(chunk[idx])
                                else:
                                    self.geo_cache[ip_key] = cc
                    elif r.status_code == 429:
                        self._lock_api("ip-api", 45)
                except: pass

            # 2. INDIVIDUAL FALLBACK FOR THE REMAINING (ZENITH TRIDENTE)
            # Find what's still unknown in this chunk
            processed_ips = [ip for ip in ips if ip in self.geo_cache]
            for p in chunk:
                ip = p.split(':')[0]
                if ip not in processed_ips:
                    if self._check_ip_residence(ip, country_code, stop_signal) == "GOLDEN":
                        res_matches.append(p)
            
            return res_matches

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(process_chunk, c) for c in chunks]
            for f in concurrent.futures.as_completed(futures):
                found = f.result()
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
        
        if stop_signal and stop_signal(): return []

        # =========================================================================
        # PHASE 0: PERSISTENCE & CACHE CHECK (Instant Startup)
        # =========================================================================
        current_time = time.time()
        
        # PERSISTENCE (v2.2.34): If we have enough valid proxies and rescrape is too soon, EXIT.
        if self.proxies and (current_time - self.last_scrape_time) < 120:
             # print(f"🚀 FASE 0: Usando proxies activos (Cooldown: {int(120 - (current_time - self.last_scrape_time))}s).")
             return self.proxies

        if self.proxies:
            # v2.2.35: Only log if we are actually checking something significant
            print(f"🚀 FASE 0: Verificando proxies en caché...")
            cached_live = self._check_proxies_live(self.proxies, stop_signal)
            if cached_live:
                self.proxies = cached_live
                print(f"  ✅ FASE 0 ÉXITO: {len(self.proxies)} proxies de caché operativos.")
                if len(self.proxies) >= 3: 
                    self.last_scrape_time = current_time
                    return self.proxies
        
        # v2.2.35: STORM SHIELD - Guard current scan with a lock
        # If another thread is already scraping, wait for it instead of starting a new scan
        with self.scrape_lock:
            # Check cache AGAIN after obtaining lock (Double-Check Pattern)
            if self.proxies and (time.time() - self.last_scrape_time) < 30:
                return self.proxies
            
            # v2.2.35: SOURCE COOLDOWN - Don't hammer remote sources if we did it recently
            if (time.time() - self.last_full_scrape_time) < 60:
                print(f"⚠️ FASE 1/2 OMITIDA: Escaneo masivo recientemente completado (Cooldown < 60s).")
                return self.proxies

            print(f"ℹ️ Escaneando proxies ({target_country})...")
            self.proxies = [] # Reset for fresh scrape

        # =========================================================================
        # PHASE 1: TIER 1 (TARGETED) - Fast & High Quality
        # =========================================================================
        if country == "ES":
            print(f"🚀 FASE 1: Buscando en fuentes ES específicas (Prioridad Alta)...")
            tier1_candidates = list(fetch_sources(es_sources, "(ES/Targeted)", stop_signal=stop_signal))
            
            # v2.2.54: Titan God Mode - Quantum Yield scaled for mass discovery
            if len(tier1_candidates) > 5000:
                print(f"  🌌 Quantum Yield: Truncando {len(tier1_candidates)} a 5000 candidatos premium.")
                random.shuffle(tier1_candidates)
                tier1_candidates = tier1_candidates[:5000]
            
            print(f"  📥 Candidatos listos para validación (Meta UHQ).")
            
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
        tier2_candidates = list(fetch_sources(target_list, "(Global)", stop_signal=stop_signal))
        random.shuffle(tier2_candidates)
        
        # v2.2.54: Massive Yield Scaling
        if country == "ES" and len(tier2_candidates) > 10000:
            print(f"  🌌 Quantum Yield: Truncando {len(tier2_candidates)} a 10000 candidatos masivos.")
            tier2_candidates = tier2_candidates[:10000]
        
        print(f"  📥 Candidatos listos para caza God Mode.")
        
        # If we are in "Global Mode", just verify and return a chunk
        if country != "ES": 
             # Logic for global...
             self.proxies = tier2_candidates[:100] # Simplified for now
             return self.proxies

        # HUNTING LOOP for ES in Tier 2
        BATCH_SIZE = 100 # v2.2.43: Ultra-Responsive (Reduced from 1500 to 100)
        GOAL = 6 # v2.2.43: Target increased for better diversity
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
        self.last_full_scrape_time = time.time() # v2.2.35: Mark full scan complete
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
            
            # Check 1: Google (v2.2.32: FAST CHECK - 6s)
            try:
                r = requests.get("https://clients3.google.com/generate_204", 
                                 proxies=proxy_dict, timeout=6, headers=headers)
                if r.status_code == 204: checks_passed += 1
            except: pass

            # Check 2: Icanhazip (v2.2.32: FAST CHECK - 5s)
            try:
                r = requests.get("https://ipv4.icanhazip.com", 
                                 proxies=proxy_dict, timeout=5, headers=headers)
                if r.status_code == 200 and len(r.text.strip()) <= 15: checks_passed += 1
            except: pass

            # Check 3: Bing (v2.2.32: FAST CHECK - 5s)
            if checks_passed < 2:
                try:
                    r = requests.get("https://www.bing.com", 
                                     proxies=proxy_dict, timeout=5, headers=headers)
                    if r.status_code == 200: checks_passed += 1
                except: pass

            if checks_passed >= 2:
                return proxy
            return None

        import concurrent.futures
        # v2.2.34: ARCTIC FREEZE - Bajar de 10 a 5 workers para evitar micro-stuttering del GIL
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(is_alive, p) for p in proxies]
            for future in concurrent.futures.as_completed(futures):
                # v2.2.34: Micro-pulso de sueño para dar paso a la GUI
                time.sleep(0.02)
                
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
                    ip = r.text.strip()
                    # v2.2.40: Unified Cache Lookup with Hardened Fields
                    if ip in self.geo_cache:
                        real_cc = self.geo_cache[ip]
                        print(f"  🌍 Geo-Guard (Cache): IP confirmada en {real_cc}.")
                    else:
                        try:
                            # query ip-api for country code - v2.2.40: Hardened Detection
                            geo = requests.get(f"http://ip-api.com/json/{ip}?fields=status,countryCode,as", timeout=5).json()
                            if geo.get("status") == "success":
                                real_cc = geo.get("countryCode", "XX").upper()
                                as_org = geo.get("as", "").lower()
                                
                                # Reject M247 / ROMANIA hosting even if marked as ES
                                if "m247" in as_org or "romania" in as_org:
                                    real_cc = "RO_FAKE"

                                self.geo_cache[ip] = real_cc 
                            else:
                                raise ConnectionError("API Fail Status")
                        except Exception as e: 
                            print(f"  ⚠️ Geo-Guard Falló (Error): {e} -> RECHAZADO.")
                            return False
                        
                    if real_cc != check_country.upper():
                        print(f"  ⚠️ Proxy funcional pero país incorrecto ({real_cc} != {check_country}). Rechazado.")
                        return False
                    print(f"  🌍 Geo-Guard: Proxy confirmado en {real_cc}.")

                # v2.2.54: Titan God Mode - FINAL BOSS CHECK (Real Spanish Domain)
                try:
                    # Test against a purely Spanish resident-facing domain
                    requests.get("https://www.marca.com", proxies=proxies, timeout=4)
                    print(f"  🇪🇸 Genuino ES (Detección Residencial Exitosa).")
                except:
                    print(f"  ⚠️ Proxy funcional pero rechazado por Dominio Local (Marca.com Fail).")
                    return False

                # Second check: Google connectivity (Strict check for OSINT)
                start_google = time.time()
                r2 = requests.get("https://www.google.es/gen_204", proxies=proxies, timeout=5)
                latency = time.time() - start_google
                
                if r2.status_code == 204 or r2.status_code == 200:
                    if latency < 2.0: # v2.2.54: Extreme Latency Filter (2.0s for Elite)
                         print(f"  ✅ Proxy Elite UHQ ({latency:.2f}s): {proxy_str}")
                         return True
                    else:
                         print(f"  ⚠️ Proxy funcional pero lento ({latency:.2f}s). Descartado.")
                         return False
                else:
                    print(f"  ⚠️ Proxy funcional pero bloqueado por Google ES: {proxy_str}")
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
            if not proxy: 
                # v2.2.40: ABSOLUTE COOLDOWN
                print("  ⏳ Pool de proxies agotado. Esperando enfriamiento (10s) para evitar bucle...")
                time.sleep(10) # 10s cooling to prevent high CPU loop
                self.scrape(country="ES" if prefer_es else None, stop_signal=stop_signal)
                if not self.proxies: break 
                proxy = self.get_random_proxy()
            
            if self.verify_proxy(proxy, check_country=check_country):
                return proxy
            
            # Remove bad proxy
            self.blacklist_proxy(proxy)
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
