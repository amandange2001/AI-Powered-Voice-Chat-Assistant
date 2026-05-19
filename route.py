from fastapi import APIRouter

from tel import send_telegram_message

router = APIRouter(

    prefix="/api/telegram",

    tags=["Telegram"]
)

# ==========================================
# SEND APPROVAL REQUEST
# ==========================================

@router.post("/send-approval")

async def send_approval(data: dict):

    response = send_telegram_message(data)

    return {

        "message": "Telegram approval sent",

        "telegram_response": response
    }