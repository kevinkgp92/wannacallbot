import os
import subprocess
import sys
import shutil
import time
# ... imports ...
import errno
import stat

# Ensure logs are written even if stdout is lost
LOG_FILE = os.path.abspath("build_log.txt")

def force_log(msg):
    """Writes to log file immediately."""
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(msg + "\n")
    except: pass

def log(msg, end="\n"):
    print(msg, end=end)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(msg + end)
    except: pass

def handle_remove_readonly(func, path, exc):
    excvalue = exc[1]
    if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    else:
        raise

def kill_existing_process(exe_name="WannaCall_Pro.exe"):
    print(f"[STATUS] Asegurando que {exe_name} esté cerrado...")
    
    # 1. Send Kill Signal
    try:
        subprocess.run(f"taskkill /F /T /IM {exe_name}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except: pass
    
    # 2. WAIT and DELETE loop
    max_retries = 20 # 10 seconds
    target_file = os.path.abspath(f"dist/{exe_name}")
    
    if os.path.exists(target_file):
        print(f"[WAIT] Esperando liberación para eliminar archivo...")
        for i in range(max_retries):
            try:
                if os.path.exists(target_file):
                    os.remove(target_file)
                print(f"[OK] Archivo eliminado previniendo bloqueos.")
                return
            except OSError:
                # Still locked
                time.sleep(0.5)
                # Retry kill
                try: subprocess.run(f"taskkill /F /T /IM {exe_name}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except: pass
        
        print("[WARN] No se pudo eliminar el archivo. Es probable que falle el build.")

def build():
    kill_existing_process() # Force close app before build
    # Reset log
    if os.path.exists(LOG_FILE):
        try: os.remove(LOG_FILE)
        except: pass

    # Enforce UTF-8 for stdout if possible
    try:
        if sys.stdout.encoding.lower() != 'utf-8':
            sys.stdout.reconfigure(encoding='utf-8')
    except: pass

    log("[START] NUCLEAR BUILD ENGINE v2.2 (ASCII MODE)")
    log(f"[INFO] Root Directory: {os.getcwd()}")
    log(f"[INFO] Target Script: {os.path.abspath(__file__)}")
    log("===================================================")

    # 1. Constants
    EXE_NAME = "WannaCall_Pro"
    MAIN_SCRIPT = "gui.py"
    ICON_PATH = "icon.ico"
    LOGO_PATH = "carnerosbot_logo.png"

    # 2. Resolve Python
    py_path = sys.executable
    log(f"[INFO] Python Engine: {py_path}")

    # SAFETY CHECK: Block Python 3.13 (Windows Store version is broken)
    if sys.version_info >= (3, 13):
        log("\n[⛔ ERROR FATAL] ESTÁS USANDO PYTHON 3.13 (VERSIÓN ROTA DE MICROSOFT).")
        log("ESTA VERSIÓN GENERA EJECUTABLES CORRUPTOS (ERROR DLL).")
        log("SOLUCIÓN: Ejecuta 'INSTALL_PYTHON_FIX.bat' y REINICIA el PC la instalación termine.")
        log("Si ya lo hiciste, asegúrate de lanzar el bot con el Python correcto.")
        sys.exit(1)
        
    log(f"[OK] Versión de Python detectada: {sys.version_info.major}.{sys.version_info.minor} (Compatible)")
    
    # 3. Clean previous builds
    log("[STATUS] Limpiando residuos anteriores...")
    log("[PROGRESS] 10")
    for folder in ["build", "dist"]:
        if os.path.exists(folder):
            try:
                # Use robust error handler for Windows read-only/locked files
                shutil.rmtree(folder, ignore_errors=False, onerror=handle_remove_readonly)
            except Exception as e:
                # Retrying slightly if it failed
                time.sleep(1)
                try:
                    shutil.rmtree(folder, ignore_errors=True)
                except:
                    log(f"  [WARN] No se pudo eliminar {folder}: {e}")
                
                # Verify if critical file remains
                if folder == "dist" and os.path.exists(f"dist/{EXE_NAME}.exe"):
                     log("\n[FATAL] ACCESO DENEGADO A LA CARPETA 'dist'.")
                     log("CAUSA: Tienes el archivo 'WannaCall_Pro.exe' abierto o en uso.")
                     log("SOLUCIÓN: Cierra todas las ventanas del bot antiguo y reintenta.")
                     sys.exit(1)

    if os.path.exists(f"{EXE_NAME}.spec"):
        try: os.remove(f"{EXE_NAME}.spec")
        except: pass

    # 4. Generate EXE
    log("[STATUS] Compilando Binario Profesional...")
    log("[PROGRESS] 20")
    log("INFO: Iniciando PyInstaller...")
    
    # Base command
    cmd = [
        py_path, "-m", "PyInstaller",
        "--noconsole",
        "--onefile",
        "--noconfirm", 
        f"--name={EXE_NAME}",
        f"--icon={ICON_PATH}" if os.path.exists(ICON_PATH) else "",
        "--add-data", f"{LOGO_PATH};." if os.path.exists(LOGO_PATH) else "",
        "--add-data", "version.json;.",
        "--collect-all", "customtkinter",
        "--collect-all", "undetected_chromedriver",
        "--collect-all", "core",
        "--collect-all", "services",
        "--hidden-import", "core.osint",
        "--hidden-import", "services.manager",
        "--hidden-import", "phonenumbers",
        "--hidden-import", "selenium",
        "--paths", ".",
        MAIN_SCRIPT
    ]
    
    # Filter empty args
    cmd = [arg for arg in cmd if arg]
    
    try:
        log("--- PROGRESO DE COMPILACIÓN ---")
        log("[PROGRESS] 30")
        # shell=True is CRITICAL for Windows Store Python to find 'python' in Popen if used indirectly,
        # but here we use absolute path. However, PyInstaller spawning subprocesses might need it.
        # We also need to capture output.
        process = subprocess.Popen(cmd, 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.STDOUT, 
                                   text=True, 
                                   bufsize=1, 
                                   encoding="utf-8", 
                                   shell=True) # shell=True kept for safety with aliases
        
        for line in process.stdout:
            l = line.strip()
            if not l: continue
            log(f"  > {l}")
            
            # Simulated progress based on output
            if "INFO: Checking" in l: log("[PROGRESS] 40")
            if "INFO: Analysing" in l: log("[PROGRESS] 50")
            if "INFO: Collecting" in l: log("[PROGRESS] 60")
            if "INFO: Building" in l: log("[PROGRESS] 75")
            if "INFO: Appending archive" in l: log("[STATUS] Empaquetando EXE...")
            if "INFO: Appending archive" in l: log("[PROGRESS] 85")
            if "INFO: Building EXE" in l: log("[PROGRESS] 90")

        process.wait()
        if process.returncode != 0:
            raise RuntimeError(f"PyInstaller returned code {process.returncode}")
            
        log("\n✅ COMPILACIÓN DE NÚCLEO COMPLETADA.")
        
    except Exception as e:
        log(f"\n❌ ERROR CRÍTICO EN PYINSTALLER: {e}")
        sys.exit(1)

    # 5. Verify
    log("[3/3] Verificando resultado...")
    output_exe = os.path.join("dist", f"{EXE_NAME}.exe")
    if os.path.exists(output_exe):
        log(f"\n[EXITO] Binario generado en: {output_exe}")
        # Copy configs
        for cfg in ["targets.json", "version.json"]:
            if os.path.exists(cfg):
                shutil.copy(cfg, "dist")
        
        # Shortcut
        try:
            log("ℹ️ Creando acceso directo...")
            desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")
            shortcut_path = os.path.join(desktop, f"{EXE_NAME}.lnk")
            abs_target = os.path.abspath(output_exe)
            
            ps_script = f'$s=(New-Object -COM WScript.Shell).CreateShortcut("{shortcut_path}");$s.TargetPath="{abs_target}";$s.WorkingDirectory="{os.path.dirname(abs_target)}";$s.Save()'
            subprocess.run(["powershell", "-Command", ps_script], capture_output=True)
            log(f"✨ Acceso directo: {shortcut_path}")
        except Exception as e:
            log(f"⚠️ Error creando acceso directo: {e}")
    else:
        log("\n[ERROR] El binario no se generó.")
        sys.exit(1)

if __name__ == "__main__":
    try:
        build()
        sys.exit(0)
    except Exception as e:
        force_log(f"FATAL TOP-LEVEL ERROR: {e}")
        sys.exit(1)
