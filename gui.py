import os
import sys
import time

def _boot_log(msg):
    """Extreme primitive logging at the top to catch import hangs."""
    try:
        # Get the real directory of the script or EXE
        if hasattr(sys, '_MEIPASS'):
            log_dir = sys._MEIPASS
        else:
            log_dir = os.path.dirname(os.path.abspath(__file__))
            
        log_path = os.path.join(log_dir, "DEBUG_BOOT.txt")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")
    except: pass

_boot_log("--- COLD START ---")

# EMERGENCY ALERT TO PROVE EXECUTION
try:
    from tkinter import messagebox, Tk
    root = Tk()
    root.withdraw()
    # messagebox.showinfo("DEBUG", "El script ha comenzado a ejecutarse.")
    root.destroy()
except: pass

# DETECCION DE "FANTASMA" (MEI / COMPILED)
if hasattr(sys, '_MEIPASS'):
    _boot_log("WARNING: Running from MEIPASS (COMPILED EXE)")
    try:
        from tkinter import messagebox, Tk
        root = Tk()
        root.withdraw()
        # Only alert if it's the old version (if we can detect it) or just alert anyway
        # Since this is v2.2.6, if it's compiled, user might have just compiled it.
        # But if they are seeing v2.0.103, they are definitely not running THIS file.
        root.destroy()
    except: pass
else:
    _boot_log("Running from SOURCE CODE (.py)")

# Handle PyInstaller and compiled environments path resolution
try:
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
        _boot_log(f"MEIPASS active: {base_path}")
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    if base_path not in sys.path:
        sys.path.insert(0, base_path)
    _boot_log("Base path resolved")
except Exception as e:
    _boot_log(f"Base path error: {e}")

_boot_log("Importing customtkinter...")
import customtkinter as ctk
_boot_log("customtkinter imported")

_boot_log("Importing standard libs...")
import threading
import queue
import re
import json
from PIL import Image
from tkinter import messagebox
_boot_log("Standard libs imported")

_boot_log("Importing core modules...")
try:
    from core.updater import AutoUpdater
    _boot_log("AutoUpdater imported")
    from core.proxy_scraper import scrape_proxies
    _boot_log("proxy_scraper imported")
    import core.utils
    _boot_log("core.utils imported")
except Exception as e:
    _boot_log(f"Core import crash: {e}")

_boot_log("Configuring CTK...")
try:
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    _boot_log("CTK configured")
except Exception as e:
     _boot_log(f"CTK config crash: {e}")

class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag
        
        # CTkTextbox encapsulates a standard Tkinter Text widget in _textbox
        # We need to configure tags on the internal widget
        target = getattr(self.widget, "_textbox", self.widget)
        
        # Tags configuration for colors
        target.tag_config("SUCCESS", foreground="#2ecc71") # Green
        target.tag_config("ERROR", foreground="#e74c3c")   # Red
        target.tag_config("WARN", foreground="#f1c40f")    # Yellow
        target.tag_config("INFO", foreground="#3498db")    # Blue
        target.tag_config("SYSTEM", foreground="#9b59b6")  # Purple
        target.tag_config("OSINT", foreground="#1abc9c")   # Turquoise
        target.tag_config("GOD", foreground="#ff4500")     # Orange-Red

    def write(self, str_out):
        if not str_out: return
        
        # Strip ANSI codes (colorama garbage)
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        clean_str = ansi_escape.sub('', str_out)
        
        if not clean_str: return

        # Thread-safe UI update
        def _update():
            # CRITICAL: Check if widget still exists to avoid crash on close
            try:
                if not self.widget.winfo_exists(): return
                
                self.widget.configure(state="normal")
                
                # Determine color based on content
                tag_to_use = self.tag
                if "✔" in clean_str or "SUCCESS" in clean_str or "EXITO" in clean_str:
                    tag_to_use = "SUCCESS"
                elif "✘" in clean_str or "ERROR" in clean_str or "Exception" in clean_str or "Falla" in clean_str:
                    tag_to_use = "ERROR"
                elif "⚠" in clean_str or "WARN" in clean_str:
                    tag_to_use = "WARN"
                elif "ℹ" in clean_str or "INFO" in clean_str:
                    tag_to_use = "INFO"
                elif "🛡️" in clean_str or "SISTEMA" in clean_str:
                    tag_to_use = "SYSTEM"
                elif "🔍" in clean_str or "OSINT" in clean_str or "📧" in clean_str or "🆔" in clean_str:
                    tag_to_use = "OSINT"
                elif "♈" in clean_str or "GOD" in clean_str or "╔═" in clean_str or "║" in clean_str:
                    tag_to_use = "GOD"
                    
                self.widget.insert("end", clean_str, (tag_to_use,))
                self.widget.see("end")
                self.widget.configure(state="disabled")
            except:
                pass # Silent fail to avoid recursion if logging fails
            
        try:
            self.widget.after(0, _update)
        except:
            pass
        
    def flush(self):
        pass

class OsintGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # NITRO: Init attributes BEFORE splash to avoid AttributeError
        self.updater_ready = False
        self.updater = None
        self.initialization_complete = False
        self.logo_image = None
        
        # Thread-safe update queue
        import queue
        self.update_queue = queue.Queue()
        
        _boot_log("OsintGUI.__init__ start")
        # TEST: Disable splash temporarily to see if main window renders alone
        # self.show_splash() 
        _boot_log("Splash skipped (test mode)")
        self.version = "2.2.33" 
        _boot_log(f"Version: {self.version}")

        # Setup Auto-Updater (Silent)
        _boot_log("Starting AutoUpdater")
        self.updater = AutoUpdater(self.version)
        self.updater.check_updates_silent(callback=self._on_update_found)
        self.after(2000, self._process_update_queue)

        self.title(f"WANNA CALL? v{self.version} [SAUL EDITION]")
        self.geometry("1100x700")
        
        # Performance & Stats tracking
        self.total_success = 0
        self.total_error = 0
        self.batch_targets = []
        self.running = False
        
        # Grid layout configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Resource Path Helper
        def resource_path(relative_path):
            """ Get absolute path to resource, works for dev and for PyInstaller """
            try:
                if hasattr(sys, '_MEIPASS'):
                    return os.path.join(sys._MEIPASS, relative_path)
                return os.path.join(os.path.abspath("."), relative_path)
            except:
                return relative_path

        self.res_path = resource_path # Make it accessible

        logo_path = resource_path("wannacallbot_logo.png")
        icon_path = resource_path("icon.ico")
        
        self.logo_image = None
        
        # Set Window Icon
        try:
            self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Warning: Could not set icon: {e}")

        if os.path.exists(logo_path):
            self.logo_image = ctk.CTkImage(light_image=Image.open(logo_path),
                                           dark_image=Image.open(logo_path),
                                           size=(180, 180))
        else:
            print(f"Warning: Logo not found at {logo_path}")
            
        _boot_log("Starting _build_main_ui")
        # --- GUI LAYOUT ---
        try:
            self._build_main_ui()
            _boot_log("UI build finished successfully")
        except Exception as e:
            _boot_log(f"FATAL ERROR IN UI BUILD: {e}")
            error_msg = f"ERROR CRITICO DE UI:\n{e}\n\n{traceback.format_exc()}"
            print(error_msg)
            # Force show error in a box since it's an EXE environment
            try:
                messagebox.showerror("Fallo de Inicialización", error_msg)
            except: pass
        
        # Safety: Ensure window is visible even if splash hangs
        self.deiconify() # Force immediate deiconify for debugging
        self.after(5000, self.deiconify)
        
    def _on_update_found(self, found, new_version):
        """Callback triggered when an update is found (from background thread)."""
        if found:
            # Put update signal into thread-safe queue
            self.update_queue.put(("update_found", new_version))

    def _process_update_queue(self):
        """Processes signals from the update thread in the main thread."""
        try:
            while True:
                signal, data = self.update_queue.get_nowait()
                if signal == "update_found":
                    _boot_log(f"Signal received: Update to {data} ready.")
                    self.updater.prompt_update(self)
        except queue.Empty:
            pass
        finally:
            # Check again soon
            if not self.running or True: # Keep checking even if not 'attacking'
                self.after(500, self._process_update_queue)

    def _build_main_ui(self):
        _boot_log("Building Sidebar...")
        # --- Sidebar (Midnight Blue) ---
        try:
            self.sidebar_frame = ctk.CTkScrollableFrame(self, width=280, corner_radius=0, fg_color="#0f0f15", label_text="") 
            self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
            self.sidebar_frame.grid_columnconfigure(0, weight=1)
            self.sidebar_frame.grid_rowconfigure(4, weight=1)
        except Exception as e: _boot_log(f"Fail Sidebar Frame: {e}")

        # --- SECTION: HEADER ---
        self.sidebar_header = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.sidebar_header.pack(fill="x", padx=10, pady=(20, 10))
        
        if self.logo_image:
            self.logo_label = ctk.CTkLabel(self.sidebar_header, text="", image=self.logo_image)
            self.logo_label.pack(pady=(0, 10))
            
        self.title_label = ctk.CTkLabel(self.sidebar_header, text="WANNA CALL?", 
                                        font=ctk.CTkFont(family="Roboto Medium", size=26, weight="bold"), 
                                        text_color="#ffc107") # Golden Yellow
        self.title_label.pack()

        # --- SECTION: EXECUTION MODE ---
        self.mode_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.mode_frame.pack(fill="x", padx=20, pady=10)
        
        self.mode_label = ctk.CTkLabel(self.mode_frame, text="MODO DE EJECUCIÓN", anchor="w", 
                                        font=ctk.CTkFont(family="Roboto", size=12, weight="bold"), text_color="gray70")
        self.mode_label.pack(fill="x")
        self.mode_desc = ctk.CTkLabel(self.mode_frame, text="Secuencial. Uno tras otro. Seguro.", anchor="w", 
                                        font=ctk.CTkFont(family="Roboto", size=10), text_color="gray50")
        self.mode_desc.pack(fill="x", pady=(0, 5))

        self.mode_option = ctk.CTkOptionMenu(self.mode_frame, values=["Automático (Secuencial)", "Porculero (Hilos)", "Nocturno", "Contrareembolso", "Buscador OSINT"],
                                             command=self.change_mode_event,
                                             fg_color="#2b2b40", button_color="#ff4500", button_hover_color="#e74c3c", text_color="white")
        self.mode_option.pack(fill="x")

        # --- SECTION: APPEARANCE & THEME ---
        self.theme_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.theme_frame.pack(fill="x", padx=20, pady=10)

        self.appearance_mode_label = ctk.CTkLabel(self.theme_frame, text="APARIENCIA", anchor="w", 
                                                font=ctk.CTkFont(family="Roboto", size=12, weight="bold"), text_color="gray70")
        self.appearance_mode_label.pack(fill="x")
        
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.theme_frame, values=["Dark", "Light"], command=self.change_appearance_mode_event,
                                                             fg_color="#333333", button_color="#444444", button_hover_color="#555555")
        self.appearance_mode_optionemenu.pack(fill="x", pady=5)

        self.proxy_switch = ctk.CTkSwitch(self.theme_frame, text="PROXY AUTOMÁTICO", font=ctk.CTkFont(size=11, weight="bold"))
        self.proxy_switch.pack(fill="x", pady=2)
        self.proxy_switch.select() # Default to ON as requested
        
        self.matrix_switch = ctk.CTkSwitch(self.theme_frame, text="MODO MATRIX", font=ctk.CTkFont(size=11, weight="bold"), command=self.toggle_matrix_theme)
        self.matrix_switch.pack(fill="x", pady=2)

        self.ghost_switch = ctk.CTkSwitch(self.theme_frame, text="MODO FANTASMA (Consola)", font=ctk.CTkFont(size=11, weight="bold"))
        self.ghost_switch.pack(fill="x", pady=2)
        self.ghost_switch.select() # Default ON as requested


        # --- SECTION: STATISTICS & CHAOS ---
        self.stats_label = ctk.CTkLabel(self.sidebar_frame, text="MÉTRICAS DE ATAQUE", anchor="w", 
                                         font=ctk.CTkFont(family="Roboto", size=12, weight="bold"), text_color="#ff4500")
        self.stats_label.pack(fill="x", padx=20, pady=(10, 0))
        
        self.stats_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="#1a1a2e", corner_radius=10, border_width=1, border_color="#33334d")
        self.stats_frame.pack(fill="x", padx=20, pady=5)
        
        self.label_success = ctk.CTkLabel(self.stats_frame, text="✅ 0", font=ctk.CTkFont(size=14, weight="bold"), text_color="#2ecc71")
        self.label_success.pack(side="left", padx=15, pady=10)
        
        self.label_error = ctk.CTkLabel(self.stats_frame, text="❌ 0", font=ctk.CTkFont(size=14, weight="bold"), text_color="#e74c3c")
        self.label_error.pack(side="right", padx=15, pady=10)

        # Chaos Meter
        self.chaos_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.chaos_frame.pack(fill="x", padx=20, pady=5)
        self.chaos_label = ctk.CTkLabel(self.chaos_frame, text="NIVEL DE CAOS", font=ctk.CTkFont(size=10, weight="bold"), text_color="gray60")
        self.chaos_label.pack(anchor="w")
        self.chaos_bar = ctk.CTkProgressBar(self.chaos_frame, height=8, progress_color="#ff0055", fg_color="#1a1a2e")
        self.chaos_bar.pack(fill="x", pady=2)
        self.chaos_bar.set(0)

        # --- SECTION: UTILITIES ---
        self.utils_label = ctk.CTkLabel(self.sidebar_frame, text="UTILIDADES PRO", anchor="w", 
                                        font=ctk.CTkFont(family="Roboto", size=12, weight="bold"), text_color="gray70")
        self.utils_label.pack(fill="x", padx=20, pady=(10, 0))
        
        self.utils_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="#1a1a2e", corner_radius=10)
        self.utils_frame.pack(fill="x", padx=20, pady=5)
        
        self.btn_autofill = ctk.CTkButton(self.utils_frame, text="✨ AUTO-RELLENAR", command=self.autofill_data,
                                          fg_color="#8e44ad", hover_color="#9b59b6", font=ctk.CTkFont(size=11), height=28)
        self.btn_autofill.pack(fill="x", padx=10, pady=(10, 2))
        
        self.btn_scrape_proxies = ctk.CTkButton(self.utils_frame, text="🌐 DESCARGAR PROXIES", command=self.scrape_new_proxies,
                                                fg_color="#2980b9", hover_color="#3498db", font=ctk.CTkFont(size=11), height=28)
        self.btn_scrape_proxies.pack(fill="x", padx=10, pady=2)

        self.btn_normalize = ctk.CTkButton(self.utils_frame, text="🧪 NORMALIZAR LISTA", command=self.normalize_batch_phones,
                                           fg_color="#d35400", hover_color="#e67e22", font=ctk.CTkFont(size=11), height=28)
        self.btn_normalize.pack(fill="x", padx=10, pady=2)

        self.btn_clear_hist = ctk.CTkButton(self.utils_frame, text="🗑️ LIMPIAR HISTORIAL", command=self.clear_history,
                                            fg_color="#7f8c8d", hover_color="#95a5a6", font=ctk.CTkFont(size=11), height=28)
        self.btn_clear_hist.pack(fill="x", padx=10, pady=2)
        
        self.btn_export_log = ctk.CTkButton(self.utils_frame, text="💾 EXPORTAR LOG", command=self.export_log,
                                            fg_color="#27ae60", hover_color="#2ecc71", font=ctk.CTkFont(size=11), height=28)
        self.btn_export_log.pack(fill="x", padx=10, pady=2)

        self.btn_open_logs = ctk.CTkButton(self.utils_frame, text="📁 ABRIR DIRECTORIO LOGS", command=self.open_logs_folder,
                                           fg_color="#34495e", hover_color="#2c3e50", font=ctk.CTkFont(size=11), height=28)
        self.btn_open_logs.pack(fill="x", padx=10, pady=2)

        self.btn_cleanup = ctk.CTkButton(self.utils_frame, text="🧹 LIMPIAR TEMPORALES", command=self.cleanup_temp,
                                         fg_color="#c0392b", hover_color="#e74c3c", font=ctk.CTkFont(size=11), height=28)
        self.btn_cleanup.pack(fill="x", padx=10, pady=(2, 10))

        # --- SECTION: STEALTH & TURBO ---
        self.stealth_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.stealth_frame.pack(fill="x", padx=20, pady=10)

        self.stealth_label = ctk.CTkLabel(self.stealth_frame, text="NIVEL DE SIGILO", anchor="w", font=ctk.CTkFont(family="Roboto", size=12, weight="bold"), text_color="gray70")
        self.stealth_label.pack(fill="x")
        self.stealth_slider = ctk.CTkSlider(self.stealth_frame, from_=0, to=2, number_of_steps=2, command=self.update_stealth_desc)
        self.stealth_slider.pack(fill="x", pady=2)
        self.stealth_slider.set(1)
        self.stealth_desc = ctk.CTkLabel(self.stealth_frame, text="Equilibrado", font=ctk.CTkFont(size=10), text_color="gray50")
        self.stealth_desc.pack()

        self.turbo_label = ctk.CTkLabel(self.stealth_frame, text="MODO TURBO (HILOS)", anchor="w", font=ctk.CTkFont(family="Roboto", size=12, weight="bold"), text_color="gray70")
        self.turbo_label.pack(fill="x", pady=(10, 0))
        self.turbo_slider = ctk.CTkSlider(self.stealth_frame, from_=1, to=10, number_of_steps=9, command=self.update_turbo_desc)
        self.turbo_slider.pack(fill="x", pady=2)
        self.turbo_slider.set(1)
        self.turbo_desc = ctk.CTkLabel(self.stealth_frame, text="1 Hilo (Seguro)", font=ctk.CTkFont(size=10), text_color="gray50")
        self.turbo_desc.pack()

        # --- SECTION: AGENT & SELECTOR ---
        self.agent_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.agent_frame.pack(fill="x", padx=20, pady=10)

        self.ua_label = ctk.CTkLabel(self.agent_frame, text="USER-AGENT (DEVICE)", anchor="w", font=ctk.CTkFont(family="Roboto", size=12, weight="bold"), text_color="gray70")
        self.ua_label.pack(fill="x")
        self.ua_option = ctk.CTkOptionMenu(self.agent_frame, values=["PC (Windows/Chrome)", "Mobile (iPhone)", "Mobile (Android)"],
                                           fg_color="#34495e", button_color="#2c3e50")
        self.ua_option.pack(fill="x", pady=5)

        self.serv_sel_label = ctk.CTkLabel(self.sidebar_frame, text="SERVICIOS ACTIVOS", anchor="w", font=ctk.CTkFont(family="Roboto", size=12, weight="bold"), text_color="gray70")
        self.serv_sel_label.pack(fill="x", padx=20, pady=(10, 0))
        
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self.filter_services)
        self.search_entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="🔍 Buscar...", textvariable=self.search_var, font=ctk.CTkFont(size=10), height=25)
        self.search_entry.pack(fill="x", padx=20, pady=5)

        self.sel_tools_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.sel_tools_frame.pack(fill="x", padx=20)
        self.btn_all = ctk.CTkButton(self.sel_tools_frame, text="Todos", width=60, height=20, command=self.select_all_services, fg_color="#34495e", font=ctk.CTkFont(size=10))
        self.btn_all.pack(side="left", padx=(0, 5))
        self.btn_none = ctk.CTkButton(self.sel_tools_frame, text="Ninguno", width=60, height=20, command=self.select_none_services, fg_color="#34495e", font=ctk.CTkFont(size=10))
        self.btn_none.pack(side="left")

        self.serv_frame = ctk.CTkScrollableFrame(self.sidebar_frame, height=180, fg_color="#1a1a2e")
        self.serv_frame.pack(fill="x", padx=20, pady=(5, 15))
        
        self.service_vars = {}
        self.service_checkboxes = {}
        try:
            _boot_log("Populating services...")
            self.populate_services()
        except Exception as e: _boot_log(f"Fail Populate Services: {e}")

        # --- SECTION: TELEGRAM ---
        self.tg_label = ctk.CTkLabel(self.sidebar_frame, text="TELEGRAM REMOTE", anchor="w", font=ctk.CTkFont(family="Roboto", size=12, weight="bold"), text_color="gray70")
        self.tg_label.pack(fill="x", padx=20)
        self.tg_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="#1a1a2e", corner_radius=10)
        self.tg_frame.pack(fill="x", padx=20, pady=5)
        
        self.tg_token = ctk.CTkEntry(self.tg_frame, placeholder_text="Token", font=ctk.CTkFont(size=10), height=24)
        self.tg_token.pack(fill="x", padx=10, pady=(8, 2))
        self.tg_chat_id = ctk.CTkEntry(self.tg_frame, placeholder_text="Chat ID", font=ctk.CTkFont(size=10), height=24)
        self.tg_chat_id.pack(fill="x", padx=10, pady=2)
        self.btn_remote = ctk.CTkButton(self.tg_frame, text="🤖 ACTIVAR MANDO", command=self.toggle_remote_control,
                                        fg_color="#8e44ad", hover_color="#9b59b6", font=ctk.CTkFont(size=10, weight="bold"), height=26)
        self.btn_remote.pack(fill="x", padx=10, pady=(5, 10))

        self.btn_update = ctk.CTkButton(self.sidebar_frame, text="🔄 ACTUALIZAR SERVICIOS", command=self.manual_update_check,
                                        fg_color="#16a085", hover_color="#1abc9c", font=ctk.CTkFont(size=11, weight="bold"), height=30)
        self.btn_update.pack(fill="x", padx=20, pady=(15, 5))

        self.btn_build = ctk.CTkButton(self.sidebar_frame, text="⚙️ GENERAR INSTALADOR EXE", command=self.trigger_build_pro,
                                       fg_color="#34495e", hover_color="#2c3e50", font=ctk.CTkFont(size=11, weight="bold"), height=30)
        self.btn_build.pack(fill="x", padx=20, pady=(5, 30))

        _boot_log("Building Main Area...")
        # --- Main Area ---
        # --- Main Area (Deep Space) ---
        try:
            self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#16161d")
            self.main_frame.grid(row=0, column=1, sticky="nsew")
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure(2, weight=1) # Log area expands
        except Exception as e: _boot_log(f"Fail Main Frame: {e}")

        # Input Fields Container (Glass Card Style)
        self.inputs_frame = ctk.CTkFrame(self.main_frame, fg_color="#1f1f2e", corner_radius=20, border_width=1, border_color="#33334d")
        self.inputs_frame.grid(row=0, column=0, padx=30, pady=30, sticky="ew")
        
        self.Target_label = ctk.CTkLabel(self.inputs_frame, text="DATOS DEL OBJETIVO", font=ctk.CTkFont(family="Roboto", size=18, weight="bold"), text_color="#ff4500")
        self.Target_label.grid(row=0, column=0, columnspan=2, padx=25, pady=(20, 5), sticky="w")
        self.Target_desc = ctk.CTkLabel(self.inputs_frame, text="Información de la víctima para los formularios", font=ctk.CTkFont(family="Roboto", size=11), text_color="gray60")
        self.Target_desc.grid(row=1, column=0, columnspan=2, padx=25, pady=(0, 10), sticky="w")
        
        # Row 2
        self.entry_phone = ctk.CTkEntry(self.inputs_frame, placeholder_text="Teléfono (Ej: 666111222)", height=35, corner_radius=8, border_color="#e74c3c")
        self.entry_phone.grid(row=2, column=0, padx=25, pady=(5, 5), sticky="ew")
        
        self.entry_name = ctk.CTkEntry(self.inputs_frame, placeholder_text="Nombre", height=35, corner_radius=8)
        self.entry_name.grid(row=2, column=1, padx=25, pady=(5, 5), sticky="ew")

        # Row 3
        self.entry_surname = ctk.CTkEntry(self.inputs_frame, placeholder_text="Apellidos", height=35, corner_radius=8)
        self.entry_surname.grid(row=3, column=0, padx=25, pady=(5, 5), sticky="ew")

        self.entry_email = ctk.CTkEntry(self.inputs_frame, placeholder_text="Email", height=35, corner_radius=8)
        self.entry_email.grid(row=3, column=1, padx=25, pady=(5, 5), sticky="ew")

        # Row 4
        self.entry_zip = ctk.CTkEntry(self.inputs_frame, placeholder_text="Código Postal", height=35, corner_radius=8)
        self.entry_zip.grid(row=4, column=0, padx=25, pady=(5, 20), sticky="ew")
        self.entry_zip.insert(0, "28013") # Default Zip Code
        
        self.inputs_frame.grid_columnconfigure(0, weight=1)
        self.inputs_frame.grid_columnconfigure(1, weight=1)

        # Action Bar
        self.action_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.action_frame.grid(row=1, column=0, padx=30, pady=(0, 20), sticky="ew")
        
        self.btn_start = ctk.CTkButton(self.action_frame, text=f"!!! INICIAR v{self.version} !!!", command=self.start_process, 
                                       fg_color="#2ecc71", hover_color="#27ae60", height=60, corner_radius=15,
                                       font=ctk.CTkFont(family="Roboto", size=20, weight="bold"),
                                       border_width=2, border_color="#2ecc71")
        self.btn_start.pack(side="left", fill="x", expand=True, padx=(0, 15))
        
        self.btn_stop = ctk.CTkButton(self.action_frame, text="DETENER", command=self.stop_process, 
                                      fg_color="#555555", hover_color="#333333", state="disabled", height=60, corner_radius=10,
                                      font=ctk.CTkFont(family="Roboto", size=20, weight="bold"))
        self.btn_stop.pack(side="right", fill="x", expand=True, padx=(15, 0))

        # Batch Mode Button
        self.btn_batch = ctk.CTkButton(self.inputs_frame, text="📁 CARGAR LISTA (.TXT)", command=self.load_batch_file,
                                      fg_color="#2980b9", hover_color="#3498db", height=35)
        self.btn_batch.grid(row=5, column=1, padx=25, pady=(15, 5), sticky="ew")
        self.batch_targets = []

        # Favorites UI - Row 5 of inputs_frame
        self.fav_label = ctk.CTkLabel(self.inputs_frame, text="FAVORITOS", font=ctk.CTkFont(family="Roboto", size=14, weight="bold"), text_color="gray70")
        self.fav_label.grid(row=5, column=0, padx=25, pady=(15, 5), sticky="w")
        
        self.fav_option = ctk.CTkOptionMenu(self.inputs_frame, values=["--- Seleccionar ---"], command=self.load_favorite_event)
        self.fav_option.grid(row=6, column=0, padx=25, pady=(0, 20), sticky="ew")
        
        self.btn_save_fav = ctk.CTkButton(self.inputs_frame, text="GUARDAR OBJETIVO", command=self.save_favorite, 
                                        fg_color="#34495e", hover_color="#2c3e50", height=35)
        self.btn_save_fav.grid(row=6, column=1, padx=25, pady=(0, 20), sticky="ew")

        self.refresh_favorites_menu()

         # Bindings for Auto-Email
        self.email_modified = False
        self.entry_name.bind("<KeyRelease>", self.update_email)
        self.entry_surname.bind("<KeyRelease>", self.update_email)
        self.entry_email.bind("<FocusIn>", self.mark_email_modified)

        # Log Area
        self.log_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.log_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_rowconfigure(2, weight=1)

        self.log_label = ctk.CTkLabel(self.log_frame, text="Registros de Operación:", anchor="w", font=ctk.CTkFont(size=14, weight="bold"), text_color="gray70")
        self.log_label.pack(fill="x", pady=(0, 5))

        self.log_box = ctk.CTkTextbox(self.log_frame, width=400, height=450, state="disabled", font=("Consolas", 12),
                                      fg_color="#13131a", text_color="#ff4500", border_width=1, border_color="#33334d")
        self.log_box.pack(fill="both", expand=True)

        # Progress Section
        self.progress_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.progress_frame.grid(row=3, column=0, padx=30, pady=(0, 20), sticky="ew")
        
        self.progress_label = ctk.CTkLabel(self.progress_frame, text="Esperando inicio...", font=ctk.CTkFont(family="Roboto", size=14))
        self.progress_label.pack(side="top", anchor="w", pady=(0, 5))
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, height=15, corner_radius=10, fg_color="#2b2b40", progress_color="#ff4500")
        self.progress_bar.pack(fill="x", expand=True)
        self.progress_bar.set(0)
        
        # Redirect standard output and error to the GUI log box
        sys.stdout = TextRedirector(self.log_box, "stdout")
        sys.stderr = TextRedirector(self.log_box, "stderr")
        
        self.tg_controller = None
        self.initialization_complete = True # Signal splash we are done building
        _boot_log("BOOT COMPLETE: GUI is ready.")
        
        # Close Splash and show main window
        self.splash_close_id = self.after(2000, self.hide_splash)
        
        # Banner initialization
        self.print_banner()
        
        # Shutdown Protocol
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """Forces a clean shutdown to prevent PyInstaller _MEI warnings."""
        try:
            self.running = False
            # Stop updater if it's doing something (daemon threads will die with sys.exit)
            if self.updater:
                self.updater.is_updating = False
            
            # Destroy GUI first
            self.destroy()
        except: pass
        finally:
            # FORCE EXIT: This releases file locks on _MEI folders immediately
            sys.exit(0)

    def _background_loader(self):
        """No longer used for core loading, kept for compatibility."""
        self.initialization_complete = True

    def show_splash(self):
        """Creates a professional splash screen while loading."""
        self.withdraw() # Hide main window
        self.splash = ctk.CTkToplevel()
        self.splash.overrideredirect(True) # No borders
        # self.splash.attributes("-topmost", True) # REMOVED: Hides error messages
        
        # Center splash
        w, h = 400, 300
        sw = self.splash.winfo_screenwidth()
        sh = self.splash.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.splash.geometry(f"{w}x{h}+{x}+{y}")
        self.splash.configure(fg_color="#16161d")
        
        # Splash content
        ctk.CTkLabel(self.splash, text="⚖️", font=("Roboto", 80), text_color="#ff4500").pack(pady=(40, 0))
        ctk.CTkLabel(self.splash, text="WANNA CALL?", font=("Roboto", 24, "bold"), text_color="white").pack()
        self.splash_label = ctk.CTkLabel(self.splash, text="Iniciando Núcleo...", font=("Roboto", 12), text_color="gray60")
        self.splash_label.pack(pady=20)
        
        self.splash_progress = ctk.CTkProgressBar(self.splash, width=300, height=4, progress_color="#ff4500", fg_color="#2b2b40")
        self.splash_progress.pack(pady=10)
        self.splash_progress.set(0)
        
        def _animate_splash(val):
            # Safety check: Stop if splash is gone
            if not hasattr(self, 'splash') or not self.splash.winfo_exists():
                return

            # NITRO LOGIC: Sync progress with background loader
            target_val = val
            
            if not self.initialization_complete:
                 # If loading, cap visual progress at 85%
                 if val < 0.85:
                     target_val += 0.02
                 else:
                     # Pulse effect while waiting
                     target_val = 0.85
            else:
                 # Loaded! Zoom to finish
                 target_val += 0.05

            if target_val <= 1.1:
                self.splash_progress.set(min(target_val, 1.0))
                # Update text based on stage
                if target_val > 0.9: self.splash_label.configure(text="¡Listo!")
                elif target_val > 0.5: self.splash_label.configure(text="Cargando Módulos...")
                
                # Close if finished (allow slight buffer > 1.0 to show full bar)
                if target_val >= 1.05 and self.initialization_complete:
                     self.hide_splash()
                     return

                self.splash.after(30, lambda: _animate_splash(target_val))
        
        _animate_splash(0)

    def hide_splash(self):
        try:
            if hasattr(self, 'splash') and self.splash.winfo_exists():
                self.splash.destroy()
        except: pass
        
        # Ensure main window is visible and forced to redraw
        try:
            _boot_log("Hiding splash and deiconifying main window")
            self.deiconify()
            self.lift()
            self.focus_force()
            self.update() # Force Tkinter to recalculate layout and draw frames
            _boot_log(f"Main window state: {self.state()}")
        except Exception as e:
            _boot_log(f"Error during deiconify: {e}")

    def trigger_build_pro(self):
        """Runs the build_pro.py script in a background thread."""
        res = messagebox.askyesno("Generar Instalador", 
                                  "Este proceso creará un ejecutable independiente (.exe) en la carpeta 'dist' y un acceso directo en tu escritorio.\n\n"
                                  "¿Deseas continuar? Puede tardar un minuto.")
        if res:
            print("SISTEMA: Iniciando proceso de compilación profesional...")
            self.btn_build.configure(state="disabled", text="🏗️ COMPILANDO...")
            threading.Thread(target=self._build_task, daemon=True).start()

    def _build_task(self):
        try:
            import subprocess
            import shutil
            
            # 1. Resolve Project Root and Python
            # 1. Resolve Project Root and Python
            found_root = None
            if getattr(sys, 'frozen', False):
                # We could be running from bin/ or dist/
                potential_roots = [
                    os.path.dirname(sys.executable),
                    os.path.dirname(os.path.dirname(sys.executable)),
                    os.getcwd()
                ]
            else:
                potential_roots = [
                    os.path.dirname(os.path.abspath(__file__)),
                    os.getcwd()
                ]

            script_path = None
            for root in potential_roots:
                test_path = os.path.join(root, "build_pro.py")
                if os.path.exists(test_path):
                    found_root = root
                    script_path = test_path
                    break
            
            if not found_root:
                print(f"❌ ERROR: No se encontró 'build_pro.py' en ninguna de las rutas: {potential_roots}")
                return

            # Resolve Python
            if not getattr(sys, 'frozen', False):
                py_exe = sys.executable
            else:
                py_exe = None
                for p in ["python.exe", "python", "python3.exe", "python3", r"C:\Python312\python.exe", r"C:\Python311\python.exe"]:
                    if shutil.which(p):
                        py_exe = p
                        break
            
            if not py_exe:
                print("❌ ERROR: No se encontró Python en el sistema.")
                self.after(0, lambda: messagebox.showerror("Ambiente No Encontrado", 
                                                          "Para generar instaladores necesitas Python instalado."))
                return

            log_file = os.path.join(found_root, "build_log.txt")

            print(f"SISTEMA: Iniciando compilación aislada con {py_exe}...")
            
            # UPDATED DIAGNOSTIC MODE: Removed flags to fix windows store python crash
            # Capturing stderr for error report
            error_log = os.path.join(found_root, "build_error.log")
            self.error_file = open(error_log, "w", encoding="utf-8")
            
            # SIMPLIFIED LAUNCH: Use current interpreter directly
            # This avoids execution alias issues by inheriting the environment
            
            # Use lists for arguments (better safety)
            cmd = [sys.executable, "-u", script_path]
            
            proc = subprocess.Popen(cmd, 
                                   cwd=os.path.dirname(script_path),
                                   stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL,
                                   # No shell=True, no flags. Just plain process spawn.
                                   )
            
            # Schedule the first poll
            self.after(500, lambda: self._poll_build_log(proc, 0, log_file))
            
        except Exception as e:
            print(f"❌ ERROR CRÍTICO: {e}")
            self.after(0, lambda: messagebox.showerror("Falla de Sistema", f"Error al lanzar el compilador: {e}"))
            self.after(0, lambda: self.btn_build.configure(state="normal", text="⚙️ GENERAR INSTALADOR EXE"))

    def _poll_build_log(self, proc, last_pos, log_file):
        """Recursive poller that runs on the MAIN thread to avoid Tcl/Tk issues."""
        try:
            # 1. Read new lines
            if os.path.exists(log_file):
                try:
                    with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
                        f.seek(last_pos)
                        new_content = f.read()
                        if new_content:
                            last_pos = f.tell()
                            
                            # Parse lines for GUI updates
                            for line in new_content.splitlines():
                                if not line.strip(): continue
                                
                                # Progress Tag
                                if "[PROGRESS]" in line:
                                    try:
                                        p_val = int(line.split("[PROGRESS]")[1].strip())
                                        self.progress_bar.set(p_val / 100)
                                    except: pass
                                    continue # Don't show tag in text box
                                    
                                # Status Tag
                                if "[STATUS]" in line:
                                    msg = line.split("[STATUS]")[1].strip()
                                    self.progress_label.configure(text=msg)
                                    # Show status in box clearly
                                    print(f"ℹ️ {msg}")
                                    continue
                                
                                # Warn Tag
                                if "[WARN]" in line:
                                     print(f"⚠️ {line.split('[WARN]')[1].strip()}")
                                     continue

                                # Filter raw noise (optional) keeps important logs
                                if " > " in line or "[INFO]" in line:
                                     continue # Hide raw noise
                                    
                                # Print everything else (errors, final success, etc)
                                print(line)
                                
                except: pass
            
            # 2. Check if process finished
            status = proc.poll()
            if status is None:
                # Still running, schedule next poll
                self.after(500, lambda: self._poll_build_log(proc, last_pos, log_file))
            else:
                # Finished! Clean up UI
                self.btn_build.configure(state="normal", text="⚙️ GENERAR INSTALADOR EXE")
                
                # Check if EXE exists as a secondary success signal
                exe_output = os.path.join(os.path.dirname(os.path.abspath(log_file)), "dist", "PerubianBot_Ultimate.exe")
                if status == 0 or os.path.exists(exe_output):
                    print("\n✨ COMPILACIÓN FINALIZADA CON ÉXITO.")
                    messagebox.showinfo("Éxito", f"El instalador ha sido generado satisfactoriamente.\n\nUbicación: {exe_output}")
                else:
                    print(f"\n❌ COMPILACIÓN FALLIDA (Código: {status})")
                    
                    # Read build log for fatal errors since stderr is not captured anymore
                    err_msg = ""
                    try:
                        if os.path.exists(log_file):
                            with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
                                # Read last 20 lines to find the fatal error
                                lines = f.readlines()[-20:] 
                                for line in reversed(lines):
                                    if "[FATAL]" in line or "FATAL" in line or "ERROR" in line:
                                        err_msg = line.strip()
                                        if "[FATAL]" in line: # Prefer explicit fatal tag
                                            break
                    except: pass
                    
                    if not err_msg:
                        err_msg = "Consulta 'build_log.txt' para ver el error exacto."
                        friendly_tip = "Posible causa: Antivirus bloqueando o carpeta abierta."
                    else:
                        print(f"\n[DIAGNÓSTICO]: {err_msg}")
                        # Friendly translation of common errors
                        friendly_tip = "Error desconocido. Revisa el antivirus."
                        if "Access is denied" in err_msg or "PermissionError" in err_msg or "ACCESO DENEGADO" in err_msg:
                            friendly_tip = "🔒 ARCHIVO BLOQUEADO: Tienes 'WannaCall_Pro.exe' abierto. Ciérralo o reinicia el PC."
                        elif "No module named" in err_msg:
                             friendly_tip = "🧩 FALTA UN MÓDULO: Tu instalación de Python está incompleta."

                    messagebox.showerror("¡Ups! Hubo un problema", 
                                       f"No pudimos crear el ejecutable.\n\n"
                                       f"🔍 Razón Técnica: {err_msg}\n\n"
                                       f"💡 CONSEJO: {friendly_tip}")
        except Exception as e:
            print(f"❌ ERROR EN POLLING: {e}")
            self.btn_build.configure(state="normal", text="⚙️ GENERAR INSTALADOR EXE")

    def print_banner(self):
        banner = rf"""
 __      __                         _________      .__  .__   
/  \    /  \_____    ____   ____    \_   ___ \_____  |  | |  |   
\   \/\/   /\__  \  /    \ /    \   /    \  \/\__  \ |  | |  |   
 \        /  / __ \|   |  \   |  \  \     \____/ __ \|  |_|  |_  
  \__/\  /  (____  /___|  /___|  /   \______  (____  /____/____/  
       \/        \/     \/     \/           \/     \/          
                                           v{self.version} - SAUL EDITION
"""
        print(banner)
        print(f"⚖️ ¿NECESITAS AYUDA LEGAL? (Versión {self.version})")
        print("📞 LLAMARME A MÍ ES MEJOR QUE LLAMAR A TU MADRE.")
        print("--------------------------------------------------")

    def _process_update_queue(self):
        """Consumes update messages from the queue on the main thread."""
        try:
            while True:
                msg = self.update_queue.get_nowait()
                self._handle_update_message(msg)
        except queue.Empty:
            pass
        finally:
            # Schedule next poll
            if self.running or True: # Keep polling
                time.sleep(1) # v2.2.28: Yield to system during GUI polling
                self.after(1000, self._process_update_queue) # Increased from 500 to 1000

    def _handle_update_message(self, message):
        """Actual logic to update GUI (formerly _on_update_check_done)."""
        # Fix for v2.2.21: Handle both strings and tuples from update_queue
        msg_type = ""
        msg_content = ""
        
        if isinstance(message, tuple):
            msg_type = message[0]
            msg_content = message[1]
        else:
            msg_type = message
            msg_content = message

        if msg_type == "RESTART_REQUIRED":
            pass
        elif isinstance(msg_type, str) and msg_type.startswith("PROGRESS:"):
            # Update splash screen if active
            try:
                percent_str = message.split(":")[1]
                percent_float = int(percent_str) / 100.0
                
                # 1. Update Splash Screen (if visible)
                if hasattr(self, 'splash_label') and self.splash_label.winfo_exists():
                    self.splash_label.configure(text=f"Descargando actualización: {percent_str}%")
                    # Keep splash alive
                    self.after_cancel(self.splash_close_id) 
                    self.splash_close_id = self.after(3000, self.hide_splash) 
                
                # 2. Update Main Window (always safe)
                if hasattr(self, 'progress_label') and hasattr(self, 'progress_bar'):
                    self.progress_label.configure(text=f"📡 Descargando actualización... {percent_str}%")
                    self.progress_bar.set(percent_float)
                    
            except: pass
            return # Don't print progress to console to avoid spam
        else:
            print(f"📡 {message}")
            
        if self.updater and self.updater.update_available:
            # Show a professional update prompt
            def show_update_prompt():
                # Check ensures we don't spam prompts
                if not getattr(self, "_update_prompt_shown", False):
                    self._update_prompt_shown = True
                    # Force hide splash so user sees the message box
                    self.hide_splash()
                    
                    res = messagebox.askyesno("Actualización Detectada", 
                                            "¡Hola! Hay una nueva versión disponible.\n\n"
                                            "¿Quieres actualizar ahora?\n"
                                            "(El bot se reiniciará solo)")
                    if res:
                        self._apply_binary_update()
                    else:
                        self._update_prompt_shown = False # Reset if rejected
            
            self.after(100, show_update_prompt)
        
        if "actualizado" in message or "Sistema al día" in message:
            try:
                from services.manager import reload_services
                # reload_services() 
            except: pass
            self.after(500, self.populate_services)

    def _apply_binary_update(self):
        try:
            if self.updater:
                self.updater.trigger_restart()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo reiniciar: {e}")

    def manual_update_check(self):
        print("ℹ️ Buscando actualizaciones manuales...")
        self.updater.check_for_updates(callback=self._on_update_check_done)

    def mark_email_modified(self, event):
        self.email_modified = True

    def update_email(self, event):
        if self.email_modified: return
        
        name = self.entry_name.get().strip().replace(" ", "").lower()
        surname = self.entry_surname.get().strip().replace(" ", "").lower()
        
        # Simple sanitization
        import re
        name = re.sub(r'[^a-z0-9]', '', name)
        surname = re.sub(r'[^a-z0-9]', '', surname)
        
        if name or surname:
            generated = f"{name}{surname}@gmail.com"
            self.entry_email.delete(0, 'end')
            self.entry_email.insert(0, generated)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def update_turbo_desc(self, value):
        threads = int(value)
        if threads == 1:
            self.turbo_desc.configure(text="1 Hilo (Seguro)", text_color="gray50")
        elif threads <= 3:
            self.turbo_desc.configure(text=f"{threads} Hilos (Rápido)", text_color="#2ecc71")
        elif threads <= 6:
            self.turbo_desc.configure(text=f"{threads} Hilos (Avanzado)", text_color="#f1c40f")
        else:
            self.turbo_desc.configure(text=f"{threads} Hilos (CAOS/TURBO)", text_color="#e74c3c")

    def toggle_matrix_theme(self):
        is_matrix = self.matrix_switch.get() == 1
        if is_matrix:
            # Matrix Colors
            ctk.set_appearance_mode("Dark")
            self.configure(fg_color="#000000")
            self.sidebar_frame.configure(fg_color="#001a00")
            self.main_frame.configure(fg_color="#000500")
            self.log_box.configure(text_color="#00ff41", fg_color="#001100")
            self.btn_start.configure(fg_color="#003300", hover_color="#005500", text_color="#00ff41")
            self.title_label.configure(text_color="#00ff41")
            print("👁️ MODO MATRIX ACTIVADO...")
        else:
            # Standard Colors
            self.configure(fg_color=["#f0f2f5", "#1a1a2e"])
            self.sidebar_frame.configure(fg_color="#0f0f15")
            self.main_frame.configure(fg_color="#16161d")
            self.log_box.configure(text_color="white", fg_color="#1a1a2e")
            self.btn_start.configure(fg_color="#ff0055", hover_color="#d90048", text_color="white")
            self.title_label.configure(text_color="white")
            print("🔄 Volviendo a interfaz estándar.")

    def toggle_remote_control(self):
        from core.telegram_control import TelegramController
        token = self.tg_token.get().strip()
        chat_id = self.tg_chat_id.get().strip()
        
        if not token or not chat_id:
            print("❌ Error: Proporciona Token y Chat ID para el control remoto.")
            return

        if not self.tg_controller:
            self.tg_controller = TelegramController(token, chat_id, self.telegram_callback)
            self.tg_controller.start()
            self.btn_remote.configure(text="🟢 CONTROL REMOTO ON", fg_color="#2ecc71")
        else:
            self.tg_controller.stop()
            self.tg_controller = None
            self.btn_remote.configure(text="🤖 ACTIVAR CONTROL REMOTO", fg_color="#8e44ad")
            print("🔴 Control remoto desactivado.")

    def telegram_callback(self, command, data=None):
        """Bridge between TelegramController and GUI"""
        if command == "status":
            stats = f"📊 *Estado Actual*\n🚀 Hilos: {int(self.turbo_slider.get())}\n✅ Éxitos: {self.total_success}\n❌ Fallos: {self.total_error}"
            self.tg_controller.send_response(stats)
        elif command == "start":
            phone = data
            self.entry_phone.delete(0, 'end')
            self.entry_phone.insert(0, phone)
            self.after(0, self.start_process)
            self.tg_controller.send_response(f"🚀 Iniciando ataque remoto a `{phone}`...")
        elif command == "stop":
            self.after(0, self.stop_process)
            self.tg_controller.send_response("🛑 Deteniendo operación...")

    def scrape_new_proxies(self):
        def _scrape():
            print("🌐 Iniciando descarga de proxies frescos...")
            self.btn_scrape_proxies.configure(state="disabled", text="⏳ DESCARGANDO...")
            try:
                # Assuming scrape_proxies saves to 'proxies.txt'
                count = scrape_proxies()
                print(f"✅ Descarga completada: {count} proxies guardados en 'proxies.txt'.")
            except Exception as e:
                print(f"⚠️ Error al descargar proxies: {e}")
            self.btn_scrape_proxies.configure(state="normal", text="🌐 DESCARGAR PROXIES")
        
        threading.Thread(target=_scrape, daemon=True).start()

    def change_mode_event(self, new_mode: str):
        desc = ""
        if "Automático" in new_mode:
            desc = "Secuencial. Uno tras otro. Seguro."
        elif "Porculero" in new_mode:
            desc = "Multihilo. Varios a la vez. Caos."
        elif "Nocturno" in new_mode:
            desc = "Solo servicios 24h. Ideal madrugada."
        elif "Contrareembolso" in new_mode:
            desc = "Envíos físicos a domicilio."
        elif "OSINT" in new_mode:
            desc = "Extrae info, ubicación y spam del número."
            # OSINT Mode Cleanup
            self.Target_label.configure(text="INVESTIGACIÓN OSINT", text_color="#f1c40f")
            self.Target_desc.configure(text="El Nombre sirve como 'Pista' para verificar perfiles sociales.")
            self.btn_start.configure(text="BUSCAR INFORMACIÓN", fg_color="#f1c40f", hover_color="#d4ac0d")
            self.entry_name.configure(placeholder_text="Pista de Nombre (Xavier, etc.)")
            
            # Hide irrelevant fields but KEEP name for hints
            self.entry_name.grid()
            self.entry_surname.grid_remove()
            self.entry_email.grid_remove()
            self.entry_zip.grid_remove()
        
        # Restore defaults if not OSINT
        if "OSINT" not in new_mode:
            self.Target_label.configure(text="DATOS DEL OBJETIVO", text_color="#ff4500")
            self.Target_desc.configure(text="Información de la víctima para los formularios")
            self.btn_start.configure(text="INICIAR ATAQUE", fg_color="#e74c3c", hover_color="#c0392b")
            self.entry_name.configure(placeholder_text="Nombre")
            
            # Show fields
            self.entry_name.grid()
            self.entry_surname.grid()
            self.entry_email.grid()
            self.entry_zip.grid()
        
        self.mode_desc.configure(text=desc)

    def get_user_data(self):
        return {
            'phone': self.entry_phone.get(),
            'name': self.entry_name.get(),
            'surname': self.entry_surname.get(),
            'email': self.entry_email.get(),
            'zipcode': self.entry_zip.get(),
            # Add placeholders for optional physical address if needed
            'address': 'Calle Falsa 123',
            'city': 'Madrid',
            'province': 'Madrid'
        }

    def get_favorites_path(self):
        # Persistence Fix (v2.2.21): 
        # Always store targets.json next to the executable/script, NOT in Temp
        try:
            if hasattr(sys, 'frozen'):
                # Running as PyInstaller EXE
                base_path = os.path.dirname(sys.executable)
            else:
                # Running as script
                base_path = os.path.dirname(os.path.abspath(__file__))
        except:
            base_path = os.path.abspath(".")
            
        return os.path.join(base_path, "targets.json")

    def refresh_favorites_menu(self):
        path = self.get_favorites_path()
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    targets = json.load(f)
                names = [t.get('phone', 'N/A') + " - " + t.get('name', 'Sin Nombre') for t in targets]
                if names:
                    self.fav_option.configure(values=["--- Seleccionar ---"] + names)
                else:
                    self.fav_option.configure(values=["--- Seleccionar ---"])
            except:
                self.fav_option.configure(values=["Error al cargar"])

    def save_favorite(self):
        data = self.get_user_data()
        if not data['phone']:
            print("ERROR: Ingrese al menos un teléfono para guardar.")
            return
            
        path = self.get_favorites_path()
        targets = []
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    targets = json.load(f)
            except: targets = []
            
        # Check if already exists (by phone)
        targets = [t for t in targets if str(t.get('phone')) != str(data['phone'])]
        targets.insert(0, data)
        
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(targets[:50], f, indent=4, ensure_ascii=False) # Keep latest 50
            print(f"✅ Objetivo {data['phone']} guardado en favoritos.")
            self.refresh_favorites_menu()
        except Exception as e:
            print(f"❌ Error al guardar favorito: {e}")

    def load_favorite_event(self, selection):
        if selection == "--- Seleccionar ---": return
        
        phone = selection.split(" - ")[0].strip()
        path = self.get_favorites_path()
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    targets = json.load(f)
                for t in targets:
                    if str(t.get('phone')) == phone:
                        self.entry_phone.delete(0, 'end')
                        self.entry_phone.insert(0, t.get('phone', ''))
                        self.entry_name.delete(0, 'end')
                        self.entry_name.insert(0, t.get('name', ''))
                        self.entry_surname.delete(0, 'end')
                        self.entry_surname.insert(0, t.get('surname', ''))
                        self.entry_email.delete(0, 'end')
                        self.entry_email.insert(0, t.get('email', ''))
                        self.entry_zip.delete(0, 'end')
                        self.entry_zip.insert(0, t.get('zipcode', ''))
                        print(f"📂 Datos cargados para: {phone}")
                        break
            except Exception as e:
                print(f"❌ Error al cargar favorito: {e}")

    def start_process(self):
        if self.running: return
        
        data = self.get_user_data()
        if not data['phone']:
            print("ERROR: El teléfono es obligatorio.")
            return

        self.running = True
        self.btn_start.configure(state="disabled", fg_color="gray")
        self.btn_stop.configure(state="normal", fg_color="#c0392b") # Dark red
        self.entry_phone.configure(state="disabled")
        
        # Reset Progress
        self.progress_bar.set(0)
        self.progress_label.configure(text="Iniciando motores...")
        
        mode = self.mode_option.get()
        print(f"--- Iniciando modo: {mode} ---")
        
        self.worker_thread = threading.Thread(target=self.run_logic, args=(mode, data))
        self.worker_thread.start()

    def load_batch_file(self):
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as f:
                phones = [line.strip() for line in f if line.strip()]
            self.batch_targets = phones
            print(f"📁 Cargada lista con {len(phones)} números.")
            self.progress_label.configure(text=f"Lista cargada: {len(phones)} números")

    def normalize_batch_phones(self):
        import re
        if not self.batch_targets:
            print("❌ Carga una lista (.txt) primero para normalizar.")
            return
        
        normalized = []
        for p in self.batch_targets:
            # Basic cleanup: remove spaces, dashes, dots
            clean = re.sub(r'[\s\-\.]', '', p)
            # If length is 9, assume Spanish and add +34 if missing
            if len(clean) == 9 and clean.startswith(('6', '7')):
               clean = "+34" + clean
            normalized.append(clean)
        
        self.batch_targets = normalized
        print(f"✅ Normalizados {len(normalized)} números.")
        self.progress_label.configure(text=f"Lista normalizada: {len(normalized)} números")

    def update_stats(self, success, error):
        self.total_success += success
        self.total_error += error
        self.after(0, lambda: self.label_success.configure(text=f"✅ {self.total_success}"))
        self.after(0, lambda: self.label_error.configure(text=f"❌ {self.total_error}"))
        
        # Update Chaos Meter (0 to 1 based on activity, capped at 100 attempts for full bar)
        total = self.total_success + self.total_error
        chaos = min(total / 100, 1.0)
        self.after(0, lambda: self.chaos_bar.set(chaos))

    def update_stealth_desc(self, value):
        texts = ["Rápido (Riesgo)", "Equilibrado", "Lento (Ultra Sigilo)"]
        self.stealth_desc.configure(text=texts[int(value)])

    def populate_services(self):
        from services.manager import SERVICE_CLASSES
        for cls in SERVICE_CLASSES:
            var = ctk.BooleanVar(value=True)
            cb = ctk.CTkCheckBox(self.serv_frame, text=cls.__name__, variable=var, font=ctk.CTkFont(size=10))
            cb.pack(fill="x", padx=5, pady=2)
            self.service_vars[cls.__name__] = var

    def select_all_services(self):
        for var in self.service_vars.values():
            var.set(True)
        print("✅ Todos los servicios seleccionados.")

    def select_none_services(self):
        for var in self.service_vars.values():
            var.set(False)
        print("❌ Todos los servicios desmarcados.")

    def autofill_data(self):
        import random
        names = ["Juan", "Maria", "Carlos", "Ana", "Pedro", "Lucia", "Diego", "Elena"]
        surnames = ["Garcia", "Rodriguez", "Lopez", "Perez", "Gonzalez", "Sanchez", "Martinez"]
        domains = ["gmail.com", "hotmail.com", "outlook.es", "yahoo.es"]
        
        name = random.choice(names)
        surname = random.choice(surnames)
        email = f"{name.lower()}.{surname.lower()}{random.randint(10,99)}@{random.choice(domains)}"
        
        self.entry_name.delete(0, 'end')
        self.entry_name.insert(0, name)
        self.entry_surname.delete(0, 'end')
        self.entry_surname.insert(0, surname)
        self.entry_email.delete(0, 'end')
        self.entry_email.insert(0, email)
        print(f"✨ Datos auto-rellenados: {name} {surname}")

    def clear_history(self):
        history_path = "history.json"
        if os.path.exists(history_path):
            try:
                os.remove(history_path)
                print("🗑️ Historial de envíos limpiado.")
            except Exception as e:
                print(f"⚠️ Error al limpiar historial: {e}")
        else:
            print("ℹ️ El historial ya está vacío.")

    def export_log(self):
        from tkinter import filedialog
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                 filetypes=[("Text files", "*.txt")],
                                                 initialfile="perubianbot_log.txt")
        if file_path:
            try:
                log_content = self.log_box.get("1.0", "end")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(log_content)
                print(f"💾 Log exportado correctamente a: {file_path}")
            except Exception as e:
                print(f"❌ Error al exportar log: {e}")

    def open_logs_folder(self):
        """Open the logs directory in system explorer"""
        if not os.path.exists("logs"):
            os.makedirs("logs")
        try:
            os.startfile("logs")
        except:
            print("⚠️ No se pudo abrir la carpeta de logs automáticamente.")

    def cleanup_temp(self):
        """Removes temporary files like proxies.txt or debug logs"""
        if os.path.exists("proxies.txt"):
            os.remove("proxies.txt")
        print("🧹 Archivos temporales eliminados.")
        self.progress_label.configure(text="Limpieza completada")

    def check_updates(self):
        # This is now handled by the new ServiceUpdater called via btn_update
        self.manual_update_check()

    def populate_services(self):
        # Clear existing
        for cb in self.service_checkboxes.values():
            try: cb.destroy()
            except: pass
        self.service_vars.clear()
        self.service_checkboxes.clear()

        from services.manager import SERVICE_CLASSES
        for cls in SERVICE_CLASSES:
            var = ctk.BooleanVar(value=True)
            cb = ctk.CTkCheckBox(self.serv_frame, text=cls.__name__, variable=var, font=ctk.CTkFont(size=10))
            cb.pack(fill="x", padx=5, pady=2)
            self.service_vars[cls.__name__] = var
            self.service_checkboxes[cls.__name__] = cb

    def filter_services(self, *args):
        query = self.search_var.get().lower()
        for name, cb in self.service_checkboxes.items():
            if query in name.lower():
                cb.pack(fill="x", padx=5, pady=2)
            else:
                cb.pack_forget()

    def stop_process(self):
        if not self.running: return
        print("--- Deteniendo... (Puede tardar unos segundos en cerrar navegadores) ---")
        self.finish_process()

    def finish_process(self):
        def _safe_finish():
            self.running = False
            self.btn_start.configure(state="normal", fg_color="#e74c3c")
            self.entry_phone.configure(state="normal")
            self.progress_bar.set(0)
            self.progress_label.configure(text="Preparado para el siguiente objetivo")
            print("--- Fin del proceso ---")
            self.auto_save_log()
        
        self.after(0, _safe_finish)

    def auto_save_log(self):
        """Automatically saves log to 'logs' directory. Must be called from main thread."""
        if not os.path.exists("logs"):
            os.makedirs("logs")
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"logs/sesion_{timestamp}.txt"
        try:
            # Tkinter access must be on main thread
            log_content = self.log_box.get("1.0", "end")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(log_content)
            print(f"📊 Registro de sesión auto-guardado en: {filename}")
        except Exception as e:
            print(f"⚠️ Error al auto-guardar log: {e}")

    def update_progress_ui(self, current, total, msg):
        """Called from worker thread to update UI.
           Signature matches manager.py: (current_step, total_steps, message_string)
        """
        try:
            percentage = current / total if total > 0 else 0
        except: percentage = 0
        
        self.after(0, lambda: self.progress_bar.set(percentage))
        self.after(0, lambda: self.progress_label.configure(text=f"[{current}/{total}] {msg}"))

    def run_logic(self, mode, data):
        try:
            targets = [data]
            if self.batch_targets:
                # If batch is loaded, use those phones instead of the single entry
                targets = []
                for phone in self.batch_targets:
                    new_data = data.copy()
                    new_data['phone'] = phone
                    targets.append(new_data)
                self.batch_targets = [] # Reset after reading

            total_targets = len(targets)
            for target_idx, current_target in enumerate(targets, 1):
                if not self.running: break
                
                print(f"\n🚀 Procesando objetivo {target_idx}/{total_targets}: {current_target['phone']}")
                
                # Force Chrome for OSINT to use selenium-stealth effectively
                is_osint = ("OSINT" in mode)
                use_auto_proxy = self.proxy_switch.get() == 1
                stealth_level = int(self.stealth_slider.get())
                max_threads = int(self.turbo_slider.get())
                ua_choice = self.ua_option.get()
                use_headless = self.ghost_switch.get() == 1
                
                # Map UA choice to actual string or type
                custom_ua = None
                if "iPhone" in ua_choice:
                    custom_ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/04.1"
                elif "Android" in ua_choice:
                    custom_ua = "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36"
                
                # Filter services based on selection
                selected_services = [name for name, var in self.service_vars.items() if var.get()]
                
                # Lazy import ServiceManager
                from services.manager import ServiceManager
                
                # Pass auto_proxy, stealth and turbo to manager
                manager = ServiceManager(current_target, 
                                         progress_callback=self.update_progress_ui, 
                                         force_chrome=is_osint, 
                                         auto_proxy=use_auto_proxy,
                                         stealth_level=stealth_level,
                                         enabled_services=selected_services,
                                         max_threads=max_threads,
                                         user_agent=custom_ua,
                                         stop_check_callback=lambda: not self.running,
                                         headless=use_headless)
                
                if is_osint:
                    manager.run_osint(current_target['phone'])
                elif "Automático" in mode:
                    manager.run_auto()
                elif "Porculero" in mode:
                    manager.run_porculero()
                elif "Nocturno" in mode:
                    manager.run_nocturno()
                elif "Contrareembolso" in mode:
                    manager.run_contrareembolso()
                elif "OSINT" in mode:
                    manager.run_osint(current_target['phone'])
                
                # Update global stats
                self.update_stats(manager.stats['success'], manager.stats['error'])
                
            # Send Telegram Report if configured
            token = self.tg_token.get().strip()
            chat_id = self.tg_chat_id.get().strip()
            if token and chat_id:
                try:
                    from core.notifications import TelegramNotifier
                    notifier = TelegramNotifier(token, chat_id)
                    # For batch mode, we send a summary of the whole session
                    summary_stats = {'success': self.total_success, 'error': self.total_error, 'skipped': 0}
                    final_phone = data['phone'] if not self.batch_targets else "Multi-Objetivo"
                    notifier.send_report(summary_stats, final_phone, mode)
                    print("✅ Notificación de Telegram enviada.")
                except Exception as e:
                    print(f"⚠️ Error enviando reporte Telegram: {e}")
                
        except Exception as e:
            print(f"CRITICAL ERROR: {e}")
        finally:
            self.after(0, self.finish_process)

if __name__ == "__main__":
    try:
        app = OsintGUI()
        app.mainloop()
    except Exception as e:
        # Emergency error logging
        with open("STARTUP_CRASH.txt", "w") as f:
            import traceback
            traceback.print_exc(file=f)
        
        # Try to show message if possible
        try:
            import tkinter.messagebox
            tkinter.messagebox.showerror("Critical Error", f"Failed to start:\n{e}")
        except: pass
        
        # Original FATAL_ERROR handling for other exceptions during mainloop
        import traceback
        import os
        with open("FATAL_ERROR.txt", "w", encoding="utf-8") as f:
            f.write("--- CRASH REPORT ---\n")
            f.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Error: {e}\n\n")
            f.write(traceback.format_exc())
        print(f"❌ ERROR CRÍTICO DETECTADO. Detalles guardados en FATAL_ERROR.txt")
        # Final emergency alert
        try:
            from tkinter import messagebox
            import tkinter as tk
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Error Crítico de Aplicación", 
                                f"Se ha producido un error inesperado:\n\n{e}\n\n"
                                "Revisa FATAL_ERROR.txt para más detalles.")
        except:
            pass
