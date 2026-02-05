import requests
import re
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
import time
import random

class DuckEngine:
    """
    Lightweight, No-Browser Search Engine using DuckDuckGo HTML version.
    Designed for high-speed parallel dorking.
    """
    
    BASE_URL = "https://html.duckduckgo.com/html/"
    
    # Rotation of lightweight User-Agents to avoid immediate block (though DDG is lenient)
    UAS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ]

    @staticmethod
    def _search_worker(query, max_results=5):
        try:
            headers = {
                "User-Agent": random.choice(DuckEngine.UAS),
                "Referer": "https://duckduckgo.com/"
            }
            data = {'q': query}
            
            # Request valid for ~5 seconds
            resp = requests.post(DuckEngine.BASE_URL, data=data, headers=headers, timeout=5)
            
            if resp.status_code == 200:
                results = []
                # Simple Regex Scraping for DDG HTML
                # Pattern for result snippets
                # This scrapes the 'result__a' class which is the title link
                link_pattern = re.compile(r'<a class="result__a" href="([^"]+)">([^<]+)</a>')
                snippet_pattern = re.compile(r'<a class="result__snippet" href="[^"]+">([^<]+)</a>')
                
                # We split by 'result__body' to keep context? 
                # Easier: Find all titles, they usually align with snippets sequentially.
                
                links = link_pattern.findall(resp.text)
                # snippets = snippet_pattern.findall(resp.text) # Snippets are harder in Regex, titles are usually enough for OSINT relevance
                
                for i, match in enumerate(links[:max_results]):
                    raw_url = match[0]
                    title = match[1]
                    
                    # DDG HTML urls are encoded in /l/?kh=-1&uddg=...
                    # We need to decode them
                    if "/l/?kh" in raw_url or "uddg=" in raw_url:
                        try:
                            # Extract actual URL from uddg param
                            parsed = urllib.parse.urlparse(raw_url)
                            qs = urllib.parse.parse_qs(parsed.query)
                            if 'uddg' in qs:
                                clean_url = qs['uddg'][0]
                            else:
                                clean_url = raw_url
                        except:
                            clean_url = raw_url
                    else:
                        clean_url = raw_url

                    # HTML Entity Decode for Title
                    clean_title = title.replace("<b>", "").replace("</b>", "").replace("&amp;", "&").replace("&#x27;", "'").replace("&quot;", '"')
                    
                    results.append({
                        "title": clean_title,
                        "url": clean_url,
                        "source": "DuckDuckGo"
                    })
                return results
            elif resp.status_code == 403:
                print("⚠️ DDG Rate Limit (403)")
                return []
            else:
                return []
        except Exception as e:
            # print(f"DDG Error: {e}")
            return []

    @staticmethod
    def search_parallel(dorks, max_workers=10):
        """
        Runs multiple dorks in parallel using threads.
        dorks: List of query strings.
        Returns: list of all results flattened.
        """
        all_results = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_dork = {executor.submit(DuckEngine._search_worker, d): d for d in dorks}
            
            for future in concurrent.futures.as_completed(future_to_dork):
                try:
                    data = future.result()
                    if data:
                        all_results.extend(data)
                except:
                    pass
        return all_results
