import os
import subprocess
import time
import shutil

def build():
    version = "2.2.15"
    print("===================================================")
    print(f"    WANNA CALL? - EXE BUILDER (v{version})")
    print("===================================================")

    # 0. Kill active processes
    print("\n[0/3] Matando procesos activos...")
    subprocess.run('taskkill /F /IM "WannaCall*" /T 2>nul', shell=True)
    subprocess.run('taskkill /F /IM "python.exe" /T 2>nul', shell=True)
    time.sleep(2)

    # 1. Folders
    print("\n[1/3] Preparando carpetas...")
    dist_path = f"dist_{int(time.time())}"
    build_path = f"build_{int(time.time())}"
    
    # 2. PyInstaller
    print("\n[2/3] Iniciando PyInstaller (Esto puede tardar)...")
    cmd = [
        "python", "-m", "PyInstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--icon", "logo_v3.ico",
        "--name", f"WannaCall_v2.2.15",
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
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("\n[3/3] EXITO: CONSTRUCCION COMPLETADA")
        exe_path = os.path.join(dist_path, f"WannaCall_v2.2.15.exe")
        final_name = "WannaCall_v2.2.15_PORTABLE.exe"
        if os.path.exists(exe_path):
            shutil.copy(exe_path, final_name)
            print(f"\nUbicacion: {os.path.abspath(exe_path)}")
    else:
        print(f"\n[!] ERROR DURANTE LA CONSTRUCCION: {result.stderr}")

if __name__ == "__main__":
    build()
