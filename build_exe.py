import os
import subprocess
import time
import shutil
import glob

def build():
    version = "2.2.34"
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
    for folder in ["build", "dist"]:
        try:
            if os.path.exists(folder):
                shutil.rmtree(folder)
                print(f"  🗑️ Purga: {folder}")
        except: pass
    
    timestamp = int(time.time())
    dist_path = f"dist_{timestamp}"
    # [NUCLEAR CLEANUP] v2.2.34: Kill legacy processes and purge ALL old EXEs
    print("\n[NUCLEAR CLEANUP] Iniciando limpieza de espacio de trabajo...")
    
    print("\n[0/3] Matando procesos activos...")
    subprocess.run("taskkill /F /IM geckodriver.exe /T", shell=True, capture_output=True)
    subprocess.run("taskkill /F /IM chromedriver.exe /T", shell=True, capture_output=True)
    subprocess.run("taskkill /F /IM WannaCall_v*.exe /T", shell=True, capture_output=True)

    print("\n[PURGA NUCLEAR] Eliminando versiones anteriores del directorio...")
    for old_exe in glob.glob("WannaCall_v*.exe"):
        try:
            # Don't delete our own target name if it exists somehow, or just kill all
            os.remove(old_exe)
            print(f"  ✅ Borrado: {old_exe}")
        except Exception as e:
            print(f"  [ERROR] No se pudo borrar {old_exe}: {e}")

    # Remove specs and logs
    for f in glob.glob("*.spec"): os.remove(f)
    for f in glob.glob("*.log"): 
        try: os.remove(f)
        except: pass

    print("\n[1/3] Preparando carpetas...")
    if not os.path.exists(dist_path): os.makedirs(dist_path)
    
    print("\n[2/3] Iniciando PyInstaller (Esto puede tardar)...")
    cmd = [
        "python", "-m", "PyInstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--icon", "logo_v3.ico",
        "--name", f"WannaCall_v{version}",
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
        exe_path = os.path.join(dist_path, f"WannaCall_v{version}.exe")
        final_name = f"WannaCall_v{version}_PORTABLE.exe"
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
