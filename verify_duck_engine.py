from core.duck_engine import DuckEngine
import time

def test_duck():
    print("Testing DuckEngine with a known spam number...")
    res = DuckEngine.search_parallel(["site:listaspam.com \"666111222\""], max_workers=1)
    print(f"Results: {len(res)}")
    for r in res:
        print(r)

    print("\nTesting DuckEngine with a generic term...")
    res2 = DuckEngine.search_parallel(["test"], max_workers=1)
    print(f"Results: {len(res2)}")

if __name__ == "__main__":
    test_duck()
