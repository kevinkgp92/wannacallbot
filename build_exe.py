import os
import subprocess
import shutil
import time
import sys

def kill_process_by_name(name):
    try:
        if sys.platform == "win32":
            subprocess.run(["taskkill", "/F", "/IM", name, "/T"], capture_output=True)
    except:
        pass

def clean_folder(folder):
    if not os.path.exists(folder):
        return folder
    print(f"   - Intentando limpiar {folder}...")
    try:
        shutil.rmtree(folder)
        print(f"   ✅ {folder} eliminado.")
        return folder
    except Exception:
        print(f"   [!] {folder} esta bloqueado. Usando carpeta alternativa...")
        new_folder = f"{folder}_{int(time.time())}"
        return new_folder

def build():
    print("===================================================")
    print("    WANNA CALL? - EXE BUILDER (PyInstaller)")
    print("===================================================")
    
    print("\n[0/3] Matando procesos activos...")
    kill_process_by_name("WannaCall*")
    kill_process_by_name("python.exe")
    kill_process_by_name("py.exe")
    
    print("\n[1/3] Preparando carpetas...")
    dist_folder = clean_folder("dist")
    build_folder = clean_folder("build")

    # Define files to include
    to_include = [
        "carnerosbot_logo.png;.",
        "logo_v3.png;.",
        "icon.ico;.",
        "logo_v3.ico;.",
        "version.txt;.",
        "requirements.txt;.",
        "CHANGELOG.md;."
    ]

    add_data_flags = []
    for item in to_include:
        src = item.split(';')[0]
        if os.path.exists(src):
            add_data_flags.extend(["--add-data", item])

    icon_file = "logo_v3.ico" if os.path.exists("logo_v3.ico") else "icon.ico"

    print("\n[2/3] Iniciando PyInstaller (Esto puede tardar)...")
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--icon", icon_file,
        "--name", f"WannaCall_v2.2.9",
        "--distpath", dist_folder,
        "--workpath", build_folder,
        "--clean"
    ]
    
    cmd.extend(add_data_flags)
    cmd.append("gui.py")

    try:
        print(f"Comando: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
        
        if result.returncode == 0:
            print("\n[3/3] EXITO: CONSTRUCCION COMPLETADA")
            # In --onefile mode, the EXE is directly in the dist folder
            exe_path = os.path.abspath(os.path.join(dist_folder, "WannaCall_v2.2.9.exe"))
            print(f"\nUbicacion: {exe_path}")
            
            # Copy to root
            try:
                shutil.copy2(exe_path, os.path.join(os.getcwd(), "WannaCall_v2.2.9_PORTABLE.exe"))
                print(f"✅ Copiado a la raiz: {os.path.join(os.getcwd(), 'WannaCall_v2.2.9_PORTABLE.exe')}")
            except Exception as e:
                print(f"⚠️ No se pudo copiar a la raiz: {e}")
                
        else:
            print(f"\nERROR: PyInstaller fallo con codigo {result.returncode}")
            print(result.stderr[-500:])
    except Exception as e:
        print(f"\nERROR DURANTE LA CONSTRUCCION: {e}")

if __name__ == "__main__":
    build()
