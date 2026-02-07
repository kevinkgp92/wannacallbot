import os
import subprocess
import time
import shutil
import glob

def get_version():
    try:
        with open("version.txt", "r") as f:
            return f.read().strip()
    except:
        return "2.2.49"

def build():
    version = get_version()
    print("===================================================")
    print(f"    WANNA CALL? - EXE BUILDER (v{version})")
    print("===================================================")
    
    # [NUCLEAR CLEANUP] v2.2.35: Aggressive purge and process kill
    print("\n[CLEANUP] Preparando espacio de trabajo...")
    
    # Kill processes
    subprocess.run("taskkill /F /IM geckodriver.exe /T", shell=True, capture_output=True)
    subprocess.run("taskkill /F /IM chromedriver.exe /T", shell=True, capture_output=True)
    # v2.2.45: NO LONGER KILLING BROWSER PROCESSES (Chrome/Firefox)
    # Only kill previous versions of the bot if needed
    subprocess.run("taskkill /F /IM WannaCall_v*.exe /T", shell=True, capture_output=True)
    time.sleep(1)

    # Remove old builds/dist
    for folder in glob.glob("build_*") + glob.glob("dist_*") + ["build", "dist"]:
        try:
            if os.path.exists(folder):
                shutil.rmtree(folder)
        except: pass

    # Remove old EXEs
    for old_exe in glob.glob("WannaCall_v*.exe"):
        try:
            os.remove(old_exe)
            print(f"  - Borrado: {old_exe}")
        except Exception as e:
            print(f"  - No se pudo borrar {old_exe} (Continuando...)")

    # Remove specs/logs
    for f in glob.glob("*.spec") + glob.glob("*.log"):
        try: os.remove(f)
        except: pass

    timestamp = int(time.time())
    dist_path = f"dist_{timestamp}"
    build_path = f"build_{timestamp}"
    if not os.path.exists(dist_path): os.makedirs(dist_path)

    print("\n[1/2] Iniciando PyInstaller (Esto puede tardar)...")
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
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("\n[2/2] EXITO: CONSTRUCCION COMPLETADA")
        exe_path = os.path.join(dist_path, f"WannaCall_v{version}.exe")
        portable_name = f"WannaCall_v{version}_PORTABLE.exe"
        if os.path.exists(exe_path):
            shutil.copy(exe_path, portable_name)
            print(f"\nBinario listo: {portable_name}")
    else:
        print("\n[!] ERROR EN LA COMPILACION")

if __name__ == "__main__":
    build()
