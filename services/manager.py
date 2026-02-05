import os
import sys
import time
import importlib
import pkgutil
import inspect
from concurrent.futures import ThreadPoolExecutor
from services.base_service import ServiceType, BaseService
from core.browser import BrowserManager
from core.osint import OSINTManager
from core.updater import ServiceUpdater
from core.captcha import LocalCaptchaSolver

# Dynamic Base Path for robust file discovery
if getattr(sys, 'frozen', False):
    EXE_DIR = os.path.dirname(sys.executable)
else:
    EXE_DIR = os.getcwd()

def discover_services():
    """Dynamically discover all service classes in the definitions package."""
    service_classes = []
    try:
        import services.definitions as definitions
        # 1. Get the bundled path (inside EXE/_MEIPASS)
        paths = getattr(definitions, '__path__', [])
        
        # 2. Add local path (next to EXE/Script) for updates/overrides
        local_path = os.path.join(EXE_DIR, "services", "definitions")
        if os.path.exists(local_path) and local_path not in paths:
            paths.append(local_path)
            # Ensure the local directory's parent is in sys.path so imports work
            if EXE_DIR not in sys.path:
                sys.path.insert(0, EXE_DIR)
        
        print(f"SISTEMA: Escaneando servicios en: {paths}")
        
        # Iterate through all modules in the paths
        for loader, module_name, is_pkg in pkgutil.iter_modules(paths):
            if module_name == "__init__": continue
            
            full_module_name = f"services.definitions.{module_name}"
            try:
                # print(f"DEBUG: Scrying {full_module_name}") # Minimal spam
                # Reload if already loaded to pick up changes
                if full_module_name in sys.modules:
                    importlib.reload(sys.modules[full_module_name])
                    module = sys.modules[full_module_name]
                else:
                    module = importlib.import_module(full_module_name)
                
                # Find all classes that inherit from BaseService
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, BaseService) and obj is not BaseService:
                        if obj not in service_classes:
                            service_classes.append(obj)
            except Exception as e:
                print(f"ERROR: Could not load module {full_module_name}: {e}")
    except Exception as e:
        print(f"CRITICAL ERROR in discovery: {e}")
    
    # Trace completion
    try:
        if hasattr(sys, '_MEIPASS'):
            log_dir = os.path.dirname(sys.executable)
        else:
            log_dir = os.path.abspath(".")
        log_path = os.path.join(log_dir, "DEBUG_BOOT.txt")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{time.strftime('%H:%M:%S')}] Services discovered: {len(service_classes)}\n")
    except: pass
    return service_classes

# Initial discovery
SERVICE_CLASSES = discover_services()

def reload_services():
    """Forces a re-scan of the services directory."""
    global SERVICE_CLASSES
    SERVICE_CLASSES = discover_services()
    return SERVICE_CLASSES

