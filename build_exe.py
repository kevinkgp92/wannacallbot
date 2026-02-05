import os
import subprocess
import shutil
import sys

def build():
    print("===================================================")
    print("    WANNA CALL? - EXE BUILDER (PyInstaller)")
    print("===================================================")
    print("\n[1/3] Limpiando carpetas de construcción...")
    
    if os.path.exists("dist"): shutil.rmtree("dist")
    if os.path.exists("build"): shutil.rmtree("build")

    # Define files to include
    # Format: "source;destination" (Windows)
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
        if os.path.exists(item.split(';')[0]):
            add_data_flags.extend(["--add-data", item])

    icon_file = "logo_v3.ico" if os.path.exists("logo_v3.ico") else "icon.ico"

    print("\n[2/3] Iniciando PyInstaller (Esto puede tardar unos minutos)...")
    
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onedir", # Using onedir for faster startup, onefile is slow for large apps
        "--windowed",
        "--icon", icon_file,
        "--name", "WannaCall_v2.2.7",
        "--clean"
    ]
    
    cmd.extend(add_data_flags)
    cmd.append("gui.py")

    try:
        subprocess.run(cmd, check=True)
        print("\n[3/3] ¡CONSTRUCCIÓN COMPLETADA!")
        print(f"\n✅ Tu ejecutable está listo en: {os.path.abspath('dist/WannaCall_v2.2.7/WannaCall_v2.2.7.exe')}")
        print("\nNOTA: Se ha creado en modo 'Carpeta' para que abra AL INSTANTE.")
        print("Si quieres pasarlo a alguien, comprime la carpeta 'WannaCall_v2.2.7' en un .zip")
    except Exception as e:
        print(f"\n❌ ERROR DURANTE LA CONSTRUCCIÓN: {e}")

if __name__ == "__main__":
    build()
