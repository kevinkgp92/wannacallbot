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
        
        # v2.2.59: Titan Ultimatum - Absolute Zero Cache Purge
        try:
            if os.path.exists(CACHE_FILE): os.remove(CACHE_FILE)
            if os.path.exists(GEO_CACHE_FILE): os.remove(GEO_CACHE_FILE)
            # print("  🧹 Titan Ultimatum: Caché purgada (Absolute Zero).")
        except: pass
        
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

    def _batch_filter_country(self, proxies, country_code, stop_signal=None):
        """Filters a chunk of proxies by country using multiple Geo-IP APIs with caching."""
        valid_proxies = []
        clean_proxies = [p for p in proxies if ":" in p]
        
        # 1. Check Cache first
        uncached = []
        for p in clean_proxies:
            if p in self.session_blacklist:
                continue
            
            ip = p.split(':')[0]
            if ip in self.geo_cache:
                cc = self.geo_cache[ip]
                # v2.2.60: FIX CRITICO CACHÉ - Aceptar GOLDEN como ES válido
                if cc == country_code or cc == "GOLDEN":
                    valid_proxies.append(p)
                elif cc == "RO_FAKE" or cc == "FAIL" or cc == "BAD_DC":
                    self.session_blacklist.add(p) 
            else:
                uncached.append(p)
        
        if not uncached: return valid_proxies

        # 2. Process uncached in chunks (Batch API)
        chunks = [uncached[i:i + 100] for i in range(0, len(uncached), 100)]
        
        def process_chunk(chunk):
            if stop_signal and stop_signal(): return []
            matches = []
            ips = [p.split(':')[0] for p in chunk]
            
            # STRATEGY A: ip-api.com (Batch) - v2.2.42: Titan Hardened
            try:
                data = [{"query": ip, "fields": "status,countryCode,as"} for ip in ips]
                r = requests.post("http://ip-api.com/batch", json=data, timeout=10)
                if r.status_code == 200:
                    results = r.json()
                    # Robust JSON Handle: Ensure results is a list
                    if not isinstance(results, list): return []
                    
                    for idx, res in enumerate(results):
                        if idx >= len(ips): break
                        ip_key = ips[idx]
                        if res.get("status") == "success":
                            cc = res.get('countryCode', 'XX')
                            as_org = res.get('as', '').lower()
                            
                            # v2.2.59: God Particle - Golden Only Policy
                            is_golden_asn = any(asn in as_org for asn in self.residential_asns)
                            is_residential_name = any(x in as_org for x in self.residential_isps)
                            
                            if "m247" in as_org or "romania" in as_org:
                                cc = "RO_FAKE" 
                                self.session_blacklist.add(chunk[idx])
                            elif (is_golden_asn or is_residential_name) and cc == country_code:
                                cc = "GOLDEN"

                            self.geo_cache[ip_key] = cc
                            
                            # v2.2.59: ULTIMATUM - Only GOLDEN IPs are allowed for OSINT
                            if cc == "GOLDEN":
                                matches.append(chunk[idx])
                            else:
                                # v2.2.59: Absolute Zero - Reject everything else
                                self.session_blacklist.add(chunk[idx])
                        else:
                            self.geo_cache[ip_key] = "FAIL"
                            self.session_blacklist.add(chunk[idx])
                    return matches
                elif r.status_code == 429:
                    # v2.2.56: ANTI-429 Omega Jitter
                    wait_time = random.uniform(2.0, 5.0)
                    print(f"  ⚠️ Geo-Check Rate Limited (429). Jitter activado: {wait_time:.1f}s...")
                    time.sleep(wait_time)
                    return [] 
            except Exception as e: 
                print(f"  ⚠️ Geo-Check Error: {e}")
                pass

            # STRATEGY B: Turbo Resilient Fallback (v2.2.53 - Deep Detect)
            sub_chunk = chunk[:40] 
            
            def check_single_candidate(p):
                if stop_signal and stop_signal(): return None
                ip = p.split(':')[0]
                if ip in self.geo_cache:
                    cc = self.geo_cache[ip]
                    # v2.2.60: FIX CRITICO - Golden es ES
                    return p if (cc == country_code or cc == "GOLDEN") else None

                try:
                    # v2.2.53: Using a more detailed fallback API
                    # Use ip-api direct with fields
                    r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,countryCode,as", timeout=4)
                    if r.status_code == 200:
                        res = r.json()
                        if res.get("status") == "success":
                            cc = res.get('countryCode', 'XX')
                            as_org = str(res.get('as', '')).lower()
                            
                            # v2.2.57: Atomic ASN Check
                            is_golden_asn = any(asn in as_org for asn in self.residential_asns)
                            is_residential_name = any(x in as_org for x in self.residential_isps)
                            
                            dc_keywords = [
                                "m247", "romania", "datacenter", "hosting", "cloud", "digitalocean", "vultr", 
                                "ovh", "hetzner", "linode", "aws", "amazon", "google", "azure", "microsoft",
                                "stablepoint", "as9009", "as41853", "as200676", "as202422", "as212238", "as16276"
                            ]
                            
                            if any(x in as_org for x in dc_keywords):
                                cc = "RO_FAKE"
                                self.session_blacklist.add(p)
                            elif (is_golden_asn or is_residential_name) and (cc == country_code or cc == "ES"):
                                cc = "GOLDEN"

                            self.geo_cache[ip] = cc
                            # v2.2.60: TOLERANCIA CERO - Solo GOLDEN pasa el filtro
                            return p if cc == "GOLDEN" else None
                        
                    # v2.2.57: ZENITH TRIDENTE (Strategy B: ipapi.co)
                    r2 = requests.get(f"https://ipapi.co/{ip}/json/", timeout=4)
                    if r2.status_code == 200:
                        res = r2.json()
                        cc = res.get("country_code", "XX")
                        asn = str(res.get("asn", "")).lower()
                        org = str(res.get("org", "")).lower()
                        
                        is_golden = any(asn_id in asn or asn_id in org for asn_id in self.residential_asns)
                        
                        if any(x in org for x in ["m247", "romania", "datacenter", "hosting", "as9009"]):
                            cc = "RO_FAKE"
                        elif is_golden and (cc == country_code or cc == "ES"):
                            cc = "GOLDEN"
                            
                        self.geo_cache[ip] = cc
                        return p if cc == "GOLDEN" else None
                    
                    # v2.2.57: ZENITH TRIDENTE (Strategy C: findip.net)
                    # Use findip.net as ultimate fallback
                    r3 = requests.get(f"https://api.findip.net/{ip}/?token=free", timeout=4)
                    if r3.status_code == 200:
                         res = r3.json()
                         cc = res.get("country", {}).get("iso_code", "XX")
                         org = str(res.get("traits", {}).get("autonomous_system_organization", "")).lower()
                         asn = str(res.get("traits", {}).get("autonomous_system_number", "")).lower()
                         
                         is_golden = any(asn_id in f"as{asn}" or asn_id in org for asn_id in self.residential_asns)
                         is_dc = any(x in org for x in ["m247", "romania", "datacenter", "hosting", "as9009"])
                         
                         if is_golden and not is_dc and (cc == country_code or cc == "ES"):
                             self.geo_cache[ip] = "GOLDEN"
                             return p
                         else:
                             self.geo_cache[ip] = "BAD_DC"
                             self.session_blacklist.add(p)
                except: pass
                return None

            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
                results = list(executor.map(check_single_candidate, sub_chunk))
                matches.extend([r for r in results if r])
            
            return matches

        # TURBO GEO-FILTER: Reduced to 5 workers for v2.2.28 (STABILITY FIRST)
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(process_chunk, chunk) for chunk in chunks]
            for future in concurrent.futures.as_completed(futures):
                time.sleep(0.05) # v2.2.36.3: Balanced for Geo-Filter smoothness
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
