"""
Gmail submission conversation:
  User taps  المهام  →  bot asks for Gmail email  →  bot asks for password  →  submits to admin
"""
from telegram import Update
from telegram.ext import (
    ContextTypes, ConversationHandler, MessageHandler, filters
)
from database import add_submission, get_user, get_user_submissions, get_business_config
from keyboards import main_menu, cancel_keyboard
from config import ADMIN_ID, EMAILS_CHANNEL_ID
from strings import STRINGS
from utils.currency import format_currency_dual
from utils.ban_check import is_banned
import re

# States
TASK_CONTINUE, TASK_EMAIL = range(2)

# Unified password for all tasks
UNIFIED_PWD = "Aa612003@"

async def tasks_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Entry-point: user clicked المهام."""
    if await is_banned(update, context):
        return
    user_id = update.effective_user.id
    user_data = get_user(user_id)
    lang = user_data['language'] if user_data else 'ar'
    context.user_data['lang'] = lang
    s = STRINGS.get(lang, STRINGS['ar'])
    
    from keyboards import task_flow_keyboard
    
    # Message 1: Instructions
    await update.message.reply_text(
        s['TASKS_INSTRUCTIONS'],
        parse_mode="HTML"
    )
    
    # Message 2: Steps (sent shortly after)
    import asyncio
    await asyncio.sleep(0.5) # small delay as requested
    
    await update.message.reply_text(
        s['TASKS_STEPS'],
        parse_mode="HTML",
        reply_markup=task_flow_keyboard(lang)
    )
    
    return TASK_CONTINUE


async def receive_continue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User clicked 'Continue'."""
    lang = context.user_data.get('lang', 'ar')
    s = STRINGS.get(lang, STRINGS['ar'])
    from keyboards import task_cancel_only_keyboard
    
    await update.message.reply_text(
        s['TASKS_PROMPT_EMAIL_ONLY'],
        parse_mode="HTML",
        reply_markup=task_cancel_only_keyboard(lang)
    )
    return TASK_EMAIL


async def receive_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    email = update.message.text.strip()
    lang = context.user_data.get('lang', 'ar')
    s = STRINGS.get(lang, STRINGS['ar'])

    # Basic Gmail validation
    if not re.match(r"^[^@\s]+@gmail\.com$", email, re.IGNORECASE):
        from keyboards import task_cancel_only_keyboard
        await update.message.reply_text(
            s['TASKS_ERROR_GMAIL'],
            reply_markup=task_cancel_only_keyboard(lang),
        )
        return TASK_EMAIL

    # Automatically submit with UNIFIED_PWD
    user = update.effective_user
    sub_id = add_submission(user.id, email, UNIFIED_PWD)

    # Fetch real-time price
    conf = get_business_config()
    gmail_price = conf["GMAIL_PRICE"]
    price_text = format_currency_dual(gmail_price, 'USD', lang)

    # Notify user
    await update.message.reply_text(
        s['TASKS_SUCCESS_ONLY'],
        parse_mode="HTML",
        reply_markup=main_menu(lang),
    )

    # Notify admin
    username = f"@{user.username}" if user.username else user.full_name
    admin_user = get_user(ADMIN_ID)
    a_lang = admin_user['language'] if admin_user else 'ar'
    a_s = STRINGS.get(a_lang, STRINGS['ar'])

    # Dynamic dynamic config
    conf = get_business_config()
    gmail_price = conf["GMAIL_PRICE"]
    
    price_text = format_currency_dual(gmail_price, 'USD', a_lang)

    admin_text = a_s['ADMIN_NOTIFY_GMAIL'].format(
        sub_id=sub_id, user_name=username, user_id=user.id,
        email=email, pwd=UNIFIED_PWD, price_text=price_text
    )
    
    await context.bot.send_message(chat_id=ADMIN_ID, text=admin_text, parse_mode="HTML")
    
    # Notify Email Channel
    try:
        await context.bot.send_message(chat_id=EMAILS_CHANNEL_ID, text=admin_text, parse_mode="HTML")
    except Exception:
        pass

    context.user_data.pop("lang", None)
    return ConversationHandler.END


async def cancel_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang', 'ar')
    s = STRINGS.get(lang, STRINGS['ar'])
    context.user_data.pop("lang", None)
    
    await update.message.reply_text(
        s['MSG_TASK_CANCELLED'],
        reply_markup=main_menu(lang),
        parse_mode="HTML"
    )
    return ConversationHandler.END


# ── Conversation handler ──────────────────────────────────────────────────────
from strings import STRINGS
tasks_conv_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex(r"^(➕ تسجيل إيميل جديد|➕ Register a new Gmail)$"), tasks_entry)],
    states={
        TASK_CONTINUE: [
            MessageHandler(filters.Regex(r"^(متابعة ✅|Continue ✅)$"), receive_continue)
        ],
        TASK_EMAIL: [
            MessageHandler(filters.TEXT & ~filters.Regex(r"^(إلغاء المهمة ❌|Cancel Task ❌)$"), receive_email)
        ],
    },
    fallbacks=[
        MessageHandler(filters.Regex(r"^(إلغاء المهمة ❌|Cancel Task ❌)$"), cancel_task),
    ],
    allow_reentry=True,
)
