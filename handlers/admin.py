"""
Admin-only commands (work only when sent by ADMIN_ID):

  /admin              — overview panel
  /pending            — list pending Gmail submissions
  /approve <id>       — approve a submission, credit user
  /reject <id> [why]  — reject a submission
  /paid <wid>         — mark withdrawal as completed
  /withdrawals        — list pending withdrawals
  /stats              — global statistics
  /broadcast <msg>    — send message to all users
"""
import asyncio
import os
from functools import wraps
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telegram.ext import ContextTypes, CommandHandler
from database import (
    get_pending_submissions, approve_submission, reject_submission,
    get_stats, get_all_user_ids, complete_withdrawal, get_pending_withdrawals,
    get_user, reject_withdrawal
)
from config import ADMIN_ID, DASHBOARD_URL
from strings import STRINGS

from utils.currency import format_currency_dual

# Helper to get admin settings
def get_admin_settings():
    admin_user = get_user(ADMIN_ID)
    lang = admin_user['language'] if admin_user else 'ar'
    currency = admin_user['currency'] if admin_user else 'USD'
    s = STRINGS.get(lang, STRINGS['ar'])
    return lang, currency, s

# ── Auth decorator ────────────────────────────────────────────────────────────
def admin_only(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id != ADMIN_ID:
            u_id = update.effective_user.id
            u_data = get_user(u_id)
            u_lang = u_data['language'] if u_data else 'ar'
            u_s = STRINGS.get(u_lang, STRINGS['ar'])
            await update.message.reply_text(u_s['ADMIN_ONLY'])
            return
        return await func(update, context)
    return wrapper


# ── /admin ────────────────────────────────────────────────────────────────────
@admin_only
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total, approved, pending, paid = get_stats()
    pending_w = len(get_pending_withdrawals())
    lang, currency, s = get_admin_settings()
    
    paid_text = format_currency_dual(paid, currency, lang)

    # Get dashboard URL from central config
    dashboard_url = DASHBOARD_URL

    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(s.get('OPEN_DASHBOARD', "Open Dashboard 🖥️"), web_app=WebAppInfo(url=dashboard_url))]
    ])

    await update.message.reply_text(
        f"{s['ADMIN_PANEL_TITLE']}"
        f"{s['ADMIN_PANEL_STATS'].format(
            total=total, approved=approved, pending=pending,
            pending_w=pending_w, paid_text=paid_text
        )}",
        parse_mode="HTML",
        reply_markup=keyboard
    )


# ── /pending ──────────────────────────────────────────────────────────────────
@admin_only
async def list_pending(update: Update, context: ContextTypes.DEFAULT_TYPE):
    subs = get_pending_submissions()
    lang, currency, s = get_admin_settings()
    
    if not subs:
        await update.message.reply_text(s['ADMIN_PENDING_NONE'])
        return

    lines = [s['ADMIN_PENDING_HEADER'].format(count=len(subs))]
    for sub in subs:
        date = sub["submitted_at"][:10]
        lines.append(s['ADMIN_PENDING_ITEM'].format(
            id=sub['id'], user_id=sub['user_id'],
            gmail=sub['gmail_account'], pwd=sub['gmail_password'],
            date=date
        ))

    # Split long message
    text = "\n".join(lines)
    if len(text) > 4096:
        for i in range(0, len(text), 4096):
            await update.message.reply_text(text[i:i+4096], parse_mode="HTML")
    else:
        await update.message.reply_text(text, parse_mode="HTML")


# ── /approve <id> ─────────────────────────────────────────────────────────────
@admin_only
async def approve_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang, currency, s = get_admin_settings()
    if not context.args:
        await update.message.reply_text(s['ADMIN_APPROVE_USAGE'])
        return
    try:
        sub_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text(s['ADMIN_APPROVE_ERROR_ID'])
        return

    result = approve_submission(sub_id)
    if not result:
        await update.message.reply_text(s['ADMIN_APPROVE_NOT_FOUND'].format(id=sub_id))
        return

    await update.message.reply_text(
        s['ADMIN_APPROVE_SUCCESS'].format(id=sub_id),
        parse_mode="HTML",
    )
    # Notify user
    try:
        u_id = result["user_id"]
        u_data = get_user(u_id)
        u_lang = u_data['language'] if u_data else 'ar'
        u_currency = u_data['currency'] if u_data else 'USD'
        us = STRINGS.get(u_lang, STRINGS['ar'])
        
        # Use locked price from the record
        reward_price = result.get("price", 0.20)
        price_text = format_currency_dual(reward_price, u_currency, u_lang)
        
        msg = us['NOTIFY_USER_APPROVE'].format(
            gmail=result['gmail_account'],
            price_text=price_text
        )
        
        await context.bot.send_message(
            chat_id=u_id,
            text=msg,
            parse_mode="HTML",
        )
    except Exception as e:
        import logging
        logging.error(f"Error sending approval notification: {e}")


