import requests
import time
import threading

class TelegramController:
    def __init__(self, token, chat_id, app_callback):
        self.token = token
        self.chat_id = chat_id
        self.app_callback = app_callback # Function to call start/status in GUI
        self.running = False
        self.last_update_id = 0
        self.thread = None

    def start(self):
        if not self.token or not self.chat_id:
            print("⚠️ Telegram Controller: Faltan Token o Chat ID.")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()
        print("🤖 Controlador remoto de Telegram ACTIVADO.")

    def stop(self):
        self.running = False

    def _listen_loop(self):
        while self.running:
            try:
                url = f"https://api.telegram.org/bot{self.token}/getUpdates"
                params = {"offset": self.last_update_id + 1, "timeout": 20}
                r = requests.get(url, params=params, timeout=25)
                
                if r.status_code == 200:
                    updates = r.json().get("result", [])
                    for update in updates:
                        self.last_update_id = update["update_id"]
                        message = update.get("message", {})
                        text = message.get("text", "")
                        from_id = str(message.get("chat", {}).get("id", ""))
                        
                        if from_id == str(self.chat_id):
                            self._handle_command(text)
                
            except Exception as e:
                print(f"⚠️ Error en loop de Telegram: {e}")
                time.sleep(5)
            
            time.sleep(1)

    def _handle_command(self, text):
        text = text.strip()
        if text == "/status":
            self.app_callback("status")
        elif text == "/help":
            help_msg = (
                "🤖 *Mando a Distancia CarnerosBot*\n\n"
                "/status - Ver progreso actual\n"
                "/start <numero> - Iniciar ataque básico\n"
                "/stop - Detener ejecución actual"
            )
            self.send_response(help_msg)
        elif text.startswith("/start"):
            parts = text.split()
            if len(parts) > 1:
                phone = parts[1]
                self.app_callback("start", phone)
            else:
                self.send_response("❌ Uso: `/start 666111222`")
        elif text == "/stop":
            self.app_callback("stop")

    def send_response(self, message):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        data = {"chat_id": self.chat_id, "text": message, "parse_mode": "Markdown"}
        requests.post(url, data=data, timeout=10)
