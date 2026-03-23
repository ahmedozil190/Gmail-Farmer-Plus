from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from database import get_user, update_user_currency
from keyboards import settings_menu, currency_keyboard, main_menu
from strings import STRINGS
from utils.ban_check import is_banned

async def settings_handler_fn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """🛠 Settings Menu."""
    from utils.subscription import require_subscription
    if not await require_subscription(update, context):
        return
    if await is_banned(update, context):
        return
    user = get_user(update.effective_user.id)
    lang = user['language'] if user else 'ar'
    s = STRINGS.get(lang, STRINGS['ar'])
    
    context.user_data['parent_menu'] = 'main'
    await update.message.reply_text(
        s['SETTINGS_MSG'],
        parse_mode="HTML",
        reply_markup=settings_menu(lang)
    )


async def currency_btn_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User clicked 'Currency' button."""
    user = get_user(update.effective_user.id)
    lang = user['language'] if user else 'ar'
    s = STRINGS.get(lang, STRINGS['ar'])
    
    context.user_data['parent_menu'] = 'settings'
    context.user_data['curr_page'] = 0
    context.user_data['pagination_context'] = 'currency'
    await update.message.reply_text(
        s['CURRENCY_MSG'],
        parse_mode="HTML",
        reply_markup=currency_keyboard(lang, page=0)
    )


async def change_currency_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User selected a specific currency or navigation."""
    text = update.message.text
    user_id = update.effective_user.id
    user = get_user(user_id)
    lang = user['language'] if user else 'ar'
    s = STRINGS.get(lang, STRINGS['ar'])
    
    if context.user_data.get('pagination_context') != 'currency':
        return

    page = context.user_data.get('curr_page', 0)

    if text == s['BTN_NEXT_PAGE']:
        page += 1
        context.user_data['curr_page'] = page
        await update.message.reply_text(s['BTN_NEXT_PAGE'], reply_markup=currency_keyboard(lang, page))
        return
    elif text == s['BTN_PREV_PAGE']:
        page = max(0, page - 1)
        context.user_data['curr_page'] = page
        await update.message.reply_text(s['BTN_PREV_PAGE'], reply_markup=currency_keyboard(lang, page))
        return

    # Check if text matches "CODE - Name"
    import re
    match = re.search(r"^([A-Z]{3}) - ", text)
    if match:
        new_curr = match.group(1)
        update_user_currency(user_id, new_curr)
        await update.message.reply_text(
            s['CURRENCY_SET_SUCCESS'].format(currency=new_curr),
            parse_mode="HTML",
            reply_markup=settings_menu(lang)
        )
    else:
        # Unknown/Fallback
        await update.message.reply_text(s['ERROR_RETRY'], reply_markup=settings_menu(lang))

settings_handler = MessageHandler(filters.Regex(r"^(⚙️ الإعدادات|⚙️ Settings)$"), settings_handler_fn)
currency_handler = MessageHandler(filters.Regex(r"^(💵 العملة|💵 Currency)$"), currency_btn_handler)
# Updated filter to REMOVE navigation buttons (Next/Prev preserved, but Back removed)
select_currency_handler = MessageHandler(
    filters.Regex(r"^(➡️ Next Page|➡️ الصفحة التالية|⬅️ Previous Page|⬅️ الصفحة السابقة|[A-Z]{3} - .*)$"), 
    change_currency_handler
)