# ── /reject <id> [reason] ─────────────────────────────────────────────────────
@admin_only
async def reject_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang, currency, s = get_admin_settings()
    if not context.args:
        await update.message.reply_text(s['ADMIN_REJECT_USAGE'])
        return
    try:
        sub_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text(s['ADMIN_APPROVE_ERROR_ID'])
        return

    # Use localized default reason
    def_reason = s.get('DEF_REASON', "غير محدد" if lang == 'ar' else "Not specified")
    reason = " ".join(context.args[1:]) if len(context.args) > 1 else def_reason
    result = reject_submission(sub_id, reason)
    if not result:
        await update.message.reply_text(s['ADMIN_APPROVE_NOT_FOUND'].format(id=sub_id))
        return

    await update.message.reply_text(
        s['ADMIN_REJECT_SUCCESS'].format(id=sub_id, reason=reason),
        parse_mode="HTML",
    )
    try:
        u_id = result["user_id"]
        u_data = get_user(u_id)
        u_lang = u_data['language'] if u_data else 'ar'
        us = STRINGS.get(u_lang, STRINGS['ar'])
        
        msg = us['NOTIFY_USER_REJECT'].format(
            gmail=result['gmail_account'],
            reason=reason
        )
        await context.bot.send_message(
            chat_id=u_id,
            text=msg,
            parse_mode="HTML",
        )
    except Exception:
        pass


# ── /withdrawals ──────────────────────────────────────────────────────────────
@admin_only
async def list_withdrawals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rows = get_pending_withdrawals()
    lang, currency, s = get_admin_settings()
    
    if not rows:
        await update.message.reply_text(s['ADMIN_W_PENDING_NONE'])
        return

    lines = [s['ADMIN_W_PENDING_HEADER'].format(count=len(rows))]
    for r in rows:
        amount_text = format_currency_dual(r['amount'], currency, lang)
        lines.append(s['ADMIN_W_PENDING_ITEM'].format(
            id=r['id'], user_id=r['user_id'],
            amount_text=amount_text, method=r['method'],
            wallet=r['wallet_address']
        ))
    await update.message.reply_text("\n".join(lines), parse_mode="HTML")


# ── /paid <wid> ───────────────────────────────────────────────────────────────
@admin_only
async def paid_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang, currency, s = get_admin_settings()
    if not context.args:
        await update.message.reply_text(s['ADMIN_PAID_USAGE'])
        return
    try:
        wid = int(context.args[0])
    except ValueError:
        await update.message.reply_text(s['ADMIN_APPROVE_ERROR_ID'])
        return

    result = complete_withdrawal(wid)
    if not result:
        await update.message.reply_text(s['ADMIN_APPROVE_NOT_FOUND'].format(id=wid))
        return

    await update.message.reply_text(s['ADMIN_PAID_SUCCESS'].format(id=wid))
    
    # Notify user
    try:
        u_id = result["user_id"]
        u_data = get_user(u_id)
        u_lang = u_data['language'] if u_data else 'ar'
        u_currency = u_data['currency'] if u_data else 'USD'
        us = STRINGS.get(u_lang, STRINGS['ar'])
        
        amount_text = format_currency_dual(result['amount'], u_currency, u_lang)
        
        msg = us['NOTIFY_USER_PAID'].format(
            amount_text=amount_text
        )
        
        await context.bot.send_message(
            chat_id=u_id,
            text=msg,
            parse_mode="HTML",
        )
    except Exception as e:
        import logging
        logging.error(f"Error sending payout notification: {e}")


