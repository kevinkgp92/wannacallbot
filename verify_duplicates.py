import sys
import os

# Add the project root to sys.path
sys.path.append(os.getcwd())

from services.manager import ServiceManager

def check_duplicates():
    user_data = {
        'name': 'Test',
        'surname': 'User',
        'email': 'test@example.com',
        'phone': '600000000',
        'zipcode': '28001'
    }
    
    manager = ServiceManager(user_data)
    
    names = [s.name for s in manager.services]
    unique_names = set(names)
    
    print(f"Total services registered: {len(names)}")
    print(f"Unique services: {len(unique_names)}")
    
    if len(names) != len(unique_names):
        print("\n[!] DUPLICATES FOUND:")
        seen = set()
        for name in names:
            if name in seen:
                print(f"Duplicate: {name}")
            seen.add(name)
    else:
        print("\n[SUCCESS] No duplicates found.")
        
    print("\nFull list of services:")
    for i, name in enumerate(sorted(names), 1):
        print(f"{i}. {name}")

    manager.browser_manager.close()

if __name__ == "__main__":
    check_duplicates()
