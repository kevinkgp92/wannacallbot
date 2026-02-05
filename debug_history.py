import json
import os
import sys

# Path to history file (adjust if needed)
HISTORY_PATH = r"C:\Users\kevin\Downloads\perubianbot\dist\history.json"

def inspect_history():
    print(f"--- INSPECTING HISTORY: {HISTORY_PATH} ---")
    if not os.path.exists(HISTORY_PATH):
        print("File does not exist!")
        return

    try:
        with open(HISTORY_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        print(f"JSON Loaded. Total Protected Numbers: {len(data)}")
        print("-" * 30)
        
        for phone, services in data.items():
            print(f"Phone: {phone}")
            print(f"Services ({len(services)}): {services}")
            print("-" * 30)
            
    except Exception as e:
        print(f"Error reading JSON: {e}")

if __name__ == "__main__":
    inspect_history()
