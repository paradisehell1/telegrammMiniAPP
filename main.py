from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
import time

BOT_TOKEN = ""
MINI_APP_URL = ""

bot = TeleBot(BOT_TOKEN)

# Команда /start
@bot.message_handler(commands=["start"])
def start(message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    web_app = WebAppInfo(url=MINI_APP_URL)
    button = KeyboardButton(text="🍽 Открыть Mini App", web_app=web_app)
    kb.add(button)

    bot.send_message(
        message.chat.id,
        "Панель сотрудников ресторана 👇",
        reply_markup=kb
    )
@bot.message_handler(func=lambda m: True)
def handle_webapp_data(message):
    import json
    try:
        data = json.loads(message.text)
        if data.get("type") == "auth_request":
            # Telegram присылает initData при отправке sendData
            print("Пользователь запросил авторизацию:", message.from_user)
    except Exception as e:
        print("Ошибка:", e)
# Бесконечный запуск polling с обработкой ошибок
def run_bot():
    while True:
        try:
            # Увеличенные таймауты long polling
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"Произошла ошибка polling: {e}")
            print("Перезапуск через 5 секунд...")
            time.sleep(5)

if __name__ == "__main__":
    run_bot()