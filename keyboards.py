from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
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


def pagination_keyboard(lang: str = 'ar', page: int = 0, total_pages: int = 1, context_name: str = 'accounts') -> InlineKeyboardMarkup:
    """Inline pagination keyboard for lists with dynamic labels matching user screenshot."""
    s = STRINGS.get(lang, STRINGS['ar'])
    kb = []
    
    # Navigation row
    nav_row = []
    
    # page is 0-indexed.
    # Display current is page + 1.
    # Back is page. Next is page + 2.
    
    if page > 0:
        label = f"<< {s['BTN_PREV_PAGE_INLINE']} ({page}/{total_pages})"
        nav_row.append(InlineKeyboardButton(label, callback_data=f"page:{context_name}:{page - 1}"))
        
    if page < total_pages - 1:
        label = f"{s['BTN_NEXT_PAGE_INLINE']} ({page + 2}/{total_pages}) >>"
        nav_row.append(InlineKeyboardButton(label, callback_data=f"page:{context_name}:{page + 1}"))
    
    if nav_row:
        kb.append(nav_row)
        
    return InlineKeyboardMarkup(kb)


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


def task_cancel_only_keyboard(lang: str = 'ar') -> ReplyKeyboardMarkup:
    """Keyboard for Task Email prompt (Cancel Task only)."""
    s = STRINGS.get(lang, STRINGS['ar'])
    kb = [
        [KeyboardButton(s['BTN_CANCEL_TASK'])],
    ]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)


def remove_keyboard() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()
