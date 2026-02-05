import json
import os

# The number to block/mark as done
PHONE = "658771582"

# List of all service names (must match self.name in code)
SERVICES = [
    "Securitas Direct",
    "Prosegur",
    "MasMovil Alarmas",
    "Endesa",
    "Naturgy",
    "Iberdrola",
    "Línea Directa",
    "Pelayo",
    "Mapfre",
    "Genesis",
    "Euroinnova",
    "Jazztel",
    "Yoigo",
    "O2",
    "Simyo",
    "Racctel+",
    "Vodafone",
    "Euskaltel",
    "MásMóvil/Ford"
]

target_dir = os.path.join(os.getcwd(), 'dist')
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

file_path = os.path.join(target_dir, 'history.json')

# Load existing if any
data = {}
if os.path.exists(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except: pass

# Add phone entry
if PHONE not in data:
    data[PHONE] = []

# Add all services
for s in SERVICES:
    if s not in data[PHONE]:
        data[PHONE].append(s)

# Save
with open(file_path, 'w') as f:
    json.dump(data, f, indent=4)

print(f"[OK] Historial generado en: {file_path}")
print(f"[OK] El numero {PHONE} ha sido marcado como COMPLETADO en {len(SERVICES)} servicios.")
print(f"[OK] Al ejecutar el bot, este numero sera SALTADO automaticamente.")
