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
import asyncio
import html
import logging

# States
TASK_MENU, TASK_CONTINUE, TASK_EMAIL, TASK_METHOD, TASK_AUTO = range(5)

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
    
    btn_manual = f"{s['BTN_METHOD_MANUAL']} - {price_text}"
    btn_auto = f"{s['BTN_METHOD_AUTO']} - {price_text}"
    
    if text == s['BTN_BACK_MAIN']:
        return await cancel_task(update, context)
        
    if text in [btn_manual, btn_auto]:
        if not conf.get("BUYING_ACTIVE", True):
            await update.message.reply_text(
                s['TASKS_PAUSED'],
                parse_mode="HTML"
            )
            return TASK_MENU
            
        if text == btn_manual:
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
            
        elif text == btn_auto:
            # Send Auto Data Menu
            from keyboards import remove_keyboard
            msg = await update.message.reply_text("⏳", reply_markup=remove_keyboard())
            await msg.delete()
            return await send_auto_account_data(update, context)
            
    else:
        from keyboards import tasks_menu_keyboard
        await update.message.reply_text(
            s['ERROR_RETRY'],
            reply_markup=tasks_menu_keyboard(lang, price_text)
        )
        return TASK_MENU

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

async def send_auto_account_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang', 'ar')
    s = STRINGS.get(lang, STRINGS['ar'])
    
    from utils.name_generator import generate_account_data
    from telegram import InlineKeyboardMarkup, InlineKeyboardButton
    
    # Generate new data
    data = generate_account_data()
    context.user_data['auto_task'] = data
    
    text = s['MSG_AUTO_DATA'].format(**data)
    
    keyboard = [
        [InlineKeyboardButton(s['BTN_AUTO_DONE'], callback_data="auto_done")],
        [InlineKeyboardButton(s['BTN_AUTO_REGEN'], callback_data="auto_regen")],
        [InlineKeyboardButton(s['BTN_AUTO_CANCEL'], callback_data="auto_cancel")]
    ]
    
    if update.callback_query:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    return TASK_AUTO

async def handle_auto_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    lang = context.user_data.get('lang', 'ar')
    s = STRINGS.get(lang, STRINGS['ar'])
    
    if query.data == "auto_cancel":
        await query.message.delete()
        lang = context.user_data.get('lang', 'ar')
        s = STRINGS.get(lang, STRINGS['ar'])
        context.user_data.pop("lang", None)
        from keyboards import main_menu
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=s['MSG_TASK_CANCELLED'],
            reply_markup=main_menu(lang),
            parse_mode="HTML"
        )
        return ConversationHandler.END
        
    elif query.data == "auto_regen":
        await query.message.delete()
        return await send_auto_account_data(update, context)
        
    elif query.data == "auto_done":
        await query.message.delete()
        
        # Submit the task
        task_data = context.user_data.get('auto_task')
        if not task_data:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=s['ERROR_RETRY'])
            return TASK_MENU
            
        email = task_data['email']
        password = task_data['password']
        
        # Duplicate check
        from database import is_gmail_already_submitted, add_submission, get_business_config, get_user
        if is_gmail_already_submitted(email):
             await context.bot.send_message(chat_id=update.effective_chat.id, text=s['ERROR_RETRY'])
             return TASK_MENU
             
        user_id = update.effective_user.id
        db_sub_id = add_submission(user_id, email, password)
        sub_id = str(db_sub_id)
        
        # Send notifications
        from keyboards import main_menu
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=s['TASKS_SUCCESS_ONLY'].format(sub_id=sub_id),
            parse_mode="HTML",
            reply_markup=main_menu(lang)
        )
        
        # Notify Admin
        try:
            admin_user = get_user(ADMIN_ID)
            a_lang = admin_user['language'] if admin_user else 'ar'
            a_s = STRINGS.get(a_lang, STRINGS['ar'])
            conf_notify = get_business_config()
            p_text = format_currency_dual(conf_notify["GMAIL_PRICE"], 'USD', a_lang)
            curr_date = datetime.now().strftime("%Y-%m-%d %H:%M")
            st_text = a_s.get('DASH_FILTER_PENDING', 'Pending')

            admin_text = a_s['ADMIN_NOTIFY_GMAIL'].format(
                status=html.escape(str(st_text)),
                sub_id=html.escape(str(sub_id)),
                gmail=html.escape(str(email)),
                pwd=html.escape(str(password)),
                price=html.escape(str(p_text)),
                date=html.escape(str(curr_date)),
                user_id=html.escape(str(user_id))
            )

            await context.bot.send_message(chat_id=ADMIN_ID, text=admin_text, parse_mode="HTML", disable_web_page_preview=True)
            
            c_id = conf_notify.get("EMAILS_CHANNEL_ID")
            if c_id and "Add_In_DotEnv" not in str(c_id):
                await context.bot.send_message(chat_id=c_id, text=admin_text, parse_mode="HTML", disable_web_page_preview=True)
        except Exception as e:
            logging.error(f"Task Notify Error: {e}")
            
        context.user_data.pop("lang", None)
        context.user_data.pop("auto_task", None)
        return ConversationHandler.END


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

    # 1. Notify user immediately
    await update.message.reply_text(
        s['TASKS_SUCCESS_ONLY'].format(sub_id=sub_id),
        parse_mode="HTML",
        reply_markup=main_menu(lang),
    )

    # 2. Send notifications directly (simple & reliable)
    try:
        username = f"@{user.username}" if user.username else user.full_name
        admin_user = get_user(ADMIN_ID)
        a_lang = admin_user['language'] if admin_user else 'ar'
        a_s = STRINGS.get(a_lang, STRINGS['ar'])
        conf_notify = get_business_config()
        p_text = format_currency_dual(conf_notify["GMAIL_PRICE"], 'USD', a_lang)
        curr_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        st_text = a_s.get('DASH_FILTER_PENDING', 'Pending')

        admin_text = a_s['ADMIN_NOTIFY_GMAIL'].format(
            status=html.escape(str(st_text)),
            sub_id=html.escape(str(sub_id)),
            gmail=html.escape(str(email)),
            pwd=html.escape(str(UNIFIED_PWD)),
            price=html.escape(str(p_text)),
            date=html.escape(str(curr_date)),
            user_id=html.escape(str(user.id))
        )

        # Admin DM
        try:
            await context.bot.send_message(chat_id=ADMIN_ID, text=admin_text, parse_mode="HTML", disable_web_page_preview=True, disable_notification=False)
        except Exception as e:
            logging.error(f"Task Admin Notify Error: {e}")

        # Channel
        c_id = conf_notify.get("EMAILS_CHANNEL_ID")
        if c_id and "Add_In_DotEnv" not in str(c_id):
            try:
                await context.bot.send_message(chat_id=c_id, text=admin_text, parse_mode="HTML", disable_web_page_preview=True)
            except Exception as e:
                logging.error(f"Task Channel Notify Error: {e}")
    except Exception as e:
        logging.error(f"Task Notify Error: {e}")

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
from telegram.ext import CallbackQueryHandler

tasks_conv_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex(r"^(➕ تسجيل إيميل جديد|➕ Register a new Gmail)$"), tasks_entry)],
    states={
        TASK_MENU: [
            MessageHandler(filters.TEXT & ~filters.Regex(r"^(إلغاء المهمة ❌|Cancel Task ❌)$"), receive_task_choice)
        ],
        TASK_CONTINUE: [
            MessageHandler(filters.Regex(r"^(متابعة ✅|Continue ✅)$"), receive_continue)
        ],
        TASK_AUTO: [
            CallbackQueryHandler(handle_auto_action, pattern=r"^auto_")
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
