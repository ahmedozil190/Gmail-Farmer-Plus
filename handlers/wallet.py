from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from database import get_balance, get_user_submissions, get_user, get_user_withdrawals, get_business_config
from keyboards import main_menu, balance_menu, history_menu, pagination_keyboard
from strings import STRINGS
from utils.currency import get_exchange_rate
from utils.ban_check import is_banned


async def balance_handler_fn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """💰 الرصيد — show breakdown in dual currency."""
    from utils.subscription import require_subscription
    if not await require_subscription(update, context):
        return
    if await is_banned(update, context):
        return
    user_id = update.effective_user.id
    user_data = get_user(user_id, update.effective_user)
    lang = user_data['language'] if user_data else 'ar'
    currency_pref = user_data['currency'] if user_data else 'USD'
    s = STRINGS.get(lang, STRINGS['ar'])
    
    # Store for navigation
    context.user_data['parent_menu'] = 'main'
    
    balance, pending = get_balance(user_id)
    
    # Dual currency text preparation
    from utils.currency import format_currency_dual
    bal_text = format_currency_dual(balance, currency_pref, lang)
    hold_text = format_currency_dual(pending, currency_pref, lang)
    
    text_info = s['BALANCE_INFO_DUAL'].format(
        balance_text=bal_text,
        hold_text=hold_text
    )

    await update.message.reply_text(
        f"{s['BALANCE_TITLE']}"
        f"{text_info}",
        parse_mode="HTML",
        reply_markup=balance_menu(lang),
    )


async def history_handler_fn(update: Update, context: ContextTypes.DEFAULT_TYPE, page: int = None):
    """📜 سجل العمليات — show payouts and account acceptance/rejection with inline pagination."""
    # Handle CallbackQuery vs Message
    query = update.callback_query
    if query:
        await query.answer()
        user_id = query.from_user.id
    else:
        user_id = update.effective_user.id
        from utils.subscription import require_subscription
        if not await require_subscription(update, context):
            return
        if await is_banned(update, context):
            return

    user_data = get_user(user_id, query.from_user if query else update.effective_user)
    lang = user_data['language'] if user_data else 'ar'
    currency_pref = user_data['currency'] if user_data else 'USD'
    s = STRINGS.get(lang, STRINGS['ar'])
    
    from database import get_combined_history, count_combined_history
    from keyboards import pagination_keyboard, history_menu
    
    per_page = 5
    total_count = count_combined_history(user_id)
    total_pages = (total_count + per_page - 1) // per_page if total_count > 0 else 1
    
    if page is None:
        page = 0
    if page >= total_pages:
        page = max(0, total_pages - 1)

    offset = page * per_page
    events = get_combined_history(user_id, limit=per_page, offset=offset)

    if not events:
        msg = s['HISTORY_EMPTY']
        reply_markup = history_menu(lang)
    else:
        lines = []
        lines.append(s['HISTORY_TITLE'].format(count=total_count))
        
        for ev in events:
            dt = ev['dt']
            etype = ev['type']
            info = ev['info']
            status = ev['status']
            amount = ev['amount']
            sub_id = ev['id']
            extra = ev['extra_info']
            
            date_str = dt[:10] # YYYY-MM-DD
            from utils.currency import format_currency_dual
            
            status_text = s.get('ST_' + status.upper(), status)
            
            if etype == 'withdrawal':
                amt_text = f"-{format_currency_dual(amount, currency_pref, lang)}"
                method_text = info.replace('💳','').replace('🟡','').replace('🟢','').replace('💎','').strip()
                addr_text = extra or "N/A"
            else: # submission
                amt_text = f"+{format_currency_dual(amount, currency_pref, lang)}"
                method_text = s['HISTORY_METHOD_SUBMISSION']
                addr_text = info # gmail account
            
            item_text = s['HISTORY_ITEM_TEMPLATE'].format(
                pay_id_lbl=s['DASH_PAY_ID'],
                pay_id=sub_id,
                status_lbl=s['HISTORY_STATUS'],
                status=status_text,
                method_lbl=s['HISTORY_METHOD'],
                method=method_text,
                price_lbl=s['HISTORY_PRICE'],
                price=amt_text,
                addr_lbl=s['HISTORY_ADDR'],
                address=f"<code>{addr_text}</code>",
                date_lbl=s['HISTORY_DATE'],
                date=date_str
            )
            lines.append(item_text)
            lines.append("────────────────")
        
        msg = "\n".join(lines)
        reply_markup = pagination_keyboard(lang, page, total_pages, context_name='history')

    if query:
        await query.edit_message_text(msg, parse_mode="HTML", reply_markup=reply_markup, disable_web_page_preview=True)
    else:
        await update.message.reply_text(msg, parse_mode="HTML", reply_markup=reply_markup, disable_web_page_preview=True)


