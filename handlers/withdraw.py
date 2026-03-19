"""
Withdrawal conversation:
  المهام → ask method → ask amount → ask wallet address → submit
"""
import logging
from telegram import Update, Bot
from telegram.ext import (
    ContextTypes, ConversationHandler, MessageHandler, filters
)
from database import get_balance, add_withdrawal, get_user, get_business_config
from keyboards import main_menu, cancel_keyboard, payment_methods_keyboard
from config import ADMIN_ID, PAYMENT_METHODS, WITHDRAWALS_CHANNEL_ID, BOT_TOKEN
from strings import STRINGS
from utils.ban_check import is_banned
import html
import asyncio
from datetime import datetime
from utils.currency import get_exchange_rate, format_currency_dual

# Logger
logger = logging.getLogger("bot")

# States
W_METHOD, W_AMOUNT, W_WALLET, W_CONFIRM = range(4)

CONFIRM_FILTER = filters.Regex(r"^(✅ تأكيد السحب|✅ Confirm Withdrawal)$")
EDIT_FILTER    = filters.Regex(r"^(✏️ تعديل|✏️ Edit)$")

CANCEL_FILTER  = filters.Regex(r"^(🔙 رجوع|🔙 Back)$")
METHODS_FILTER = filters.Regex(r"^(💳 Vodafone Cash|🟡 Binance|🟢 USDT \(BEP20\)|💎 TRX \(TRC20\))$")


async def withdraw_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Withdraw entry triggered by user {update.effective_user.id}")
    try:
        if await is_banned(update, context):
            return
        user_id = update.effective_user.id
        user_data = get_user(user_id)
        lang = user_data['language'] if user_data else 'ar'
        context.user_data['lang'] = lang
        currency_pref = user_data['currency'] if user_data else 'USD'
        s = STRINGS.get(lang, STRINGS['ar'])
        
        balance, pending = get_balance(user_id)
        total = balance + pending

        # Fetch dynamic settings
        conf = get_business_config()
        min_methods = conf["MIN_METHODS"]
        abs_min_usd = min(min_methods.values())
        
        if round(balance, 2) < round(abs_min_usd, 2):
            balance_info = format_currency_dual(balance, currency_pref, lang)

            context.user_data['parent_menu'] = 'balance'
            await update.message.reply_text(
                s['WITHDRAW_LOW_BALANCE'].format(balance_info=balance_info),
                parse_mode="HTML",
                reply_markup=cancel_keyboard(lang),
            )
            return ConversationHandler.END

        context.user_data["withdraw_balance"] = balance
        context.user_data["lang"] = lang
        
        avail_text = format_currency_dual(balance, currency_pref, lang)
        
        await update.message.reply_text(
            f"{s['WITHDRAW_TITLE']}"
            f"{s['WITHDRAW_AVAIL'].format(balance_text=avail_text)}"
            f"{s['WITHDRAW_METHOD_PROMPT']}",
            parse_mode="HTML",
            reply_markup=payment_methods_keyboard(lang),
        )
        return W_METHOD
    except Exception as e:
        logger.error(f"Error in withdraw_entry: {e}", exc_info=True)
        try:
            await update.message.reply_text("❌ حدث خطأ أثناء بدء عملية السحب. يرجى المحاولة مرة أخرى أو التواصل مع الدعم.")
        except:
            pass
        return ConversationHandler.END


async def receive_method(update: Update, context: ContextTypes.DEFAULT_TYPE):
    method = update.message.text.strip()
    context.user_data["withdraw_method"] = method
    balance = context.user_data.get("withdraw_balance", 0)
    lang = context.user_data.get('lang', 'ar')
    s = STRINGS.get(lang, STRINGS['ar'])

    # Fetch dynamic settings
    conf = get_business_config()
    min_methods = conf["MIN_METHODS"]
    method_min_usd = min_methods.get(method, min_methods["DEFAULT"])

    if round(balance, 2) < round(method_min_usd, 2):
        user_id = update.effective_user.id
        user_data = get_user(user_id)
        currency_pref = user_data['currency'] if user_data else 'USD'
        
        balance_info = format_currency_dual(balance, currency_pref, lang)
        min_info = format_currency_dual(method_min_usd, currency_pref, lang)
        
        # We can use WITHDRAW_LOW_BALANCE or a custom one if needed, but let's be explicit
        error_msg = (
            f"⚠️ <b>عذراً، رصيدك غير كافٍ لهذه الطريقة.</b>\n\n"
            f"💵 رصيدك: <b>{balance_info}</b>\n"
            f"📉 الحد الأدنى لـ {method}: <b>{min_info}</b>\n\n"
            f"يرجى اختيار طريقة أخرى أو العودة لاحقاً."
        ) if lang == 'ar' else (
            f"⚠️ <b>Sorry, your balance is insufficient for this method.</b>\n\n"
            f"💵 Your balance: <b>{balance_info}</b>\n"
            f"📉 Minimum for {method}: <b>{min_info}</b>\n\n"
            f"Please choose another method or come back later."
        )
        
        await update.message.reply_text(
            error_msg,
            parse_mode="HTML",
            reply_markup=payment_methods_keyboard(lang),
        )
        return W_METHOD

    await update.message.reply_text(
        s['WITHDRAW_AMOUNT_PROMPT'].format(method=method, min_w=method_min_usd, balance=balance),
        parse_mode="HTML",
        reply_markup=cancel_keyboard(lang),
    )
    return W_AMOUNT


