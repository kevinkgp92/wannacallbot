import requests
import re
import random
import time
import json
import concurrent.futures

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

    def _batch_filter_country(self, proxies, country_code, stop_signal=None):
        """Filters a chunk of proxies by country using ip-api batch."""
        valid_proxies = []
        
        # Chunk into 100 (API limit)
        chunks = [proxies[i:i + 100] for i in range(0, len(proxies), 100)]
        
        import concurrent.futures
        
        def process_chunk(chunk):
            if stop_signal and stop_signal(): return []
            matches = []
            try:
                # Prepare IPs
                ips = []
                clean_chunk = []
                for p in chunk:
                     if ":" in p:
                         ip = p.split(':')[0]
                         ips.append(ip)
                         clean_chunk.append(p)

                if not max(ips, default=0): return [] # Safety check

                # API expects: [{"query": "ip"}, ...]
                data = [{"query": ip, "fields": "countryCode"} for ip in ips]
                
                # High timeout for API stability
                r = requests.post("http://ip-api.com/batch", json=data, timeout=10)
                results = r.json()
                
                for idx, res in enumerate(results):
                    if res.get('countryCode') == country_code:
                        matches.append(clean_chunk[idx])
            except: pass
            return matches

        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(process_chunk, chunk) for chunk in chunks]
            for future in concurrent.futures.as_completed(futures):
                if stop_signal and stop_signal(): 
                    executor.shutdown(wait=False, cancel_futures=True)
                    return []
                found = future.result()
                if found: valid_proxies.extend(found)

        return valid_proxies

    def scrape(self, country=None, allow_fallback=False, stop_signal=None):
        """Mass Scrapes and HUNTS for valid proxies using a TIERED approach."""
        target_country = country if country else "Global"
        print(f"ℹ️ Escaneando proxies ({target_country})...")
        
        if stop_signal and stop_signal(): return []

        # --- SOURCES DEFINITION ---
        
        # TIER 1: HIGH QUALITY / TARGETED (We want to check these FIRST)
        es_sources = [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=es&ssl=all&anonymity=all",
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=10000&country=es&ssl=all&anonymity=all",
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=10000&country=es&ssl=all&anonymity=all",
            "https://www.proxy-list.download/api/v1/get?type=http&country=ES",
            "https://www.proxy-list.download/api/v1/get?type=https&country=ES",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/ES_RAW.txt",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
            "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
            "https://www.proxyscan.io/api/proxy?country=es&format=txt",
            "https://spys.me/proxy.txt"
        ]
        
        # TIER 2: MASSIVE HAYSTACK (Only used if Tier 1 fails)
        global_sources = [
            # HTTP Only (Protocol Fix)
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
            "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt",
            "https://raw.githubusercontent.com/zloi-user/hideip.me/main/http.txt",
            "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/http.txt",
            "https://raw.githubusercontent.com/SevenWorksDev/proxy-list/main/proxies/http.txt",
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
            "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt",
            "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
            "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt",
            "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt"
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
        # TURBO MODE: Check 60 sources in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=60) as executor:
            futures = [executor.submit(fetch_one, u) for u in urls]
            for future in concurrent.futures.as_completed(futures):
                if stop_signal and stop_signal():
                    executor.shutdown(wait=False, cancel_futures=True)
                    return set()
                found = future.result()
                if found: collected.update(found)
            return collected

        self.proxies = [] # Reset

        # =========================================================================
        # PHASE 1: TIER 1 (TARGETED) - Fast & High Quality
        # =========================================================================
        if country == "ES":
            print(f"🚀 FASE 1: Buscando en fuentes ES específicas (Prioridad Alta)...")
            tier1_candidates = list(fetch_sources(es_sources, "(ES/Targeted)"))
            print(f"  📥 Recolectedos {len(tier1_candidates)} candidatos ES.")
            
            if tier1_candidates:
                # Direct check (no need to batch heavily, usually < 2000 IPs)
                # But we still run Geo-Filter to be sure (some lists are mixed)
                geo_matches = self._batch_filter_country(tier1_candidates, "ES", stop_signal)
                if geo_matches:
                     live_matches = self._check_proxies_live(geo_matches, stop_signal)
                     if live_matches:
                         self.proxies.extend(live_matches)
                         print(f"  ✅ FASE 1 ÉXITO: {len(self.proxies)} proxies ES encontrados.")
            
            # EARLY EXIT if we found enough
            # v2.2.4: If we have even ONE good targeted proxy, we START.
            # No need to wait for massive mining.
            if len(self.proxies) >= 1:
                 print(f"✅ LISTA FINAL: {len(self.proxies)} proxies operativos (FASE 1).")
                 return self.proxies
            else:
                 print("⚠️ Fase 1 insuficiente. Activando FASE 2 (Búsqueda Masiva Global)...")

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
        BATCH_SIZE = 3000
        GOAL = 3       # v2.2.4: Lowered goal to 3 to prevent "half hour" waits
        MAX_SCAN = 80000 
        
        scanned = 0
        print(f"  🦅 Iniciando Caza de Proxies (Meta: {GOAL} Vivos | Límite: {MAX_SCAN})...")
        
        for i in range(0, len(tier2_candidates), BATCH_SIZE):
            if stop_signal and stop_signal(): break
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
        return self.proxies

    def _check_proxies_live(self, proxies, stop_signal=None):
        """Verifies if proxies are actually ALIVE before using them."""
        print(f"  ⚡ Verificando conectividad de {len(proxies)} candidatos españoles...")
        alive = []
        
        def is_alive(proxy):
            if stop_signal and stop_signal(): return False
            try:
                # Fast check using Google Gen_204
                # v2.2.5 DEBUG: Print errors
                r = requests.get(
                    "http://clients3.google.com/generate_204", 
                    proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"}, 
                    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"},
                    timeout=8 
                )
                if r.status_code == 204 or r.status_code == 200:
                    return proxy
                # else:
                #     print(f"X {proxy}: Status {r.status_code}")
            except Exception as e: 
                # print(f"X {proxy}: {e}") # Uncomment for extreme debug
                pass
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
