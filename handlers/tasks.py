"""
Gmail submission conversation:
  User taps  المهام  →  bot asks for Gmail email  →  bot asks for password  →  submits to admin
"""
from datetime import datetime
from telegram import Update, Bot
from telegram.ext import (
    ContextTypes, ConversationHandler, MessageHandler, filters
)
from database import add_submission, get_user, get_user_submissions, get_business_config
from keyboards import main_menu, cancel_keyboard
from config import ADMIN_ID, EMAILS_CHANNEL_ID, BOT_TOKEN
from strings import STRINGS
from utils.currency import format_currency_dual
from utils.ban_check import is_banned
import re
import html
import logging

# States
TASK_MENU, TASK_CONTINUE, TASK_EMAIL = range(3)

# Unified password for all tasks
UNIFIED_PWD = "Aa612003@"

async def tasks_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Entry-point: user clicked المهام."""
    from utils.subscription import require_subscription
    if not await require_subscription(update, context):
        return
    if await is_banned(update, context):
        return
    user_id = update.effective_user.id
    user_data = get_user(user_id)
    lang = user_data['language'] if user_data else 'ar'
    context.user_data['lang'] = lang
    s = STRINGS.get(lang, STRINGS['ar'])
    
    from keyboards import tasks_menu_keyboard
    
    # Fetch real-time price
    conf = get_business_config()
    gmail_price = conf["GMAIL_PRICE"]
    price_text = format_currency_dual(gmail_price, 'USD', lang)
    
    await update.message.reply_text(
        s['TASKS_MENU_PROMPT'],
        parse_mode="HTML",
        reply_markup=tasks_menu_keyboard(lang, price_text)
    )
    
    return TASK_MENU


async def receive_task_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User clicked a task from the menu."""
    text = update.message.text.strip()
    lang = context.user_data.get('lang', 'ar')
    s = STRINGS.get(lang, STRINGS['ar'])
    
    conf = get_business_config()
    gmail_price = conf["GMAIL_PRICE"]
    price_text = format_currency_dual(gmail_price, 'USD', lang)
    
    expected_gmail_btn = s['BTN_TASK_GMAIL'].format(price=price_text)
    
    if text == s['BTN_BACK_MAIN']:
        return await cancel_task(update, context)
        
    if text == expected_gmail_btn:
        if not conf.get("BUYING_ACTIVE", True):
            await update.message.reply_text(
                s['TASKS_PAUSED'],
                parse_mode="HTML"
            )
            return TASK_MENU
    else:
        from keyboards import tasks_menu_keyboard
        await update.message.reply_text(
            s['ERROR_RETRY'],
            reply_markup=tasks_menu_keyboard(lang, price_text)
        )
        return TASK_MENU
        
    # Send Instructions
    from keyboards import task_flow_keyboard
    
    await update.message.reply_text(
        s['TASKS_INSTRUCTIONS'],
        parse_mode="HTML"
    )
    
    import asyncio
    await asyncio.sleep(0.5)
    
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

    # Check for duplicates
    from database import is_gmail_already_submitted
    if is_gmail_already_submitted(email):
        from keyboards import task_cancel_only_keyboard
        await update.message.reply_text(
            s['ERR_DUPLICATE_GMAIL'],
            reply_markup=task_cancel_only_keyboard(lang),
            parse_mode="HTML"
        )
        return TASK_EMAIL

    # Automatically submit with UNIFIED_PWD
    user = update.effective_user
    db_sub_id = add_submission(user.id, email, UNIFIED_PWD)
    sub_id = str(db_sub_id)

    # Fetch real-time price
    conf = get_business_config()
    gmail_price = conf["GMAIL_PRICE"]
    price_text = format_currency_dual(gmail_price, 'USD', lang)

    # Notify user
    await update.message.reply_text(
        s['TASKS_SUCCESS_ONLY'].format(sub_id=sub_id),
        parse_mode="HTML",
        reply_markup=main_menu(lang),
    )

    # Notify admin
    username = f"@{user.username}" if user.username else user.full_name
    admin_user = get_user(ADMIN_ID)
    a_lang = admin_user['language'] if admin_user else 'ar'
    a_s = STRINGS.get(a_lang, STRINGS['ar'])

    # Separate task to avoid "Already Read" issue when admin is testing
    async def _async_notify():
        try:
            await asyncio.sleep(1) # Tiny delay to separate from user's interaction
            
            # Fetch fresh config inside task
            conf_async = get_business_config()
            price_text_admin = format_currency_dual(conf_async["GMAIL_PRICE"], 'USD', a_lang)
            current_date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            status_text = a_s.get('DASH_FILTER_PENDING', 'Pending')
            
            admin_text = a_s['ADMIN_NOTIFY_GMAIL'].format(
                status=html.escape(str(status_text)),
                sub_id=html.escape(str(sub_id)),
                gmail=html.escape(str(email)),
                pwd=html.escape(str(UNIFIED_PWD)),
                price=html.escape(str(price_text_admin)),
                date=html.escape(str(current_date_str)),
                user_id=html.escape(str(user.id))
            )
            
            standalone_bot = Bot(token=BOT_TOKEN)
            
            # Notify Admin
            try:
                await standalone_bot.send_message(chat_id=ADMIN_ID, text=admin_text, parse_mode="HTML", disable_web_page_preview=True)
            except Exception as e:
                logging.error(f"Async Admin Notify Error: {e}")
                try:
                    await standalone_bot.send_message(chat_id=ADMIN_ID, text=admin_text.replace("<b>","").replace("</b>","").replace("<code>","").replace("</code>",""))
                except: pass

            # Notify Channel
            ch_id = conf_async.get("EMAILS_CHANNEL_ID")
            if ch_id and "Add_In_DotEnv" not in str(ch_id):
                try:
                    await standalone_bot.send_message(chat_id=ch_id, text=admin_text, parse_mode="HTML", disable_web_page_preview=True)
                except Exception as e:
                    logging.error(f"Async Channel Notify Error: {e}")
                    try:
                        await standalone_bot.send_message(chat_id=ch_id, text=admin_text.replace("<b>","").replace("</b>","").replace("<code>","").replace("</code>",""))
                    except: pass
        except Exception as e:
            logging.error(f"Global Async Notify Failure: {e}")

    import asyncio
    asyncio.create_task(_async_notify())

    context.user_data.pop("lang", None)
    return ConversationHandler.END

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
        TASK_MENU: [
            MessageHandler(filters.TEXT & ~filters.Regex(r"^(إلغاء المهمة ❌|Cancel Task ❌)$"), receive_task_choice)
        ],
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
