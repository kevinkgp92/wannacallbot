import requests
import threading
import webbrowser
import tkinter as tk
from tkinter import messagebox
import logging
import sys
import os
import subprocess

# CONFIG
REPO_USER = "kevinkgp92"
REPO_NAME = "wannacallbot"
VERSION_URL = f"https://raw.githubusercontent.com/{REPO_USER}/{REPO_NAME}/main/version.txt"
RELEASE_URL = f"https://github.com/{REPO_USER}/{REPO_NAME}/releases/latest"

class AutoUpdater:
    def __init__(self, current_version):
        self.current_version = current_version
        self.latest_version = None
        self.update_available = False

    def check_updates_silent(self, callback=None):
        """Checks for updates in a background thread."""
        threading.Thread(target=self._check, args=(callback,), daemon=True).start()

    def _check(self, callback):
        try:
            print(f"🔄 Buscando actualizaciones en: {VERSION_URL}")
            r = requests.get(VERSION_URL, timeout=5)
            if r.status_code == 200:
                remote_ver = r.text.strip()
                # Check if versions are different
                if remote_ver != self.current_version:
                    self.latest_version = remote_ver
                    self.update_available = True
                    print(f"🔔 Actualización encontrada: {remote_ver} (Actual: {self.current_version})")
                    if callback:
                        callback(True, remote_ver)
                    return
            print("✅ Aplicación actualizada.")
            if callback: callback(False, None)
        except Exception as e:
            print(f"⚠️ Error buscando actualizaciones: {e}")
            if callback: callback(False, None)

    def apply_update_git(self):
        """Perform a git pull and restart the application."""
        try:
            print("🚀 Iniciando actualización automática via Git...")
            # 1. Force update
            subprocess.run(["git", "fetch", "--all"], check=True, capture_output=True)
            subprocess.run(["git", "reset", "--hard", "origin/main"], check=True, capture_output=True)
            subprocess.run(["git", "pull", "origin", "main"], check=True, capture_output=True)
            
            print("✅ Código actualizado. Reiniciando...")
            
            # 2. Restart
            if getattr(sys, 'frozen', False):
                subprocess.Popen([sys.executable])
            else:
                subprocess.Popen([sys.executable, "gui.py"])
            
            os._exit(0)
            
        except Exception as e:
            messagebox.showerror("Error de Actualización", f"No se pudo completar la actualización automática:\n{e}\n\nPor favor, usa el archivo AUTO_FIX_ULTIMATE.bat")

    def prompt_update(self):
        """Shows a GUI prompt to the user."""
        msg = f"¡Nueva versión disponible (v{self.latest_version})!\n\n¿Quieres actualizar ahora?\n(El bot se reiniciará automáticamente)"
        response = messagebox.askyesno("Actualización Detectada 🚀", msg)
        if response:
            self.apply_update_git()
