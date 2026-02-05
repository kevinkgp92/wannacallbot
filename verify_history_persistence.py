from core.history import HistoryManager
import os

def test_history():
    print("Testing History Persistence...")
    test_phone = "123456789"
    test_service = "TestService"
    
    # Clean up before test
    hm = HistoryManager("test_history.json")
    if os.path.exists(hm.filename):
        os.remove(hm.filename)
    
    # 1. Verify empty
    hm = HistoryManager("test_history.json")
    if hm.is_registered(test_phone, test_service):
        print("FAIL: Should be empty initially")
        return

    # 2. Add record
    print("Adding record...")
    hm.add_record(test_phone, test_service)
    
    # 3. Verify in current instance
    if not hm.is_registered(test_phone, test_service):
        print("FAIL: Should be registered in current instance")
        return
        
    # 4. Verify persistence (new instance)
    print("Verifying persistence...")
    hm2 = HistoryManager("test_history.json")
    if not hm2.is_registered(test_phone, test_service):
        print("FAIL: Persistence failed (not found in new instance)")
    else:
        print("SUCCESS: Record persisted correctly")

    # Clean up
    if os.path.exists("test_history.json"):
        os.remove("test_history.json")

if __name__ == "__main__":
    test_history()
