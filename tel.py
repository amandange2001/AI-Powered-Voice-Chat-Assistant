import requests

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from dotenv import load_dotenv

import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ==========================================
# CHANGED sendMessage → sendPhoto
# ==========================================

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

# ==========================================
# SEND TELEGRAM MESSAGE
# ==========================================

def send_telegram_message(data):

    visitor_id = data["visitor_id"]

    visitor_name = data["visitor_name"]

    mobile = data["mobile"]

    company_name = data["company_name"]

    visit_purpose = data["visit_purpose"]

    meeting_with = data["meeting_with"]

    chat_id = data["chat_id"]

    # ==========================================
    # NEW PHOTO URL PARAMETER
    # ==========================================

    photo_url = data["photo_url"]

    # ==========================================
    # INLINE BUTTONS
    # ==========================================

    keyboard = {

        "inline_keyboard": [

            [

                {

                    "text": "✅ Approve",

                    "callback_data": f"approve_{visitor_id}"

                },

                {

                    "text": "❌ Reject",

                    "callback_data": f"reject_{visitor_id}"

                }
            ]
        ]
    }

    # ==========================================
    # TELEGRAM MESSAGE
    # ==========================================

    message = f"""
🚨 NEW VISITOR REQUEST

🆔 Visitor ID: {visitor_id}

👤 Visitor Name: {visitor_name}

🏢 Company: {company_name}

📞 Mobile: {mobile}

📌 Purpose: {visit_purpose}

👨 Meeting With: {meeting_with}
"""

    payload = {

        "chat_id": telegram_chat_id,

        # ==========================================
        # SEND PHOTO
        # ==========================================

        "photo": photo_url,

        # ==========================================
        # MESSAGE AS CAPTION
        # ==========================================

        "caption": message,

        "reply_markup": keyboard
    }

    response = requests.post(

        TELEGRAM_API,

        json=payload
    )

    return response.json()