async def receive_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang', 'ar')
    s = STRINGS.get(lang, STRINGS['ar'])
    try:
        amount_usd = float(update.message.text.strip())
    except ValueError:
        await update.message.reply_text(s['WITHDRAW_ERROR_NUM'], reply_markup=cancel_keyboard(lang))
        return W_AMOUNT

    balance_usd = context.user_data.get("withdraw_balance", 0)
    method = context.user_data.get("withdraw_method", "")

    # Fetch dynamic settings
    conf = get_business_config()
    min_methods = conf["MIN_METHODS"]
    method_min_usd = min_methods.get(method, min_methods["DEFAULT"])
    
    # Check limit in USD
    if amount_usd < method_min_usd:
        await update.message.reply_text(
            s['WITHDRAW_ERROR_MIN'].format(min_w=method_min_usd),
            reply_markup=cancel_keyboard(lang),
        )
        return W_AMOUNT
        
    if amount_usd > balance_usd:
        await update.message.reply_text(
            s['WITHDRAW_ERROR_MAX'].format(balance=balance_usd),
            reply_markup=cancel_keyboard(lang),
        )
        return W_AMOUNT

    context.user_data["withdraw_amount"] = amount_usd # Store USD in DB

    # Ask for wallet address label based on method
    if "Vodafone" in method:
        label = s.get('LBL_WALLET_VODAFONE', "رقم فودافون كاش" if lang == 'ar' else "Vodafone Cash Number")
    elif "Binance" in method:
        label = s.get('LBL_WALLET_BINANCE', "Binance Pay ID أو UID" if lang == 'ar' else "Binance Pay ID or UID")
    elif "USDT" in method:
        label = s.get('LBL_WALLET_USDT', "عنوان محفظة USDT (BEP20)" if lang == 'ar' else "USDT (BEP20) Wallet Address")
    elif "TRX" in method:
        label = s.get('LBL_WALLET_TRX', "عنوان محفظة TRX (TRC20)" if lang == 'ar' else "TRX (TRC20) Wallet Address")
    else:
        label = s.get('LBL_WALLET_GENERIC', "عنوان المحفظة (Wallet Address)" if lang == 'ar' else "Wallet Address")

    context.user_data["confirm_label"] = label
    await update.message.reply_text(
        s['WITHDRAW_WALLET_PROMPT'].format(label=label),
        reply_markup=cancel_keyboard(lang),
    )
    return W_WALLET


async def receive_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    wallet  = update.message.text.strip()
    amount  = context.user_data.get("withdraw_amount", 0)
    method  = context.user_data.get("withdraw_method", "")
    lang    = context.user_data.get('lang', 'ar')
    s       = STRINGS.get(lang, STRINGS['ar'])
    label   = context.user_data.get("confirm_label", "Address")

    context.user_data["withdraw_wallet"] = wallet

    # Show confirmation summary
    summary = (
        f"<b>{s.get('CONFIRM_TITLE', 'تأكيد طلب السحب')}</b>\n\n"
        f"🔹 {s.get('CONFIRM_METHOD', 'الطريقة:')} <b>{method}</b>\n"
        f"🔹 {s.get('CONFIRM_AMOUNT', 'المبلغ:')} <b>${amount:.2f}</b>\n"
        f"🔹 {label}: <b><code>{wallet}</code></b>\n\n"
        f"⚠️ يرجى التأكد من البيانات قبل التأكيد." if lang == 'ar' else
        f"⚠️ Please verify details before confirming."
    )

    from telegram import ReplyKeyboardMarkup
    confirm_kb = [
        ["✅ تأكيد السحب" if lang == 'ar' else "✅ Confirm Withdrawal"],
        ["✏️ تعديل" if lang == 'ar' else "✏️ Edit"]
    ]
    
    await update.message.reply_text(
        summary,
        parse_mode="HTML",
        reply_markup=ReplyKeyboardMarkup(confirm_kb, resize_keyboard=True)
    )
    return W_CONFIRM