async def my_accounts_handler_fn(update: Update, context: ContextTypes.DEFAULT_TYPE, page: int = None):
    """📂 حساباتي — show all user submissions with inline pagination."""
    from utils.subscription import require_subscription
    
    # Handle CallbackQuery vs Message
    query = update.callback_query
    if query:
        await query.answer()
        user_id = query.from_user.id
        msg_obj = query.message
    else:
        user_id = update.effective_user.id
        msg_obj = update.message
        if not await require_subscription(update, context):
            return
        if await is_banned(update, context):
            return

    user_data = get_user(user_id, query.from_user if query else update.effective_user)
    lang = user_data['language'] if user_data else 'ar'
    s = STRINGS.get(lang, STRINGS['ar'])

    from database import get_user_submissions, count_user_submissions
    from keyboards import pagination_keyboard
    
    per_page = 5
    total_count = count_user_submissions(user_id)
    total_pages = (total_count + per_page - 1) // per_page if total_count > 0 else 1
    
    # Identify target page
    if page is None:
        if query:
            # This shouldn't normally happen if routed correctly, but for safety:
            page = 0 
        else:
            page = 0
            
    # Bound check
    if page >= total_pages:
        page = max(0, total_pages - 1)
    if page < 0:
        page = 0

    offset = page * per_page
    subs = get_user_submissions(user_id, limit=per_page, offset=offset)

    if not subs:
        text_out = s['MY_ACCOUNTS_EMPTY']
        reply_markup = main_menu(lang)
    else:
        lines = []
        lines.append(s['MY_ACCOUNTS_TITLE'].format(count=total_count))
        
        for sub in subs:
            if sub["status"] == "pending":
                status_text = s['ST_PENDING']
            elif sub["status"] == "approved":
                status_text = s['ST_APPROVED']
            else:
                status_text = s['ST_REJECTED']
                
            date = sub["submitted_at"][:10]
            item_text = s['MY_ACCOUNTS_ITEM_TEMPLATE'].format(
                status=status_text,
                task_id=sub['id'],
                gmail=sub['gmail_account'],
                date=date
            )
            lines.append(item_text)
            lines.append("────────────────")
        text_out = "\n".join(lines)
        
        reply_markup = pagination_keyboard(lang, page, total_pages, context_name='accounts')

    if query:
        await query.edit_message_text(text_out, parse_mode="HTML", reply_markup=reply_markup)
    else:
        await msg_obj.reply_text(text_out, parse_mode="HTML", reply_markup=reply_markup)


async def unified_back_handler_fn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Unified 'Back' handler that looks at context.user_data['parent_menu']."""
    user_id = update.effective_user.id
    user_data = get_user(user_id, update.effective_user)
    lang = user_data['language'] if user_data else 'ar'
    parent = context.user_data.get('parent_menu', 'main')
    
    if parent == 'balance':
        await balance_handler_fn(update, context)
    elif parent == 'settings':
        from handlers.settings import settings_handler_fn
        await settings_handler_fn(update, context)
    else:
        # parent == 'main' or None
        s = STRINGS[lang]
        await update.message.reply_text(s['START_MSG_1'], parse_mode="HTML")
        await update.message.reply_text(
            s['START_MSG_2'],
            reply_markup=main_menu(lang),
            parse_mode="HTML"
        )


# Expose as proper handlers
balance_handler  = MessageHandler(filters.Regex(r"^(💰 الرصيد|💰 Balance)$"),       balance_handler_fn)
history_handler  = MessageHandler(filters.Regex(r"^(📜 سجل العمليات|📜 Balance history)$"), history_handler_fn)
my_accounts_handler = MessageHandler(
    filters.Regex(r"^(📂 حساباتي|📂 My accounts)$"), 
    my_accounts_handler_fn
)
unified_back_handler = MessageHandler(filters.Regex(r"^(🔙 رجوع|🔙 Back|🔙 العودة للقائمة الرئيسية|🔙 Back to Main Menu)$"), unified_back_handler_fn)
