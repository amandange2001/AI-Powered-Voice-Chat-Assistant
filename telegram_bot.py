from telegram import Update

from telegram.ext import (
    Application,
    CallbackContext,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from database import get_db_connection

from dotenv import load_dotenv

import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ==========================================
# TEMP STATES
# ==========================================

pending_rejections = {}

# ==========================================
# BUTTON CLICK HANDLER
# ==========================================

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    callback_data = query.data

    action, visitor_id = callback_data.split("_")

    conn = get_db_connection()

    cursor = conn.cursor()

    try:

        # ==========================================
        # CHECK STATUS
        # ==========================================

        cursor.execute("""

            SELECT status,
                   visitor_name,
                   company_name,
                   mobile,
                   meeting_with

            FROM visitors

            WHERE visitor_id=%s

        """, (visitor_id,))

        visitor = cursor.fetchone()

        if not visitor:

            await query.message.reply_text(
                "❌ Visitor not found"
            )

            return

        if visitor["status"].upper() != "PENDING":

            await query.message.reply_text(
                "⚠ This request has already been processed"
            )

            return

        # ==========================================
        # APPROVE FLOW
        # ==========================================

        if action == "approve":

            cursor.execute("""

                UPDATE visitors

                SET status='APPROVED'

                WHERE visitor_id=%s

            """, (

                visitor_id,
            ))

            conn.commit()

            await query.message.reply_text(

                f"""
✅ VISITOR APPROVED

🆔 Visitor ID: {visitor_id}

👤 Visitor Name: {visitor['visitor_name']}

🏢 Company: {visitor['company_name']}

📞 Mobile: {visitor['mobile']}

👨 Meeting With: {visitor['meeting_with']}
"""
            )

            print(f"Visitor {visitor_id} APPROVED")

        # ==========================================
        # REJECT FLOW
        # ==========================================

        elif action == "reject":

            pending_rejections[
                query.from_user.id
            ] = visitor_id

            await query.message.reply_text(

                f"""
❌ Please enter rejection reason

🆔 Visitor ID: {visitor_id}
"""
            )

    except Exception as e:

        print("ERROR:", e)

        await query.message.reply_text(
            "❌ Something went wrong"
        )

    finally:

        cursor.close()

        conn.close()

# ==========================================
# HANDLE REJECTION REASON
# ==========================================

async def handle_rejection_reason(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.message.from_user.id

    if user_id not in pending_rejections:

        return

    visitor_id = pending_rejections[user_id]

    rejection_reason = update.message.text

    conn = get_db_connection()

    cursor = conn.cursor()

    try:

        # ==========================================
        # GET VISITOR DETAILS
        # ==========================================

        cursor.execute("""

            SELECT visitor_name,
                   company_name,
                   mobile,
                   meeting_with

            FROM visitors

            WHERE visitor_id=%s

        """, (visitor_id,))

        visitor = cursor.fetchone()

        # ==========================================
        # UPDATE VISITOR STATUS
        # ==========================================

        cursor.execute("""

            UPDATE visitors

            SET status='REJECTED',
                reason=%s

            WHERE visitor_id=%s

        """, (

            rejection_reason,
            visitor_id
        ))

        conn.commit()

        # ==========================================
        # SEND CONFIRMATION
        # ==========================================

        await update.message.reply_text(

            f"""
❌ VISITOR REJECTED

🆔 Visitor ID: {visitor_id}

👤 Visitor Name: {visitor['visitor_name']}

🏢 Company: {visitor['company_name']}

📞 Mobile: {visitor['mobile']}

👨 Meeting With: {visitor['meeting_with']}

📝 Rejection Reason: {rejection_reason}
"""
        )

        print(f"Visitor {visitor_id} REJECTED")

        # ==========================================
        # REMOVE TEMP STATE
        # ==========================================

        del pending_rejections[user_id]

    except Exception as e:

        print("ERROR:", e)

        await update.message.reply_text(
            "❌ Failed to reject visitor"
        )

    finally:

        cursor.close()

        conn.close()

# ==========================================
# START TELEGRAM BOT
# ==========================================

app = Application.builder().token(BOT_TOKEN).build()

# ==========================================
# BUTTON HANDLER
# ==========================================

app.add_handler(
    CallbackQueryHandler(button_click)
)

# ==========================================
# MESSAGE HANDLER
# ==========================================

app.add_handler(

    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_rejection_reason
    )
)

print("✅ Telegram Bot Running...")

app.run_polling()