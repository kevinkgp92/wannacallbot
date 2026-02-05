import os
import sys
import subprocess
import time

def trigger_self_update(new_exe_path):
    """
    Creates a temporary batch file to swap the current EXE with a new one 
    after the current process exits.
    """
    if not getattr(sys, 'frozen', False):
        print("DEBUG: Not running as EXE, skipping binary swap.")
        return False
        
    current_exe = sys.executable
    pid = os.getpid()
    
    # Batch script logic:
    # 1. Wait for current PID to vanish
    # 2. Delete old EXE
    # 3. Rename new EXE to old EXE name
    # 4. Start the new EXE
    # 5. Delete itself
    batch_content = f"""@echo off
setlocal
:wait
tasklist /FI "PID eq {pid}" | find ":" > nul
if errorlevel 1 (
    timeout /t 1 /nobreak > nul
    goto perform
)
timeout /t 1 /nobreak > nul
goto wait

:perform
del /f /q "{current_exe}"
move /y "{new_exe_path}" "{current_exe}"
start "" "{current_exe}"
del "%~f0"
"""
    
    batch_path = os.path.join(os.path.dirname(current_exe), "update_swapper.bat")
    try:
        with open(batch_path, "w") as f:
            f.write(batch_content)
        
        # Run it silently
        subprocess.Popen(["cmd.exe", "/c", batch_path], 
                         creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0,
                         close_fds=True)
        return True
    except Exception as e:
        print(f"ERROR: Failed to trigger update: {e}")
        return False
