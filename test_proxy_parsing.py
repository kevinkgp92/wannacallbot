import os
import sys

# Mock BrowserManager to test the parsing logic
class MockBrowserManager:
    def _parse_proxy_string(self, proxy_str):
        if not proxy_str: return None, None, None
        
        proto = "http"
        actual_proxy = proxy_str
        tier = None
        
        if "|" in actual_proxy:
            parts = actual_proxy.split("|")
            if len(parts) == 3:
                proto = parts[0]
                actual_proxy = parts[1]
                tier = parts[2]
            elif len(parts) == 2:
                if ":" in parts[0]:
                    actual_proxy = parts[0]
                    tier = parts[1]
                else:
                    proto = parts[0]
                    actual_proxy = parts[1]
        
        try:
            if ":" in actual_proxy:
                host, port = actual_proxy.split(":", 1)
                if "|" in port:
                    port = port.split("|")[0]
            else:
                host, port = actual_proxy, "80"
        except:
            host, port = actual_proxy, "80"
            
        return proto, actual_proxy, (host, port)

def test():
    bm = MockBrowserManager()
    test_cases = [
        ("1.2.3.4:80", ("http", "1.2.3.4:80", ("1.2.3.4", "80"))),
        ("1.2.3.4:80|SILVER", ("http", "1.2.3.4:80", ("1.2.3.4", "80"))),
        ("socks5|1.2.3.4:1080", ("socks5", "1.2.3.4:1080", ("1.2.3.4", "1080"))),
        ("socks5|1.2.3.4:1080|GOLDEN", ("socks5", "1.2.3.4:1080", ("1.2.3.4", "1080"))),
        ("http|5.6.7.8:3128|BRONZE", ("http", "5.6.7.8:3128", ("5.6.7.8", "3128"))),
    ]
    
    passed = 0
    for inp, expected in test_cases:
        res = bm._parse_proxy_string(inp)
        if res == expected:
            print(f"✅ PASS: {inp} -> {res}")
            passed += 1
        else:
            print(f"❌ FAIL: {inp} -> Got {res}, expected {expected}")
            
    if passed == len(test_cases):
        print("\n✨ All tests passed!")
    else:
        print(f"\n⚠️ {len(test_cases) - passed} tests failed.")

if __name__ == "__main__":
    test()
