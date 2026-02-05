import sys
import subprocess
import importlib.util

def install(package):
    print(f"📦 Instalando {package}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--no-warn-script-location"])
        print(f"✅ {package} instalado correctamente.")
    except Exception as e:
        print(f"❌ Error instalando {package}: {e}")

def check_and_install():
    required = [
        "customtkinter", 
        "undetected-chromedriver", 
        "requests", 
        "pillow", 
        "packaging",
        "selenium",
        "phonenumbers"
    ]
    
    print("🔎 Verificando dependencias...")
    for package in required:
        try:
            # Handle package names vs import names
            import_name = package.replace("-", "_")
            if importlib.util.find_spec(import_name) is None:
                print(f"⚠️ Falta: {package}")
                install(package)
            else:
                print(f"OK: {package}")
        except ImportError:
            install(package)

if __name__ == "__main__":
    check_and_install()
    print("\n✅ Verificación completada.")