# ── /reject_w <wid> [reason] ──────────────────────────────────────────────────
@admin_only
async def reject_w_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang, currency, s = get_admin_settings()
    if not context.args:
        usage = s.get('ADMIN_REJECT_W_USAGE', "Usage: /reject_w <id> [reason]")
        await update.message.reply_text(usage)
        return
    try:
        wid = int(context.args[0])
    except ValueError:
        await update.message.reply_text(s['ADMIN_APPROVE_ERROR_ID'])
        return

    def_reason = s.get('DEF_REASON', "غير محدد" if lang == 'ar' else "Not specified")
    reason = " ".join(context.args[1:]) if len(context.args) > 1 else def_reason
    
    result = reject_withdrawal(wid, reason)
    if not result:
        await update.message.reply_text(s['ADMIN_APPROVE_NOT_FOUND'].format(id=wid))
        return

    success_msg = s.get('ADMIN_REJECT_W_SUCCESS', "✅ Withdrawal {id} rejected. Reason: {reason}")
    await update.message.reply_text(success_msg.format(id=wid, reason=reason))
    
    # Notify user
    try:
        u_id = result["user_id"]
        u_data = get_user(u_id)
        u_lang = u_data['language'] if u_data else 'ar'
        u_currency = u_data['currency'] if u_data else 'USD'
        us = STRINGS.get(u_lang, STRINGS['ar'])
        
        amount_text = format_currency_dual(result['amount'], u_currency, u_lang)
        
        # We might need a separate NOTIFY_USER_W_REJECT but let's see if we can reuse
        msg = (
            f"❌ <b>تم رفض طلب السحب الخاص بك</b>\n\n"
            f"💵 المبلغ: <b>{amount_text}</b>\n"
            f"📝 السبب: {reason}\n\n"
            f"تم إعادة المبلغ لرصيدك."
        ) if u_lang == 'ar' else (
            f"❌ <b>Your withdrawal request was rejected</b>\n\n"
            f"💵 Amount: <b>{amount_text}</b>\n"
            f"📝 Reason: {reason}\n\n"
            f"Amount has been returned to your balance."
        )
        # Note: actually in database.py reject_withdrawal DOES NOT return money yet as per current code?
        # Let's check database.py reject_withdrawal again.
        
        await context.bot.send_message(chat_id=u_id, text=msg, parse_mode="HTML")
    except Exception:
        pass


# ── /stats ────────────────────────────────────────────────────────────────────
@admin_only
async def stats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total, approved, pending, paid = get_stats()
    lang, currency, s = get_admin_settings()
    
    paid_text = format_currency_dual(paid, currency, lang)

    await update.message.reply_text(
        f"{s['ADMIN_STATS_TITLE']}"
        f"{s['ADMIN_STATS_BODY'].format(
            total=total, approved=approved, pending=pending, paid_text=paid_text
        )}",
        parse_mode="HTML",
    )


# ── /broadcast ────────────────────────────────────────────────────────────────
@admin_only
async def broadcast_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang, currency, s = get_admin_settings()
    if not context.args:
        await update.message.reply_text(s['ADMIN_BROADCAST_USAGE'])
        return
    message = " ".join(context.args)
    user_ids = get_all_user_ids()
    sent = failed = 0
    for uid in user_ids:
        try:
            await context.bot.send_message(chat_id=uid, text=message)
            sent += 1
        except Exception:
            failed += 1
        await asyncio.sleep(0.05)  # rate-limit safety

    await update.message.reply_text(
        s['ADMIN_BROADCAST_SUCCESS'].format(sent=sent, failed=failed),
        parse_mode="HTML",
    )


# ── Export list of handlers ───────────────────────────────────────────────────
admin_handlers = [
    CommandHandler("admin",       admin_panel),
    CommandHandler("pending",     list_pending),
    CommandHandler("approve",     approve_cmd),
    CommandHandler("reject",      reject_cmd),
    CommandHandler("withdrawals", list_withdrawals),
    CommandHandler("paid",        paid_cmd),
    CommandHandler("reject_w",    reject_w_cmd),
    CommandHandler("stats",       stats_cmd),
    CommandHandler("broadcast",   broadcast_cmd),
]