class ServiceManager:
    def __init__(self, user_data, progress_callback=None, force_chrome=False, auto_proxy=False, stealth_level=1, enabled_services=None, max_threads=1, user_agent=None, stop_check_callback=None, headless=False):
        self.user_data = user_data
        self.progress_callback = progress_callback
        self.force_chrome = force_chrome
        self.auto_proxy = auto_proxy
        self.stealth_level = stealth_level
        self.max_threads = max_threads
        self.user_agent = user_agent
        self.stop_check_callback = stop_check_callback # NEW: Stop signal
        self.headless = headless # NEW: Ghost Mode
        self.browser_manager = BrowserManager(headless=self.headless, auto_proxy=self.auto_proxy, user_agent=self.user_agent, stop_check=self.stop_check_callback)
        self.browser = self.browser_manager.get_driver(force_chrome=force_chrome)
        self.osint_manager = OSINTManager()
        self.updater = ServiceUpdater()
        self.captcha_solver = LocalCaptchaSolver()
        self.stats = {'success': 0, 'error': 0, 'skipped': 0}
        self.lock = None # Will be initialized for parallel mode
        
        # Check for updates on init
        self.updater.check_for_updates()

        # Instantiate only selected services
        if enabled_services is not None:
            self.service_classes = [cls for cls in SERVICE_CLASSES if cls.__name__ in enabled_services]
        else:
            self.service_classes = SERVICE_CLASSES
            
        self.services = []
        # In parallel mode, we instantiate inside the worker
        if self.max_threads == 1:
            for cls in self.service_classes:
                svc = cls(self.browser, self.user_data)
                svc.stealth_level = self.stealth_level
                self.services.append(svc)

    def run_auto(self):
        """Sequential or Parallel execution based on max_threads"""
        try:
            if self.max_threads > 1:
                self.run_turbo()
            else:
                self._run_sequential()
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"\n[ERROR EN MODO AUTO] {e}")
            input("Presione ENTER para volver al menú...")
        except KeyboardInterrupt:
            print("\nDetenido por el usuario.")
            input("Presione ENTER para continuar...")

    def _run_sequential(self):
        try:
            print(f"Starting Auto Mode (Sequential) - {len(self.services)} services.")
            total_services = len(self.services)
            for i, service_instance in enumerate(self.services, 1):
                # STOP CHECK
                if self.stop_check_callback and self.stop_check_callback():
                    print("🛑 DETENIDO POR EL USUARIO.")
                    break

                if self.progress_callback:
                    self.progress_callback(i, total_services, service_instance.name)
                
                print(f"Running {service_instance.name}...")
                
                # Smart Retry Logic (max 2 attempts)
                success = False
                for attempt in range(1, 3):
                    try: 
                        self.browser.delete_all_cookies()
                    except: pass
                    
                    try:
                        if attempt > 1:
                            print(f"  🔄 Reintentando {service_instance.name} (Intento {attempt})...")
                            time.sleep(random.uniform(2, 5))
                            
                        service_instance.run()
                        
                        # Verify actual success if not already marked as OK
                        if getattr(service_instance, 'status', None) != 'ERROR':
                            if service_instance.verify_success():
                                service_instance.status = 'OK'
                                success = True
                                break
                            else:
                                if attempt == 1:
                                    print(f"  ⚠️ No se detectó mensaje de éxito. Reintentando...")
                                    continue
                    except Exception as e:
                        print(f"  ❌ Error en intento {attempt}: {e}")
                
                if success or getattr(service_instance, 'status', None) == 'OK':
                    self.stats['success'] += 1
                elif getattr(service_instance, 'status', None) == 'WARN':
                    self.stats['skipped'] += 1
                else:
                    self.stats['error'] += 1

            self.print_summary()
            self.browser_manager.close()
        except Exception as e:
            print(f"Error general: {e}")
            input("Presione ENTER para continuar...")

    def run_turbo(self):
        """Parallel execution using multiple headless browsers"""
        import threading
        from concurrent.futures import ThreadPoolExecutor
        self.lock = threading.Lock()
        total_services = len(self.service_classes)
        print(f"🚀 MODO TURBO ACTIVADO: {self.max_threads} hilos para {total_services} servicios.")
        
        # Helper function for thread worker
        def worker(ServiceClass, index):
             mgr = BrowserManager(headless=True, auto_proxy=self.auto_proxy, user_agent=self.user_agent)
             driver = mgr.get_driver(force_chrome=self.force_chrome)
             try:
                 service = ServiceClass(driver, self.user_data)
                 service.stealth_level = self.stealth_level
                 if self.progress_callback:
                     self.progress_callback(index, total_services, service.name)
                 
                 print(f"[Turbo-{index}] Ejecutando {service.name}...")
                 
                 # Smart Retry Logic in Turbo Mode
                 success = False
                 for attempt in range(1, 3):
                     try:
                         if attempt > 1:
                             time.sleep(random.uniform(2, 5))
                         service.run()
                         if getattr(service, 'status', None) != 'ERROR':
                             if service.verify_success():
                                 service.status = 'OK'
                                 success = True
                                 break
                     except: pass

                 with self.lock:
                     if success or getattr(service, 'status', None) == 'OK': self.stats['success'] += 1
                     elif getattr(service, 'status', None) == 'ERROR': self.stats['error'] += 1
                     elif getattr(service, 'status', None) == 'WARN': self.stats['skipped'] += 1
             except Exception as e:
                 print(f"[Turbo] Error en {ServiceClass.__name__}: {e}")
                 with self.lock: self.stats['error'] += 1
             finally:
                 mgr.close()

        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            for i, cls in enumerate(self.service_classes, 1):
                executor.submit(worker, cls, i)

        self.print_summary()
        self.browser_manager.close()

    def run_porculero(self):
        """Parallel execution (Chaos Mode)"""
        print(f"Starting Porculero Mode (Parallel) - Running {len(SERVICE_CLASSES)} services.")

        # Helper function for thread worker
        def worker(ServiceClass):
             mgr = BrowserManager(headless=True)
             driver = mgr.get_driver()
             try:
                 service = ServiceClass(driver, self.user_data)
                 print(f"[Thread] Running {service.name}")
                 service.run()
             except Exception as e:
                 print(f"Thread Error: {e}")
             finally:
                 mgr.close()

        with ThreadPoolExecutor(max_workers=3) as executor:
            executor.map(worker, SERVICE_CLASSES)

    def run_nocturno(self):
        """Runs only services marked as NIGHT"""
        print("Starting Nocturno Mode...")
        self.stats = {'success': 0, 'error': 0, 'skipped': 0}
        
        filtered_services = [s for s in self.services if ServiceType.NIGHT in s.types]
        total = len(filtered_services)
        
        print(f"Executing {total} night services.")

        for i, service_instance in enumerate(filtered_services, 1):
            if self.progress_callback:
                self.progress_callback(i, total, service_instance.name)
            try:
                service_instance.run()
                if getattr(service_instance, 'status', None) == 'OK':
                    self.stats['success'] += 1
                elif getattr(service_instance, 'status', None) == 'ERROR':
                    self.stats['error'] += 1
                elif getattr(service_instance, 'status', None) == 'WARN':
                    self.stats['skipped'] += 1
            except Exception as e:
                self.stats['error'] += 1
                print(f"Error: {e}")

        self.print_summary()

        self.browser_manager.close()

    def run_contrareembolso(self):
        """Runs PHYSICAL services"""
        print("Starting Contrareembolso Mode...")
        
        filtered_services = [s for s in self.services if ServiceType.PHYSICAL in s.types]
        total = len(filtered_services)
        
        print(f"Executing {total} physical services.")

        for i, service_instance in enumerate(filtered_services, 1):
            if self.progress_callback:
                self.progress_callback(i, total, service_instance.name)
            try:
                service_instance.run()
                if getattr(service_instance, 'status', None) == 'OK':
                    self.stats['success'] += 1
                elif getattr(service_instance, 'status', None) == 'ERROR':
                    self.stats['error'] += 1
                elif getattr(service_instance, 'status', None) == 'WARN':
                    self.stats['skipped'] += 1
            except Exception as e:
                self.stats['error'] += 1
                print(f"Error: {e}")

        self.print_summary()

        self.browser_manager.close()

    def run_osint(self, phone):
        """Runs OSINT Manager and formats the report for output"""
        try:
            print(f"🔍 INICIANDO ESCANEO GOD MODE PARA: {phone}")
            # Try to get name hint from user_data
            name_hint = self.user_data.get('name') or self.user_data.get('nombre')
            
            # Pass progress_callback down for OSINT steps visibility
            report = self.osint_manager.lookup(self.browser_manager, 
                                             phone, 
                                             name_hint=name_hint,
                                             progress_callback=self.progress_callback,
                                             stop_check=self.stop_check_callback)
            
            final_report = self.osint_manager.format_report(report)
            
            # Print specifically to ensure it hits the GUI redirector with a highlight
            print("\n" + final_report + "\n")
            
            # Close browser 
            self.browser_manager.close()
            return report
        except Exception as e:
            print(f"❌ Error en OSINT: {e}")
            self.browser_manager.close()
            return None

    def print_summary(self):
        """Prints a high-visibility summary of the operation"""
        s = self.stats
        total = s['success'] + s['error'] + s['skipped']
        
        sep = "═" * 50
        
        summary = [
            "\n" + f"╔{sep}╗",
            f"║ ♈ RESUMEN DE OPERACIÓN - CARNEROSBOT              ║",
            f"╠{sep}╣",
            f"║ ✅ ÉXITOS      : {s['success']:30} ║",
            f"║ ❌ FALLOS      : {s['error']:30} ║",
            f"║ 🛡️ SALTADOS    : {s['skipped']:30} ║",
            f"╟──────────────────────────────────────────────────╢",
            f"║ 📊 TOTAL       : {total:30} ║",
            f"╚{sep}╝"
        ]
        print("\n".join(summary))
        if s['success'] > 0:
            print(f"🔥 ¡OPERACIÓN COMPLETADA CON ÉXITO! {s['success']} servicios activados.")
        else:
            print("⚠️ Operación finalizada sin éxitos confirmados.")
