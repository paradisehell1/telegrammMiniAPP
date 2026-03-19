from telebot import TeleBot, apihelper
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
import time
import json
import logging

# ================= CONFIG =================
BOT_TOKEN = ""
MINI_APP_URL = ""


PROXY_URL = ""


# ==========================================

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


apihelper.proxy = {
    "http": PROXY_URL,
    "https": PROXY_URL,
}

# Создаем бота
bot = TeleBot(BOT_TOKEN)


# ================= HANDLERS =================

@bot.message_handler(commands=["start"])
def start(message):
    try:
        kb = ReplyKeyboardMarkup(resize_keyboard=True)

        web_app = WebAppInfo(url=MINI_APP_URL)
        button = KeyboardButton(
            text="Открыть заявки",
            web_app=web_app
        )
        kb.add(button)

        bot.send_message(
            message.chat.id,
            'Для просмотра заявок, нажмите на кнопку "Открыть заявки"',
            reply_markup=kb
        )

        logger.info(f"/start от {message.from_user.id}")

    except Exception as e:
        logger.error(f"Ошибка в /start: {e}")


@bot.message_handler(func=lambda m: True)
def handle_message(message):
    try:
        data = json.loads(message.text)

        # ================= НОВАЯ БРОНЬ =================
        if data.get("type") == "new_booking":
            booking = data.get("booking", {})

            text = (
                f"🍽 <b>Новая бронь!</b>\n\n"
                f"<b>Имя:</b> {booking.get('first_name')} {booking.get('last_name')}\n"
                f"<b>Телефон:</b> {booking.get('phone')}\n"
                f"<b>Гостей:</b> {booking.get('guests')}\n"
                f"<b>Зал:</b> {booking.get('hall')}\n"
                f"<b>Время:</b> {booking.get('booking_datetime')}\n"
                f"<b>Комментарий:</b> {booking.get('comments') or '—'}"
            )

            bot.send_message(
                message.chat.id,
                text,
                parse_mode="HTML"
            )

            logger.info(f"Новая бронь: {booking}")

        # ================= AUTH =================
        elif data.get("type") == "auth_request":
            logger.info(f"Auth request от {message.from_user.id}")

        else:
            logger.warning(f"Неизвестный тип сообщения: {data}")

    except json.JSONDecodeError:
        logger.warning(f"Не JSON сообщение: {message.text}")

    except Exception as e:
        logger.error(f"Ошибка обработки сообщения: {e}")


# ================= RUN =================

def run_bot():
    while True:
        try:
            logger.info("Бот запущен...")
            bot.infinity_polling(
                timeout=60,
                long_polling_timeout=60
            )

        except Exception as e:
            logger.error(f"Ошибка polling: {e}")
            time.sleep(5)


if __name__ == "__main__":
    run_bot()