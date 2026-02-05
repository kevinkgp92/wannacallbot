import os
import json
import sys
import subprocess
import requests
import time

# CONFIGURATION
# ==========================================
# Force UTF-8 for Windows Consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except: pass

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "") # SANITIZED
REPO_OWNER = "kevinkgp92"
REPO_NAME = "wannacallbot"
# ==========================================

VERSION_FILE = "version.json"
BUILD_SCRIPT = "build_pro.py"


# UTILITIES
# ==========================================
class ProgressBar:
    def __init__(self, total=100, prefix='', suffix='', decimals=1, length=50, fill='█'):
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.decimals = decimals
        self.length = length
        self.fill = fill
        self.iteration = 0
        self.start_time = time.time()

    def update(self, iteration, status=None):
        self.iteration = iteration
        percent = ("{0:." + str(self.decimals) + "f}").format(100 * (iteration / float(self.total)))
        filled_length = int(self.length * iteration // self.total)
        bar = self.fill * filled_length + '-' * (self.length - filled_length)
        
        stat_str = f"| {status}" if status else ""
        # Clear line and print bar
        sys.stdout.write(f'\r{self.prefix} |{bar}| {percent}% {self.suffix} {stat_str}')
        sys.stdout.flush()
        
    def complete(self):
        sys.stdout.write('\n')

def log(msg, temporary=False):
    """
    Classic log. If temporary=True, it uses \r to be overwritten.
    """
    if temporary:
        sys.stdout.write(f"\r[GOD MODE] {msg}")
        sys.stdout.flush()
    else:
        # Clear potential progress bar line
        sys.stdout.write("\r" + " " * 80 + "\r") 
        print(f"[GOD MODE] {msg}")

def bump_version():
    """Reads version.json, increments patch, and saves it."""
    if not os.path.exists(VERSION_FILE):
        log("❌ Error: No existe version.json")
        sys.exit(1)
        
    with open(VERSION_FILE, "r") as f:
        data = json.load(f)
    
    current_v = data.get("version", "1.0.0")
    major, minor, patch = map(int, current_v.split("."))
    
    # Increment patch
    new_v = f"{major}.{minor}.{patch + 1}"
    
    data["version"] = new_v
    with open(VERSION_FILE, "w") as f:
        json.dump(data, f, indent=4)
        
    log(f"📈 Versión incrementada: {current_v} -> {new_v}")
    return new_v

def run_build():
    """Runs the build script and checks for success with REAL TIME PROGRESS."""
    log("🔨 Iniciando compilación de núcleo...")
    
    # Progress Bar Instance
    pb = ProgressBar(total=100, prefix='BUILDING', length=40)
    
    cmd = [sys.executable, BUILD_SCRIPT]
    
    # Run with explicit UTF-8 and merge stderr
    # Run with explicit UTF-8 env to ensure build_pro.py outputs UTF-8
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUNBUFFERED"] = "1"
    
    process = subprocess.Popen(
        cmd, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT, 
        text=True, 
        encoding="utf-8", 
        errors="replace",
        bufsize=1,
        env=env
    )
    
    current_status = "Iniciando..."
    
    # Real-time output parsing
    while True:
        line = process.stdout.readline()
        if not line and process.poll() is not None:
            break
        
        if line:
            line = line.strip()
            # Parse hooks
            if "[PROGRESS]" in line:
                try:
                    val = int(line.replace("[PROGRESS]", "").strip())
                    pb.update(val, current_status)
                except: pass
            elif "[STATUS]" in line:
                current_status = line.replace("[STATUS]", "").strip()
                pb.update(pb.iteration, current_status)
            elif "[FATAL]" in line or "[ERROR]" in line:
                # Always print errors above bar
                sys.stdout.write("\r" + " " * 80 + "\r")
                print(f"❌ {line}")
            else:
                 # VERBOSE MODE: Print everything else to debug hangs
                 # Only print if it's not a known prefix and has content
                 if line and not line.startswith("["):
                     sys.stdout.write("\r" + " " * 80 + "\r")
                     print(f"  » {line}")
                     # Redraw bar immediately
                     pb.update(pb.iteration, current_status)
                 
    rc = process.poll()
    pb.complete()
    
    if rc != 0:
        log("❌ Error fatal en compilación. Revisa build_log.txt")
        sys.exit(1)
        
    # Verify file exists
    exe_path = os.path.join("dist", "WannaCall_Pro.exe")
    if not os.path.exists(exe_path):
        log("❌ Error: El compilador dijo OK, pero no veo el .exe")
        sys.exit(1)
        
    log("✅ Compilación exitosa.")
    return exe_path

class ProgressFileReader:
    def __init__(self, filename, progress_callback):
        self.f = open(filename, 'rb')
        self.filename = filename
        self.total_size = os.path.getsize(filename)
        self.read_so_far = 0
        self.callback = progress_callback
        
    def read(self, size=-1):
        if size == -1: size = 4096 # Default chunk if not specified by requests
        data = self.f.read(size)
        self.read_so_far += len(data)
        self.callback(self.read_so_far, self.total_size)
        return data
        
    def close(self):
        self.f.close()
        
    def __len__(self):
        return self.total_size

def upload_release(version, exe_path):
    """Creates a release and uploads the asset with PROGRESS BAR."""
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # 1. Create Release
    log(f"🚀 Creando Release v{version} en GitHub...")
    release_data = {
        "tag_name": f"v{version}",
        "target_commitish": "main",
        "name": f"WannaCall Pro v{version}",
        "body": "Actualización automática desde God Mode System.\n\n" + \
                "**CHANGELOG**:\n" + \
                "- Hotfix critical fixes applied.\n" + \
                "- Auto-deployment via God Mode.",
        "draft": False,
        "prerelease": False
    }
    
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases"
    r = requests.post(url, json=release_data, headers=headers)
    
    if r.status_code != 201:
        log(f"❌ Error creando release: {r.status_code} - {r.text}")
        sys.exit(1)
        
    release_json = r.json()
    upload_url_template = release_json["upload_url"] 
    upload_url = upload_url_template.split("{")[0]
    
    # 2. Upload Asset with Progress
    file_size_mb = os.path.getsize(exe_path) / (1024 * 1024)
    log(f"📤 Subiendo binario ({round(file_size_mb, 2)} MB)...")
    
    pb = ProgressBar(total=100, prefix='UPLOADING', length=40)
    
    def progress_cb(current, total):
        percent = int((current / total) * 100)
        pb.update(percent, f"{round(current/1024/1024, 1)}MB / {round(total/1024/1024, 1)}MB")

    try:
        # Custom file reader for requests streaming
        files = {'file': ( 'WannaCall_Pro.exe', open(exe_path, 'rb'), 'application/octet-stream' )}
        
        # Requests doesn't support easy upload callbacks without toolbelt or custom adapter.
        # We will use a simpler approach: Chunked upload manually is hard with Pre-Signed URLs or GitHub API logic.
        # But we can wrap the file object.
        
        wrapped_file = ProgressFileReader(exe_path, progress_cb)
        
        headers_upload = headers.copy()
        headers_upload["Content-Type"] = "application/octet-stream"
        
        r_upload = requests.post(
            upload_url,
            headers=headers_upload,
            params={'name': 'WannaCall_Pro.exe'},
            data=wrapped_file
        )
        wrapped_file.close()
        pb.complete()
        
        if r_upload.status_code != 201:
            log(f"❌ Error subiendo asset: {r_upload.status_code} - {r_upload.text}")
            sys.exit(1)
            
        log("✨ ¡ÉXITO! Nueva versión publicada y disponible.")
        
    except Exception as e:
        log(f"❌ Error en subida: {e}")
        sys.exit(1)

# Absolute path to Git because system path is broken
GIT_PATH = r"C:\Program Files\Git\cmd\git.exe"

def run_git(args):
    """Runs a git command using the absolute path."""
    cmd = [GIT_PATH] + args
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")

def sync_source_code(version):
    log("🔄 Sincronizando código fuente con GitHub...")
    
    if not os.path.exists(GIT_PATH):
        log(f"⚠️ Git no encontrado en {GIT_PATH}. Saltando sync de código.")
        return

    # 1. Configure remote with Token for auth-less push
    remote_url = f"https://{GITHUB_TOKEN}@github.com/{REPO_OWNER}/{REPO_NAME}.git"
    
    run_git(["remote", "set-url", "origin", remote_url])
    
    # 2. Add all changes
    run_git(["add", "."])
    
    # 3. Commit
    commit_msg = f"Auto-update v{version} (God Mode)"
    res_commit = run_git(["commit", "-m", commit_msg])
    
    if "nothing to commit" in res_commit.stdout:
         log("ℹ️ No hay cambios de código para subir.")
    else:
         log(f"✅ Cambios confirmados: {commit_msg}")
         
    # 4. Push (FORCE)
    log("🔥 FORZANDO sincronización (Source of Truth: Local)...")
    res_push = run_git(["push", "origin", "main", "--force"])
    
    if res_push.returncode != 0:
        log(f"⚠️ Alerta: No se pudo subir el código fuente.")
        err = res_push.stderr.replace(GITHUB_TOKEN, "HIDDEN_TOKEN")
        print(f"Error Git: {err}")
    else:
        log("✨ Código fuente sincronizado (Force Push).")

if __name__ == "__main__":
    try:
        print("""
        =========================================
           WANNA CALL? - GOD MODE PUBLISHER
        =========================================
        """)
        
        # 1. Bump Version
        ver = bump_version()
        
        # 2. Build
        binary = run_build()
        
        # 3. Upload Release (Binary)
        upload_release(ver, binary)
        
        # 4. Sync Source Code (Git)
        sync_source_code(ver)
        
        print("\n-----------------------------------------")
        print("🤖 PROCESO COMPLETADO. PUEDES DESCANSAR.")

    except Exception as e:
        print(f"\n❌❌❌ ERROR FATAL EN GOD MODE ❌❌❌")
        print(e)
        import traceback
        traceback.print_exc()
        
    finally:
        if "--auto" not in sys.argv:
            input("Pulsa Enter para salir...")
