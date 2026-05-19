import requests

BOT_TOKEN = "8452900401:AAF_5HkYW7JGLY_EZ2LX9YQ3qZMMN1LN6-0"

CHAT_ID = "1024362622"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

payload = {

    "chat_id": CHAT_ID,

    "text": "✅ Visitor Management Telegram Bot Connected Successfully"
}

response = requests.post(url, json=payload)

print(response.json())