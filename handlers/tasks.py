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
TASK_METHOD, TASK_CONTINUE, TASK_EMAIL, TASK_AUTO = range(4)

# Removed static UNIFIED_PWD

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
    
    conf = get_business_config()
    if not conf.get("BUYING_ACTIVE", True):
        s = STRINGS.get(lang, STRINGS['ar'])
        await update.message.reply_text(s['TASKS_PAUSED'], parse_mode="HTML")
        return ConversationHandler.END

    # Get prices
    price_manual_val = user_data["custom_manual_price"] if user_data and user_data["custom_manual_price"] is not None else conf["GMAIL_PRICE"]
    price_auto_val = user_data["custom_auto_price"] if user_data and user_data["custom_auto_price"] is not None else conf["GMAIL_PRICE_AUTO"]
    
    currency = user_data['currency'] if (user_data and user_data['currency']) else 'USD'
    price_manual_text = format_currency_dual(price_manual_val, currency, lang)
    price_auto_text = format_currency_dual(price_auto_val, currency, lang)

    from keyboards import task_method_keyboard
    s = STRINGS.get(lang, STRINGS['ar'])
    text = s.get('MSG_CHOOSE_METHOD', "How would you prefer to create the new account?")
    
    await update.message.reply_text(
        text=text,
        parse_mode="HTML",
        reply_markup=task_method_keyboard(lang, price_manual_text, price_auto_text)
    )
    return TASK_METHOD


async def handle_method_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    lang = context.user_data.get('lang', 'ar')
    s = STRINGS.get(lang, STRINGS['ar'])
    
    # Check manual button (regex would be better but let's check startswith/contains)
    if s['BTN_METHOD_MANUAL'].split(" - ")[0] in text:
        return await send_manual_instructions(update, context)
        
    elif s['BTN_METHOD_AUTO'].split(" - ")[0] in text:
        return await send_auto_account_data(update, context)
        
    elif text == s['BTN_BACK'] or text == "🔙 رجوع" or text == "🔙 Back":
        from keyboards import main_menu
        await update.message.reply_text(
            text=s['PROCESS_CANCELLED'],
            reply_markup=main_menu(lang)
        )
        return ConversationHandler.END
        
    return TASK_METHOD


async def send_manual_instructions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang', 'ar')
    s = STRINGS.get(lang, STRINGS['ar'])
    
    from database import get_business_config
    conf = get_business_config()
    unified_pwd = conf.get("GMAIL_MANUAL_PWD", "aass1122")
    
    from keyboards import task_continue_keyboard
    
    text = s.get('TASKS_MANUAL_INSTRUCTIONS', "Manual Instructions").format(unified_pwd=unified_pwd)
    
    await update.message.reply_text(
        text=text,
        parse_mode="HTML",
        reply_markup=task_continue_keyboard(lang)
    )
    return TASK_CONTINUE


async def receive_continue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    lang = context.user_data.get('lang', 'ar')
    s = STRINGS.get(lang, STRINGS['ar'])
    
    if text == s['BTN_FOLLOW_UP']:
        from keyboards import task_cancel_only_keyboard
        await update.message.reply_text(
            text=s['TASKS_PROMPT_EMAIL'],
            parse_mode="HTML",
            reply_markup=task_cancel_only_keyboard(lang)
        )
        return TASK_EMAIL
    
    elif text == s['BTN_BACK']:
        # Go back to method selection
        return await tasks_entry(update, context)
        
    return TASK_CONTINUE