async def receive_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    lang = context.user_data.get('lang', 'ar')
    s = STRINGS.get(lang, STRINGS['ar'])

    if "Edit" in text or "تعديل" in text:
        # Re-ask for method to allow full edit
        await update.message.reply_text(
            f"{s['WITHDRAW_METHOD_PROMPT']}",
            reply_markup=payment_methods_keyboard(lang),
        )
        return W_METHOD

    # Proceed with submission
    amount  = context.user_data.get("withdraw_amount", 0)
    method  = context.user_data.get("withdraw_method", "")
    wallet  = context.user_data.get("withdraw_wallet", "")
    user    = update.effective_user

    wid = add_withdrawal(user.id, amount, method, wallet)

    user_data = get_user(user.id)
    currency_pref = user_data['currency'] if user_data else 'USD'
    
    # If method is Vodafone Cash and currency is USD, force EGP for this message
    display_cur = currency_pref
    if "Vodafone" in method and currency_pref == 'USD':
        display_cur = 'EGP'
    
    amount_text = format_currency_dual(amount, display_cur, lang)

    # 1. Notify user immediately
    await update.message.reply_text(
        s['WITHDRAW_SUCCESS'].format(amount_text=amount_text, method=method, wallet=wallet),
        parse_mode="HTML",
        reply_markup=main_menu(lang),
    )

    # 2. Schedule notification via Job Queue
    async def _job_withdraw_notify(context: ContextTypes.DEFAULT_TYPE):
        try:
            j_data = context.job.data
            wid = j_data['wid']
            u_id = j_data['user_id']
            u_name = j_data['username']
            amount = j_data['amount']
            method = j_data['method']
            wallet = j_data['wallet']

            admin_user = get_user(ADMIN_ID)
            a_lang = admin_user['language'] if admin_user else 'ar'
            a_currency = admin_user['currency'] if admin_user else 'USD'
            a_s = STRINGS.get(a_lang, STRINGS['ar'])
            
            p_text = format_currency_dual(amount, a_currency, a_lang)
            curr_date = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            withdraw_text = a_s['ADMIN_NOTIFY_WITHDRAW'].format(
                source="Bot",
                wid=html.escape(str(wid)),
                user_name=html.escape(str(u_name)),
                user_id=html.escape(str(u_id)),
                amount_text=html.escape(str(p_text)),
                method=html.escape(str(method)),
                wallet=html.escape(str(wallet))
            )
            
            # Notify Admin
            try:
                await context.bot.send_message(chat_id=ADMIN_ID, text=withdraw_text, parse_mode="HTML", disable_web_page_preview=True, disable_notification=False)
            except Exception as e:
                logging.error(f"Withdraw Admin Job Error: {e}")

            # Notify Withdrawals Channel
            conf_notify = get_business_config()
            ch_id = conf_notify.get("WITHDRAWALS_CHANNEL_ID")
            if ch_id and "Add_In_DotEnv" not in str(ch_id):
                try:
                    await context.bot.send_message(chat_id=ch_id, text=withdraw_text, parse_mode="HTML", disable_web_page_preview=True)
                except Exception as e:
                    logging.error(f"Withdraw Channel Job Error: {e}")
        except Exception as e:
            logging.error(f"Withdraw Job Wrapper Error: {e}")

    username = f"@{user.username}" if user.username else user.full_name
    job_data = {
        'wid': wid,
        'user_id': user.id,
        'username': username,
        'amount': amount,
        'method': method,
        'wallet': wallet
    }
    context.job_queue.run_once(_job_withdraw_notify, when=3, data=job_data)

    for k in ("withdraw_balance", "withdraw_method", "withdraw_amount", "lang"):
        context.user_data.pop(k, None)
    return ConversationHandler.END


async def cancel_withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang', 'ar')
    s = STRINGS.get(lang, STRINGS['ar'])
    for k in ("withdraw_balance", "withdraw_method", "withdraw_amount"):
        context.user_data.pop(k, None)
    context.user_data.pop("lang", None)
    
    await update.message.reply_text(
        s['START_MSG_1'],
        parse_mode="HTML"
    )
    await update.message.reply_text(
        s['START_MSG_2'],
        reply_markup=main_menu(lang),
        parse_mode="HTML"
    )
    return ConversationHandler.END


# ── Conversation handler ──────────────────────────────────────────────────────
withdraw_conv_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex(r"سحب|Payout"), withdraw_entry)],
    states={
        W_METHOD:  [MessageHandler(METHODS_FILTER,                     receive_method)],
        W_AMOUNT:  [MessageHandler(filters.TEXT & ~CANCEL_FILTER,       receive_amount)],
        W_WALLET:  [MessageHandler(filters.TEXT & ~CANCEL_FILTER,       receive_wallet)],
        W_CONFIRM: [MessageHandler(filters.TEXT & ~CANCEL_FILTER,       receive_confirm)],
    },
    fallbacks=[
        MessageHandler(CANCEL_FILTER, cancel_withdraw),
    ],
    allow_reentry=True,
)
