import requests
import threading
import webbrowser
import tkinter as tk
from tkinter import messagebox
import logging
import sys
import os
import subprocess
import re

# CONFIG
REPO_USER = "kevinkgp92"
REPO_NAME = "wannacallbot"
VERSION_URL = f"https://raw.githubusercontent.com/{REPO_USER}/{REPO_NAME}/main/version.txt"
CHANGELOG_URL = f"https://raw.githubusercontent.com/{REPO_USER}/{REPO_NAME}/main/CHANGELOG.md"

class AutoUpdater:
    def __init__(self, current_version):
        self.current_version = current_version
        self.latest_version = None
        self.update_available = False
        self.changelog_data = "No se pudo cargar el registro de cambios."
        self._update_window = None

    def check_updates_silent(self, callback=None):
        """Checks for updates in a background thread."""
        threading.Thread(target=self._check, args=(callback,), daemon=True).start()

    def _check(self, callback):
        try:
            print(f"🔄 Buscando actualizaciones en: {VERSION_URL}")
            r = requests.get(VERSION_URL, timeout=5)
            if r.status_code == 200:
                remote_ver = r.text.strip()
                if self._is_newer(remote_ver, self.current_version):
                    self.latest_version = remote_ver
                    self.update_available = True
                    
                    # Also fetch changelog
                    self._fetch_changelog()
                    
                    print(f"🔔 Actualización encontrada: {remote_ver} (Actual: {self.current_version})")
                    if callback:
                        callback(True, remote_ver)
                    return
            print("✅ Aplicación actualizada.")
            if callback: callback(False, None)
        except Exception as e:
            # v2.2.36.1 (Hotfix): Silence connection errors (Socket [WinError 10013]) for a cleaner experience
            if any(x in str(e).lower() for x in ["connection", "socket", "10013", "timeout", "retries"]):
                print("⚠️  Actualización: Saltada (Desconectado o Firewall).")
            else:
                print(f"⚠️ Error buscando actualizaciones: {e}")
            if callback: callback(False, None)

    def _fetch_changelog(self):
        """Fetches the latest part of the changelog from GitHub."""
        try:
            r = requests.get(CHANGELOG_URL, timeout=5)
            if r.status_code == 200:
                full_text = r.text
                # Extract first section (latest version)
                # Matches from first '##' to second '##'
                sections = re.split(r'##\s+\[', full_text)
                if len(sections) > 1:
                    # sections[0] is usually the header, [1] is the latest
                    self.changelog_data = f"## [{sections[1]}"
                    # Clean up horizontal rules or end markers if any
                    self.changelog_data = self.changelog_data.split("---")[0].strip()
        except:
            pass

    def _is_newer(self, remote, local):
        """Semantic version comparison (e.g. 2.2.31 > 2.2.30)"""
        try:
            r_parts = [int(p) for p in re.findall(r'\d+', remote)]
            l_parts = [int(p) for p in re.findall(r'\d+', local)]
            for i in range(max(len(r_parts), len(l_parts))):
                rv = r_parts[i] if i < len(r_parts) else 0
                lv = l_parts[i] if i < len(l_parts) else 0
                if rv > lv: return True
                if rv < lv: return False
            return False
        except:
            return remote != local # Fallback

    def prompt_update(self, master):
        """Shows the premium visual update window."""
        try:
            from core.update_gui import UpdateWindow
            self._update_window = UpdateWindow(
                master, 
                self.current_version, 
                self.latest_version, 
                self.changelog_data,
                self.apply_update_git
            )
        except Exception as e:
            print(f"Error opening update window: {e}")
            # Fallback to simple prompt
            msg = f"¡Nueva versión disponible (v{self.latest_version})!\n\n¿Quieres actualizar ahora?"
            if messagebox.askyesno("Actualización", msg):
                self.apply_update_git()

    def apply_update_git(self):
        """Perform a git pull and restart the application."""
        # Use a thread to not freeze the GUI during git operations
        threading.Thread(target=self._do_git_update, daemon=True).start()

    def _do_git_update(self):
        try:
            if self._update_window:
                self._update_window.set_status("Conectando con GitHub...")
            
            # 1. Force update
            def run(cmd):
                return subprocess.run(cmd, check=True, capture_output=True, text=True)

            if self._update_window: self._update_window.set_status("Descargando nuevos archivos...")
            run(["git", "fetch", "--all"])
            
            if self._update_window: self._update_window.set_status("Sincronizando código...")
            run(["git", "reset", "--hard", "origin/main"])
            run(["git", "pull", "origin", "main"])
            
            if self._update_window: self._update_window.set_status("✅ ¡Listo! Reiniciando...")
            
            # 2. Restart
            import time
            time.sleep(1) # Visual feedback
            
            if getattr(sys, 'frozen', False):
                subprocess.Popen([sys.executable])
            else:
                subprocess.Popen([sys.executable, "gui.py"])
            
            os._exit(0)
            
        except Exception as e:
            msg = f"No se pudo completar la actualización automática:\n{e}"
            print(msg)
            if self._update_window:
                self._update_window.destroy()
            messagebox.showerror("Error de Actualización", msg + "\n\nPor favor, usa AUTO_FIX_ULTIMATE.bat")
class ServiceUpdater:
    """Compatibility stub for service definition updates."""
    def __init__(self):
        self.local_version = "2.2.86"

    def check_for_updates(self):
        # For now, we integrate service updates into main AutoUpdater
        # This is a stub to prevent crashes in ServiceManager
        print("SISTEMA: Sincronización de servicios lista.")
        return False

    def get_local_version(self):
        return self.local_version

    def update_services(self):
        # Logic moved to main updater if needed
        pass
