import sys
import os
import time

# Ensure we can import from core/services
sys.path.append(os.getcwd())

from core.osint import OSINTManager
from services.manager import BrowserManager

def test_lookup(phone):
    print(f"--- 🕵️‍♂️ PRUEBA DE OSINT GOD MODE PARA: {phone} ---")
    print("Iniciando navegador visible para depuración...")
    
    # Use visible browser so the user can see what's happening
    mgr = BrowserManager(headless=False) 
    driver = mgr.get_driver()
    
    try:
        osint = OSINTManager()
        
        target_phone = phone # Target provided by user
    
        hint = input(f"¿Tienes una sospecha del nombre para {target_phone}? (Tu nombre sospechoso / Enter para saltar): ").strip()
        if not hint: hint = None
        
        print("\n" + "="*50)
        print(f"🔎 INICIANDO ESCANEO OSINT EXTREMO: {target_phone} " + (f"(Guiado: {hint})" if hint else ""))
        print("="*50 + "\n")
        
        report = osint.lookup(driver, target_phone, name_hint=hint)
        
        print("\n" + "█"*50)
        print("      RESULTADO DEL INFORME FINAL")
        print("█"*50)
        print(osint.format_report(report))
        print("█"*50)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"❌ CRASH: {e}")
    finally:
        print("\nCerrando en 5 segundos...")
        time.sleep(5)
        mgr.close()

if __name__ == "__main__":
    # Allow command line arg or input
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = input("Introduce número a investigar (Ej: 600123456): ").strip()
    
    if not target: target = "666111222"
    test_lookup(target)
