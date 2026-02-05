import os
import subprocess
import time
import shutil
import glob

def build():
    version = "2.2.23"
    print("===================================================")
    print(f"    WANNA CALL? - EXE BUILDER (v{version})")
    print("===================================================")
    
    print("\n[NUCLEAR CLEANUP] Iniciando limpieza de espacio de trabajo...")
    # Remove all .spec files
    for spec in glob.glob("*.spec"):
        try:
            os.remove(spec)
            print(f"  🗑️ Borrado: {spec}")
        except: pass
    
    # Remove build and dist folders
    for folder in glob.glob("build_*") + glob.glob("dist_*") + ["build", "dist"]:
        try:
            if os.path.exists(folder):
                shutil.rmtree(folder)
                print(f"  🗑️ Purga: {folder}")
        except: pass
    
    timestamp = int(time.time())
    dist_path = f"dist_{timestamp}"
    build_path = f"build_{timestamp}"
    
    print("\n[0/3] Matando procesos activos...")
    os.system("taskkill /F /IM WannaCall_v*.exe /T")
    
    print("\n[1/3] Preparando carpetas...")
    if not os.path.exists(dist_path): os.makedirs(dist_path)
    
    print("\n[2/3] Iniciando PyInstaller (Esto puede tardar)...")
    cmd = [
        "python", "-m", "PyInstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--icon", "logo_v3.ico",
        "--name", f"WannaCall_v2.2.23",
        "--distpath", dist_path,
        "--workpath", build_path,
        "--clean",
        "--add-data", "wannacallbot_logo.png;.",
        "--add-data", "logo_v3.png;.",
        "--add-data", "icon.ico;.",
        "--add-data", "logo_v3.ico;.",
        "--add-data", "version.txt;.",
        "--add-data", "requirements.txt;.",
        "--add-data", "CHANGELOG.md;.",
        "gui.py"
    ]
    
    print(f"Comando: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("\n[3/3] EXITO: CONSTRUCCION COMPLETADA")
        exe_path = os.path.join(dist_path, f"WannaCall_v2.2.23.exe")
        final_name = "WannaCall_v2.2.23_PORTABLE.exe"
        if os.path.exists(exe_path):
            # Atomic swap
            if os.path.exists(final_name): os.remove(final_name)
            shutil.copy(exe_path, final_name)
            print(f"\nUbicacion: {os.path.abspath(exe_path)}")
        else:
            print(f"\nError: No se encontro {exe_path}")
    else:
        print("\n[!] ERROR EN LA COMPILACION")

if __name__ == "__main__":
    build()
