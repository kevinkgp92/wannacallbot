import sys
import os
import pkgutil
import importlib
import inspect

# Add current dir to path
sys.path.append(os.getcwd())

from services.base_service import BaseService

def test_discovery():
    print("--- TESTING SERVICE DISCOVERY ---")
    import services.definitions as definitions
    paths = getattr(definitions, '__path__', [])
    
    # Add local path logic
    local_path = os.path.join(os.getcwd(), "services", "definitions")
    if os.path.exists(local_path) and local_path not in paths:
        paths.append(local_path)
    
    print(f"Paths: {paths}")
    
    found = []
    for loader, module_name, is_pkg in pkgutil.iter_modules(paths):
        if module_name == "__init__": continue
        full_module_name = f"services.definitions.{module_name}"
        try:
            module = importlib.import_module(full_module_name)
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, BaseService) and obj is not BaseService:
                    found.append(f"{module_name}.{name}")
        except Exception as e:
            print(f"Error loading {full_module_name}: {e}")
            
    print(f"\nFinal list of discovered services ({len(found)}):")
    for f in sorted(found):
        if "nocturno_plus" in f:
            print(f" -> {f}")
        else:
            # Shorten others
            pass

if __name__ == "__main__":
    test_discovery()
