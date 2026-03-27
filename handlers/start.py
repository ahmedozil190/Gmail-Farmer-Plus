from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import create_user, get_user, get_business_config
from keyboards import main_menu
from strings import STRINGS
from utils.ban_check import is_banned
from utils.currency import get_exchange_rate


from utils.subscription import check_subscriptions, send_force_join_prompt


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    if await is_banned(update, context):
        return
        
    args = context.args  # referral param

    # Parse referral link  → /start ref_<user_id> or /start REF<user_id>
    referrer_id = None
    if args:
        param = args[0]
        if param.startswith("ref_"):
            try:
                referrer_id = int(param[4:])
            except ValueError:
                pass
        elif param.startswith("REF"):
            try:
                referrer_id = int(param[3:])
            except ValueError:
                pass
        
        if referrer_id == user.id:
            referrer_id = None  # no self-referral

    # Language detection (on first join)
    # Default to 'ar' if user set to Arabic, else 'en'
    user_lang = 'en'
    if user.language_code and user.language_code.startswith('ar'):
        user_lang = 'ar'

    # Register user (INSERT OR IGNORE keeps existing users intact)
    existing = get_user(user.id)
    if not existing:
        create_user(
            user_id=user.id,
            username=user.username or "",
            full_name=user.full_name or "",
            referrer_id=referrer_id,
            language=user_lang
        )
        lang = user_lang
        
        if referrer_id:
            try:
                ref_db_user = get_user(referrer_id)
                ref_lang = ref_db_user['language'] if ref_db_user else 'ar'
                ref_s = STRINGS.get(ref_lang, STRINGS['ar'])
                msg = ref_s.get('REF_REGISTERED_MSG', "").format(name=user.full_name or user.first_name or "User")
                if msg:
                    await context.bot.send_message(chat_id=referrer_id, text=msg)
            except Exception:
                pass
    else:
        lang = existing['language']
        # Always sync names in case they changed or were NULL/None
        from database import update_user_info
        update_user_info(user.id, user.username or "", user.full_name or "")

    s = STRINGS.get(lang, STRINGS['ar'])

    # Check subscriptions
    unsubscribed = await check_subscriptions(context, user.id)
    if unsubscribed:
        await send_force_join_prompt(update.message, unsubscribed, s)
        return

    # Message 1
    await update.message.reply_text(
        s['START_MSG_1'],
        parse_mode="HTML"
    )

    # Message 2 (with keyboard)
    await update.message.reply_text(
        s['START_MSG_2'],
        reply_markup=main_menu(lang),
        parse_mode="HTML",
    )


async def verify_sub_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    user = update.effective_user
    existing = get_user(user.id)
    lang = existing['language'] if existing else 'ar'
    s = STRINGS.get(lang, STRINGS['ar'])

    unsubscribed = await check_subscriptions(context, user.id)
    if unsubscribed:
        # If still unsubscribed, DELETE the old message and send a NEW one for the NEXT channel
        await query.answer()
        try:
            await query.message.delete()
        except:
            pass
            
        await send_force_join_prompt(query.message, unsubscribed, s)
        return






    await query.answer()

    # Delete the verification message
    await query.message.delete()

    # Send the standard welcome messages
    await query.message.reply_text(
        s['START_MSG_1'],
        parse_mode="HTML"
    )

    await query.message.reply_text(
        s['START_MSG_2'],
        reply_markup=main_menu(lang),
        parse_mode="HTML",
    )

