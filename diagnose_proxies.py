import requests
import re
import concurrent.futures
import time

ES_SOURCES = [
    "https://api.proxyscrape.com/v4/free-proxy-list/get?request=displayproxies&protocol=http&country=es",
    "https://api.proxyscrape.com/v4/free-proxy-list/get?request=displayproxies&protocol=socks4&country=es",
    "https://api.proxyscrape.com/v4/free-proxy-list/get?request=displayproxies&protocol=socks5&country=es",
    "https://www.proxy-list.download/api/v1/get?type=http&country=ES",
    "https://www.proxy-list.download/api/v1/get?type=https&country=ES",
    "https://www.proxy-list.download/api/v1/get?type=socks4&country=ES",
    "https://www.proxy-list.download/api/v1/get?type=socks5&country=ES",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/ES_RAW.txt",
    "https://www.proxyscan.io/api/proxy?country=es&format=txt",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=es"
]

def check_geo(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=countryCode", timeout=5)
        return r.json().get('countryCode')
    except: return None

def check_alive(proxy):
    try:
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
        r = requests.get("http://clients3.google.com/generate_204", proxies=proxies, timeout=10)
        return r.status_code == 204
    except: return False

def diagnose():
    print("[DIAGNOSTIC] STARTING ES PROXY CHECK v2.2.14")
    all_candidates = set()
    
    for url in ES_SOURCES:
        try:
            print(f"[*] Testing source: {url[:60]}...")
            r = requests.get(url, timeout=10)
            found = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', r.text)
            print(f"   -> Found {len(found)} raw candidates.")
            all_candidates.update(found)
        except Exception as e:
            print(f"   -> ERROR: {e}")

    print(f"\n[STATS] Total unique candidates: {len(all_candidates)}")
    
    if not all_candidates:
        print("[!] NO CANDIDATES FOUND IN ANY SOURCE.")
        return

    # Filter a sample for Geo & Alive
    sample = list(all_candidates)[:20]
    print(f"\n[TEST] Verifying sample of {len(sample)} IPs...")
    
    valid_es = 0
    alive_es = 0
    
    for p in sample:
        ip = p.split(':')[0]
        cc = check_geo(ip)
        print(f"   IP: {ip} | Country: {cc}")
        if cc == 'ES':
            valid_es += 1
            if check_alive(p):
                print(f"      [OK] ALIVE AND ES!")
                alive_es += 1
            else:
                print(f"      [X] DEAD")
        else:
            print(f"      [-] NOT SPAIN")

    print(f"\n[RESULTS] SAMPLE SUMMARY:")
    print(f"   - Real ES %: {valid_es/len(sample)*100 if len(sample)>0 else 0}%")
    print(f"   - Alive ES %: {alive_es/len(sample)*100 if len(sample)>0 else 0}%")

if __name__ == "__main__":
    diagnose()
