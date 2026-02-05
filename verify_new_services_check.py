
import sys
import os

# Ensure we can import from current directory
sys.path.append(os.getcwd())

try:
    from services.manager import ServiceManager
    print("Successfully imported ServiceManager.")
    
    # Mock user data
    user_data = {
        'name': 'Test',
        'surname': 'User',
        'email': 'test@example.com',
        'phone': '600000000',
        'zipcode': '28001'
    }
    
    manager = ServiceManager(user_data)
    print(f"ServiceManager instantiated with {len(manager.services)} services.")
    
    expected_new = ['ADT', 'Sector Alarm', 'Holaluz', 'Axa', 'Lowi', 'UNIR']
    found_new = []
    
    print("\n--- Listing All Services ---")
    for s in manager.services:
        print(f"- {s.name} ({s.url})")
        if s.name in expected_new:
            found_new.append(s.name)
            
    print("\n--- Verification Results ---")
    if len(found_new) == len(expected_new):
        print("SUCCESS: All 6 new services found.")
    else:
        print(f"WARNING: Found {len(found_new)}/{len(expected_new)} new services.")
        missing = set(expected_new) - set(found_new)
        print(f"Missing: {missing}")

except ImportError as e:
    print(f"CRITICAL: Import Error - {e}")
except Exception as e:
    print(f"CRITICAL: Runtime Error - {e}")