async def receive_manual_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    lang = context.user_data.get('lang', 'ar')
    s = STRINGS.get(lang, STRINGS['ar'])
    
    if text == s['BTN_CANCEL'] or text == s.get('BTN_CANCEL_TASK', 'Cancel Task'):
         from keyboards import main_menu
         await update.message.reply_text(
             text=s['PROCESS_CANCELLED'],
             reply_markup=main_menu(lang)
         )
         return ConversationHandler.END

    email = text.strip().lower()
    
    # Basic validation
    if not re.match(r"[^@]+@gmail\.com$", email):
        await update.message.reply_text(s['TASKS_ERROR_GMAIL'])
        return TASK_EMAIL
        
    # Duplicate check
    from database import is_gmail_already_submitted
    if is_gmail_already_submitted(email):
        await update.message.reply_text(s['ERR_DUPLICATE_GMAIL'])
        return TASK_EMAIL
        
    # Process Manual Submission with dynamic unified password
    from database import get_business_config
    conf = get_business_config()
    password = conf.get("GMAIL_MANUAL_PWD", "aass1122")
    
    user_id = update.effective_user.id
    
    from database import add_submission, get_user
    conf = get_business_config()
    user_data = get_user(user_id)
    
    reward = user_data["custom_manual_price"] if user_data and user_data["custom_manual_price"] is not None else conf["GMAIL_PRICE"]
    
    db_sub_id = add_submission(user_id, email, password, price=reward)
    sub_id = str(db_sub_id)
    
    from keyboards import main_menu
    await update.message.reply_text(
        text=s['TASKS_SUCCESS'].format(email=email, sub_id=sub_id, price_text=format_currency_dual(reward, user_data['currency'] if user_data else 'USD', lang)),
        parse_mode="HTML",
        reply_markup=main_menu(lang)
    )
    
    # Notify Admin
    try:
        admin_user = get_user(ADMIN_ID)
        a_lang = admin_user['language'] if admin_user else 'ar'
        a_s = STRINGS.get(a_lang, STRINGS['ar'])
        curr_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        st_text = a_s.get('DASH_FILTER_PENDING', 'Pending')

        admin_text = a_s['ADMIN_NOTIFY_GMAIL'].format(
            status=html.escape(str(st_text)),
            sub_id=html.escape(str(sub_id)),
            gmail=html.escape(str(email)),
            pwd=html.escape(str(password)),
            price=html.escape(format_currency_dual(reward, 'USD', a_lang)),
            date=html.escape(str(curr_date)),
            user_id=html.escape(str(user_id))
        )

        await context.bot.send_message(chat_id=ADMIN_ID, text=admin_text, parse_mode="HTML", disable_web_page_preview=True)
        
        c_id = conf.get("EMAILS_CHANNEL_ID")
        if c_id and "Add_In_DotEnv" not in str(c_id):
            await context.bot.send_message(chat_id=c_id, text=admin_text, parse_mode="HTML", disable_web_page_preview=True)
    except Exception as e:
        logging.error(f"Manual Task Notify Error: {e}")
        
    context.user_data.clear()
    return ConversationHandler.END


