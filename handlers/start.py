from telegram import Update
from telegram.ext import ContextTypes
from database import create_user, get_user
from keyboards import main_menu
from strings import STRINGS
from utils.ban_check import is_banned
from utils.currency import get_exchange_rate


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
    else:
        lang = existing['language']

    s = STRINGS.get(lang, STRINGS['ar'])

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
