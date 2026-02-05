import requests
import threading
import webbrowser
import tkinter as tk
from tkinter import messagebox
import logging

# CONFIG
REPO_USER = "kevinkgp92"
REPO_NAME = "wannacallbot" # Asumido por el contexto
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
                # Simple string comparison (works for v2.2.5 vs v2.2.4)
                # Ideally use semver, but string compare works fine for format vX.X.X
                if remote_ver > self.current_version:
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

    def prompt_update(self):
        """Shows a GUI prompt to the user."""
        msg = f"¡Nueva versión disponible!\n\nVersión Actual: {self.current_version}\nNueva Versión: {self.latest_version}\n\n¿Quieres descargarla ahora?"
        response = messagebox.askyesno("Actualización Detectada 🚀", msg)
        if response:
            self.download_update()

    def download_update(self):
        """Opens the download page."""
        print("🚀 Abriendo página de descarga...")
        webbrowser.open(RELEASE_URL)