async def send_auto_account_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang', 'ar')
    s = STRINGS.get(lang, STRINGS['ar'])
    
    from utils.name_generator import generate_account_data
    from telegram import InlineKeyboardMarkup, InlineKeyboardButton
    
    conf = get_business_config()
    fixed_pwd = conf.get("GMAIL_AUTO_PWD", "Aa612003@")
    
    # Generate new data
    data = generate_account_data()
    data['password'] = fixed_pwd # Enforce unified password
    context.user_data['auto_task'] = data
    
    user_id = update.effective_user.id
    user_data = get_user(user_id)
    currency = user_data['currency'] if (user_data and user_data['currency']) else 'EGP'
    
    price_val = user_data["custom_auto_price"] if user_data and user_data["custom_auto_price"] is not None else conf["GMAIL_PRICE_AUTO"]
    price_text = format_currency_dual(price_val, currency, lang)
    data['price_text'] = price_text
    text = s['MSG_AUTO_DATA'].format(**data)
    
    keyboard = [
        [InlineKeyboardButton(s['BTN_AUTO_DONE'], callback_data="auto_done")],
        [InlineKeyboardButton(s['BTN_AUTO_REGEN'], callback_data="auto_regen")],
        [InlineKeyboardButton(s['BTN_AUTO_CANCEL'], callback_data="auto_cancel")]
    ]
    
    chat_id = update.effective_chat.id
    message_id = update.callback_query.message.message_id if update.callback_query else None
    
    if update.callback_query:
         await query_edit_safe(update, context, text, InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text(
            text=text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    return TASK_AUTO

async def query_edit_safe(update, context, text, reply_markup):
    try:
        await update.callback_query.edit_message_text(text=text, parse_mode="HTML", reply_markup=reply_markup)
    except:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode="HTML", reply_markup=reply_markup)

async def handle_auto_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    lang = context.user_data.get('lang', 'ar')
    s = STRINGS.get(lang, STRINGS['ar'])
    
    if query.data == "auto_cancel":
        await query.message.delete()
        from keyboards import main_menu
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=s['MSG_THANK_YOU_TRYING'],
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
            return ConversationHandler.END # End flow if no data
            
        email = task_data['email']
        password = task_data['password']
        
        # Duplicate check
        from database import is_gmail_already_submitted, add_submission, get_business_config, get_user
        if is_gmail_already_submitted(email):
             await context.bot.send_message(chat_id=update.effective_chat.id, text=s['ERROR_RETRY'])
             return ConversationHandler.END
             
        # Add with AUTO price
        conf_auto = get_business_config()
        user_id = update.effective_user.id
        user_data = get_user(user_id)
        
        # User-specific auto price or global
        reward = user_data["custom_auto_price"] if user_data and user_data["custom_auto_price"] is not None else conf_auto["GMAIL_PRICE_AUTO"]
        
        db_sub_id = add_submission(user_id, email, password, price=reward)
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
            curr_date = datetime.now().strftime("%Y-%m-%d %H:%M")
            st_text = a_s.get('DASH_FILTER_PENDING', 'Pending')

            admin_text = a_s['ADMIN_NOTIFY_GMAIL'].format(
                status=html.escape(str(st_text)),
                sub_id=html.escape(str(sub_id)),
                gmail=html.escape(str(email)),
                pwd=html.escape(str(password)),
                price=html.escape(format_currency_dual(reward, 'USD', a_lang)),
                date=html.escape(str(curr_date)),
                user_id=html.escape(str(user_id))
            )

            await context.bot.send_message(chat_id=ADMIN_ID, text=admin_text, parse_mode="HTML", disable_web_page_preview=True)
            
            c_id = conf_auto.get("EMAILS_CHANNEL_ID")
            if c_id and "Add_In_DotEnv" not in str(c_id):
                await context.bot.send_message(chat_id=c_id, text=admin_text, parse_mode="HTML", disable_web_page_preview=True)
        except Exception as e:
            logging.error(f"Task Notify Error: {e}")
            
        context.user_data.clear() # Clear all including lang/task
        return ConversationHandler.END


    context.user_data.clear()
    return ConversationHandler.END


async def cancel_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang', 'ar')
    s = STRINGS.get(lang, STRINGS['ar'])
    context.user_data.clear()
    
    from keyboards import main_menu
    await update.message.reply_text(
        s['MSG_TASK_CANCELLED'],
        reply_markup=main_menu(lang),
        parse_mode="HTML"
    )
    return ConversationHandler.END


# ── Conversation handler ──────────────────────────────────────────────────────
from strings import STRINGS
from telegram.ext import CallbackQueryHandler, filters

tasks_conv_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex(r".*(تسجيل إيميل جديد|Register a new Gmail).*"), tasks_entry)],
    states={
        TASK_METHOD: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_method_selection)
        ],
        TASK_CONTINUE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, receive_continue)
        ],
        TASK_AUTO: [
            CallbackQueryHandler(handle_auto_action, pattern=r"^auto_")
        ],
        TASK_EMAIL: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, receive_manual_email)
        ],
    },
    fallbacks=[
        MessageHandler(filters.Regex(r"^(إلغاء المهمة ❌|Cancel Task ❌|❌ إلغاء|❌ Cancel)$"), cancel_task),
        MessageHandler(filters.Regex(r"^(🔙 رجوع|🔙 Back)$"), cancel_task),
    ],
    allow_reentry=True,
)
