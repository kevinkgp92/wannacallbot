import os

file_path = r'c:\Users\kevin\Downloads\perubianbot\core\osint.py'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# We want to remove lines 460 to 478 (1-indexed: 460-478)
# In 0-indexed: index 459 to 477 inclusive.
# Looking at the view output:
# 459: 
# 460: 
# 461: ...
# 478:         except: pass

# I'll be more surgical. I'll search for the bad lines and remove them.
new_lines = []
skip = False
for i, line in enumerate(lines):
    # Line numbers in view_file are 1-indexed.
    # 460 to 478 are the ones we saw as mess.
    if i+1 >= 460 and i+1 <= 478:
        continue
    new_lines.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Successfully cleaned core/osint.py")
