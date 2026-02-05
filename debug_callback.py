
import re

file_path = r"c:\Users\kevin\Downloads\perubianbot\core\osint.py"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Searching {len(lines)} lines in {file_path}...")
for i, line in enumerate(lines, 1):
    if "progress_callback" in line:
        print(f"Line {i}: {line.strip()}")
