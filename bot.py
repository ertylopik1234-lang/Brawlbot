import requests
import time

TOKEN = "8601549576:AAHLJF0oPN6Sx6jQRpfuHz-Stl3Fri_6LxI"
ADMIN = 8744429026
last = 0

print("✅ Бот запущен (тестовая версия)")

while True:
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={last+1}&timeout=10"
        data = requests.get(url).json()
        
        for update in data.get("result", []):
            last = update["update_id"]
            message = update.get("message", {})
            chat_id = message.get("chat", {}).get("id")
            text = message.get("text", "")
            
            if text == "/start" and str(chat_id) == str(ADMIN):
                send_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                send_data = {"chat_id": chat_id, "text": "✅ Бот работает"}
                requests.post(send_url, json=send_data)
                print(f"Ответ отправлен админу {chat_id}")
        
        time.sleep(1)
        
    except Exception as e:
        print(f"Ошибка в цикле: {e}")
        time.sleep(5)
