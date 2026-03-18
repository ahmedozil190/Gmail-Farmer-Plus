from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from config import PAYMENT_METHODS, DASHBOARD_URL
from strings import STRINGS


# ── Keyboards ─────────────────────────────────────────────────────────────────

def main_menu(lang: str = 'ar') -> ReplyKeyboardMarkup:
    """Main menu — matches the screenshot layout, with language support."""
    s = STRINGS.get(lang, STRINGS['ar'])
    
    kb = [
        [KeyboardButton(s['BTN_TASKS']),     KeyboardButton(s['BTN_MYACCOUNTS'])],
        [KeyboardButton(s['BTN_BALANCE']),   KeyboardButton(s['BTN_REFERRAL'])],
        [KeyboardButton(s['BTN_SETTINGS']),  KeyboardButton(s['BTN_HELP'])],
    ]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)


def settings_menu(lang: str = 'ar') -> ReplyKeyboardMarkup:
    """Sub-menu for Settings."""
    s = STRINGS.get(lang, STRINGS['ar'])
    kb = [
        [KeyboardButton(s['BTN_LANG']),      KeyboardButton(s['BTN_CURRENCY'])],
        [KeyboardButton(s['BTN_BACK'])],
    ]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)


from utils.currency_list import CURRENCIES

def currency_keyboard(lang: str = 'ar', page: int = 0) -> ReplyKeyboardMarkup:
    """Sub-menu for Currency selection with pagination."""
    s = STRINGS.get(lang, STRINGS['ar'])
    
    per_page = 10
    start = page * per_page
    end = start + per_page
    page_items = CURRENCIES[start:end]
    
    kb = []
    # Currencies: One per row for clarity as requested (large buttons)
    for code, name in page_items:
        kb.append([KeyboardButton(f"{code} - {name}")])
    
    # Navigation row
    nav_row = []
    if page > 0:
        nav_row.append(KeyboardButton(s['BTN_PREV_PAGE']))
    if end < len(CURRENCIES):
        nav_row.append(KeyboardButton(s['BTN_NEXT_PAGE']))
    
    if nav_row:
        kb.append(nav_row)
        
    kb.append([KeyboardButton(s['BTN_BACK'])])
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)


def balance_menu(lang: str = 'ar') -> ReplyKeyboardMarkup:
    """Sub-menu for Balance options."""
    s = STRINGS.get(lang, STRINGS['ar'])
    kb = [
        [KeyboardButton(s['BTN_PAYOUT']),    KeyboardButton(s['BTN_HISTORY'])],
        [KeyboardButton(s['BTN_BACK'])],
    ]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)


def history_menu(lang: str = 'ar') -> ReplyKeyboardMarkup:
    """Sub-menu for History screen (Balance + Payout)."""
    s = STRINGS.get(lang, STRINGS['ar'])
    kb = [
        [KeyboardButton(s['BTN_BALANCE']),   KeyboardButton(s['BTN_PAYOUT'])],
        [KeyboardButton(s['BTN_BACK'])],
    ]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)


def referral_menu(lang: str = 'ar') -> ReplyKeyboardMarkup:
    """Sub-menu for Referral system."""
    s = STRINGS.get(lang, STRINGS['ar'])
    kb = [
        [KeyboardButton(s['BTN_REF_LINK'])],
        [KeyboardButton(s['BTN_REF_STATS'])],
        [KeyboardButton(s['BTN_REF_LIST'])],
        [KeyboardButton(s['BTN_BACK_MAIN'])],
    ]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)


def cancel_keyboard(lang: str = 'ar') -> ReplyKeyboardMarkup:
    s = STRINGS.get(lang, STRINGS['ar'])
    kb = [[KeyboardButton(s['BTN_BACK'])]]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)


def payment_methods_keyboard(lang: str = 'ar') -> ReplyKeyboardMarkup:
    s = STRINGS.get(lang, STRINGS['ar'])
    kb = [[KeyboardButton(m)] for m in PAYMENT_METHODS]
    kb.append([KeyboardButton(s['BTN_BACK'])])
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)


def language_keyboard(lang: str = 'ar') -> ReplyKeyboardMarkup:
    # Special keyboard for language selection
    s = STRINGS.get(lang, STRINGS['ar'])
    kb = [
        [KeyboardButton("العربية 🇸🇦"), KeyboardButton("🇺🇸 English")],
        [KeyboardButton(s['BTN_BACK'])]
    ]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)


def tasks_menu_keyboard(lang: str, price_text: str) -> ReplyKeyboardMarkup:
    """Sub-menu displaying available tasks."""
    s = STRINGS.get(lang, STRINGS['ar'])
    btn_gmail = s['BTN_TASK_GMAIL'].format(price=price_text)
    kb = [
        [KeyboardButton(btn_gmail)],
        [KeyboardButton(s['BTN_BACK_MAIN'])],
    ]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)


def task_flow_keyboard(lang: str = 'ar') -> ReplyKeyboardMarkup:
    """Keyboard for Task Entrance (Continue / Cancel Task)."""
    s = STRINGS.get(lang, STRINGS['ar'])
    kb = [
        [KeyboardButton(s['BTN_CONTINUE'])],
        [KeyboardButton(s['BTN_CANCEL_TASK'])],
    ]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)


def task_cancel_only_keyboard(lang: str = 'ar') -> ReplyKeyboardMarkup:
    """Keyboard for Task Email prompt (Cancel Task only)."""
    s = STRINGS.get(lang, STRINGS['ar'])
    kb = [
        [KeyboardButton(s['BTN_CANCEL_TASK'])],
    ]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)


def remove_keyboard() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()
