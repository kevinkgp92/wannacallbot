import requests

class TelegramNotifier:
    def __init__(self, token=None, chat_id=None):
        self.token = token
        self.chat_id = chat_id

    def send_message(self, message):
        """Sends a message to the configured Telegram chat."""
        if not self.token or not self.chat_id:
            return False

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        data = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        try:
            r = requests.post(url, data=data, timeout=10)
            return r.status_code == 200
        except Exception as e:
            print(f"⚠️ Error al enviar notificación de Telegram: {e}")
            return False

    def send_report(self, stats, phone, mode, location="Desconocida", carrier="Desconocido"):
        """Formats and sends a session summary report."""
        report = (
            f"♈ *RESUMEN DE OPERACIÓN - CARNEROSBOT*\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"📱 *Objetivo:* `{phone}`\n"
            f"📍 *Ubicación:* `{location}`\n"
            f"📡 *Operador:* `{carrier}`\n"
            f"⚙️ *Modo:* {mode}\n"
            f"✅ *Éxitos:* {stats['success']}\n"
            f"❌ *Fallos:* {stats['error']}\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"🔥 ¡Operación finalizada!"
        )
        return self.send_message(report)
