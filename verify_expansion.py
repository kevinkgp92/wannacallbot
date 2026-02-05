from services.manager import ServiceManager
from services.definitions.expansion_v2 import VertiService, SicorService, AutoSolarService, RacesService

# Fake data for testing
user_data = {
    'phone': '600123456',
    'name': 'Test User',
    'lastname': 'Test Lastname',
    'email': 'test@example.com',
    'zip': '28001'
}

print("--- VERIFICACIÓN DE EXPANSIÓN V2 ---")

# Initialize manager
mgr = ServiceManager(user_data, force_chrome=False)

# Check if new services are in the list
new_service_names = ["Verti Seguros", "Sicor Alarmas", "AutoSolar", "RACE"]
found_count = 0

print("\n[Check 1] Discovery check:")
for s in mgr.services:
    if s.name in new_service_names:
        print(f"✅ Found: {s.name}")
        found_count += 1

if found_count == 4:
    print("\n✅ All 4 new services discovered successfully.")
else:
    print(f"\n❌ Only found {found_count}/4 services.")

print("\nDone.")
