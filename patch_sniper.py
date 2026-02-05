import os

file_path = r'c:\Users\kevin\Downloads\perubianbot\core\osint.py'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    # We want to replace from line 460 to line 474 (1-indexed)
    # The header was already updated in the previous step.
    if i+1 >= 460 and i+1 <= 474:
        if i+1 == 460:
            # Insert the new code here
            new_lines.append('\n')
            new_lines.append('        def mine_snippets_deep(source_name, query_str):\n')
            new_lines.append('            try:\n')
            new_lines.append('                browser.get(f"https://www.google.com/search?q={query_str}")\n')
            new_lines.append('                time.sleep(2.5)\n')
            new_lines.append('                try:\n')
            new_lines.append('                    btns = browser.find_elements(By.TAG_NAME, "button")\n')
            new_lines.append('                    for b in btns:\n')
            new_lines.append('                        if any(x in b.text.lower() for x in ["acepto", "agree", "aceptar", "accept"]):\n')
            new_lines.append('                            b.click(); time.sleep(1); break\n')
            new_lines.append('                except: pass\n')
            new_lines.append('\n')
            new_lines.append('                results = browser.find_elements(By.CSS_SELECTOR, "div.g, .v7W49e")\n')
            new_lines.append('                for res in results[:4]:\n')
            new_lines.append('                    text = res.text\n')
            new_lines.append('                    emails = re.findall(r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,})", text)\n')
            new_lines.append('                    for em in emails:\n')
            new_lines.append('                        if em.lower() not in report[\'intel\'][\'email\']:\n')
            new_lines.append('                            report[\'intel\'][\'email\'].append(em.lower())\n')
            new_lines.append('                            print(f"  📧 Email Encontrado: {em}")\n')
            new_lines.append('\n')
            new_lines.append('                    found_nicks = re.findall(r"(?:nick|user|handle|alias|@|es:)\\s*[:]?\\s*([a-zA-Z0-9_]{4,20})", text, re.IGNORECASE)\n')
            new_lines.append('                    for n in found_nicks:\n')
            new_lines.append('                        if is_clean_name(n, is_nick=True):\n')
            new_lines.append('                            report[\'intel\'][\'social\'].append(f"{source_name}: @{n}")\n')
            new_lines.append('                            print(f"  🆔 Handle/Nick: @{n}")\n')
            new_lines.append('\n')
            new_lines.append('                    name_ctx = re.search(r"(?:por|Name|Nombre|Propietario|Vendedor)[:\\s]+([a-zA-Z\\s]{5,25})", text, re.IGNORECASE)\n')
            new_lines.append('                    if name_ctx:\n')
            new_lines.append('                        nm = name_ctx.group(1).strip()\n')
            new_lines.append('                        if is_clean_name(nm):\n')
            new_lines.append('                            report[\'intel\'][\'personal\'].append(nm)\n')
            new_lines.append('                            print(f"  👤 Nombre Contextual: {nm}")\n')
            new_lines.append('            except: pass\n')
            new_lines.append('\n')
            new_lines.append('        for fmt in formats:\n')
            new_lines.append('            mine_snippets_deep("Social", f"\\"{fmt}\\" (site:instagram.com OR site:facebook.com OR site:twitter.com)")\n')
            new_lines.append('            mine_snippets_deep("Mercado", f"\\"{fmt}\\" (site:wallapop.com OR site:vinted.es OR site:milanuncios.com)")\n')
            new_lines.append('            mine_snippets_deep("Prof", f"\\"{fmt}\\" (site:github.com OR site:linkedin.com)")\n')
            new_lines.append('            mine_snippets_deep("Fuga", f"\\"{fmt}\\" (site:pastebin.com OR site:controlc.com)")\n')
            new_lines.append('\n')
        continue
    new_lines.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Successfully installed Sniper Engine in core/osint.py")
