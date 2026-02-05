import os
import sys
import telebot
from services.manager import ServiceManager

# Replace with your token or load from env
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "♈ CarnerosBot - Telegram Control\nUso: /ataque <telefono> <nombre>\nEj: /ataque 666111222 Juan")

@bot.message_handler(commands=['ataque'])
def handle_attack(message):
    try:
        args = message.text.split()
        if len(args) < 2:
            bot.reply_to(message, "❌ Falta el teléfono.")
            return
            
        phone = args[1]
        name = args[2] if len(args) > 2 else "Objetivo"
        
        user_data = {
            'phone': phone,
            'name': name,
            'surname': 'Bot',
            'email': f"{name.lower()}@gmail.com",
            'zipcode': '28013'
        }
        
        bot.reply_to(message, f"🚀 Iniciando ataque automático a {phone}...")
        
        # We run in a separate process or thread if we want it non-blocking
        # For simplicity, we just trigger manager here
        manager = ServiceManager(user_data)
        manager.run_auto()
        
        bot.send_message(message.chat.id, f"✅ Ataque completado a {phone}.")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")

if __name__ == '__main__':
    print("Telegram Bot: Escuchando órdenes...")
    # bot.infinity_polling() # Uncomment to run
