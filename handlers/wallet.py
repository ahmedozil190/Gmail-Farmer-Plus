from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from database import get_balance, get_user_submissions, get_user, get_user_withdrawals, get_business_config
from keyboards import main_menu, balance_menu, history_menu
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
    user_data = get_user(user_id)
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


async def history_handler_fn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """📜 سجل العمليات — show payouts and account acceptance/rejection."""
    from utils.subscription import require_subscription
    if not await require_subscription(update, context):
        return
    if await is_banned(update, context):
        return
    user_id = update.effective_user.id
    user_data = get_user(user_id)
    lang = user_data['language'] if user_data else 'ar'
    currency_pref = user_data['currency'] if user_data else 'USD'
    s = STRINGS.get(lang, STRINGS['ar'])
    
    # Store for navigation
    context.user_data['parent_menu'] = 'balance'
    
    subs = get_user_submissions(user_id)
    withdraws = get_user_withdrawals(user_id)
    
    # Combine into events
    events = [] # each event: (datetime_str, type, data)
    for sub in subs:
        events.append((sub['submitted_at'], 'submission', sub))
    for w in withdraws:
        events.append((w['created_at'], 'withdrawal', w))
    
    # Sort events by date descending
    events.sort(key=lambda x: x[0], reverse=True)

    if not events:
        await update.message.reply_text(s['HISTORY_EMPTY'], reply_markup=history_menu(lang))
        return

    # User requested specific formatting for history...
    lines = []
    for dt, etype, edata in events:
        date_str = dt[:16].replace('T', ', ')
        if etype == 'withdrawal':
            from utils.currency import format_currency_dual
            amt_text = format_currency_dual(edata['amount'], currency_pref, lang)
            lines.append(
                f"⚪️ <b>Balance payout to {edata['method']}</b>: {edata['wallet_address']}\n"
                f"Balance: -{amt_text}\n"
                f"Date: {date_str} (GMT)\n"
            )
        else: # submission
            status = edata['status']
            email = edata['gmail_account']
            sub_id = edata['id']
            if 'price' in edata.keys():
                sub_price = edata['price']
            else:
                conf = get_business_config()
                sub_price = conf["GMAIL_PRICE"]
            
            if status == 'approved':
                from utils.currency import format_currency_dual
                reward_text = format_currency_dual(sub_price, currency_pref, lang)
                lines.append(
                    f"🟢 <b>Account acceptance</b>:\n"
                    f"{email} (ID: #{sub_id})\n"
                    f"Hold: -{reward_text}\n"
                    f"Balance: +{reward_text}\n"
                    f"Date: {date_str} (GMT)\n"
                )
            elif status == 'rejected':
                from utils.currency import format_currency_dual
                reward_text = format_currency_dual(sub_price, currency_pref, lang)
                lines.append(
                    f"🔴 <b>Account: {email} unavailable</b>\n"
                    f"Order ID: #{sub_id}\n"
                    f"Hold: -{reward_text}\n"
                    f"Date: {date_str} (GMT)\n"
                )
    
    full_text = "\n".join(lines)
    if len(full_text) > 4000:
        chunks = [full_text[i:i+4000] for i in range(0, len(full_text), 4000)]
        for chunk in chunks:
            await update.message.reply_text(chunk, parse_mode="HTML", disable_web_page_preview=True)
    else:
        await update.message.reply_text(full_text, parse_mode="HTML", reply_markup=history_menu(lang), disable_web_page_preview=True)


async def my_accounts_handler_fn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """📂 حساباتي — show all user submissions."""
    from utils.subscription import require_subscription
    if not await require_subscription(update, context):
        return
    if await is_banned(update, context):
        return
    user_id = update.effective_user.id
    user_data = get_user(user_id)
    lang = user_data['language'] if user_data else 'ar'
    s = STRINGS.get(lang, STRINGS['ar'])
    
    subs = get_user_submissions(user_id)
    if not subs:
        text = s['MY_ACCOUNTS_EMPTY']
    else:
        subs.sort(key=lambda x: x['id'], reverse=True)
        lines = [s['MY_ACCOUNTS_TITLE']]
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
        text = "\n".join(lines)

    await update.message.reply_text(text, parse_mode="HTML", reply_markup=main_menu(lang))


async def unified_back_handler_fn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Unified 'Back' handler that looks at context.user_data['parent_menu']."""
    user_id = update.effective_user.id
    user_data = get_user(user_id)
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
my_accounts_handler = MessageHandler(filters.Regex(r"^(📂 حساباتي|📂 My accounts)$"), my_accounts_handler_fn)
unified_back_handler = MessageHandler(filters.Regex(r"^(🔙 رجوع|🔙 Back|🔙 العودة للقائمة الرئيسية|🔙 Back to Main Menu)$"), unified_back_handler_fn)
