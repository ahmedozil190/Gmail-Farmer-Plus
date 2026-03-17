from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from database import get_referral_detailed_stats, get_user, get_referrals_list_data, get_business_config
from keyboards import referral_menu
from strings import STRINGS
from utils.currency import format_currency_dual
from utils.ban_check import is_banned


async def referral_handler_fn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """🔗 الإحالة — referral system info."""
    if await is_banned(update, context):
        return
    user_id = update.effective_user.id
    user_data = get_user(user_id)
    lang = user_data['language'] if user_data else 'ar'
    currency = user_data['currency'] if user_data else 'USD'
    s = STRINGS.get(lang, STRINGS['ar'])
    
    # Store for navigation
    context.user_data['parent_menu'] = 'main'
    
    invited, active, tasks, profit = get_referral_detailed_stats(user_id)

    # Fetch dynamic settings
    conf = get_business_config()
    referral_bonus = conf["REFERRAL_BONUS"]

    bonus_text = format_currency_dual(referral_bonus, currency, lang)
    profit_text = format_currency_dual(profit, currency, lang)

    await update.message.reply_text(
        s['REF_MSG'].format(
            bonus_text=bonus_text,
            invited=invited,
            tasks=tasks,
            profit_text=profit_text
        ),
        parse_mode="HTML",
        reply_markup=referral_menu(lang),
    )


async def referral_link_handler_fn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Shows the user's unique referral link with detailed info."""
    user_id = update.effective_user.id
    user_data = get_user(user_id)
    lang = user_data['language'] if user_data else 'ar'
    currency = user_data['currency'] if user_data else 'USD'
    s = STRINGS.get(lang, STRINGS['ar'])
    
    bot_username = (await context.bot.get_me()).username
    ref_link = f"https://t.me/{bot_username}?start=REF{user_id}"
    
    # Matching the user's requested ref_id style if possible
    ref_id = f"REF{user_id}"

    # Fetch dynamic settings
    conf = get_business_config()
    referral_bonus = conf["REFERRAL_BONUS"]

    bonus_text = format_currency_dual(referral_bonus, currency, lang)

    await update.message.reply_text(
        s['REF_LINK_DETAILS'].format(
            link=ref_link,
            bonus_text=bonus_text,
            ref_id=ref_id
        ),
        parse_mode="HTML",
        disable_web_page_preview=False # Explicitly enable as requested ("اضغط على الرابط أعلاه لتجربته")
    )


async def referral_stats_handler_fn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Detailed stats using the new template."""
    user_id = update.effective_user.id
    user_data = get_user(user_id)
    lang = user_data['language'] if user_data else 'ar'
    currency = user_data['currency'] if user_data else 'USD'
    s = STRINGS.get(lang, STRINGS['ar'])
    
    invited, active, tasks, profit = get_referral_detailed_stats(user_id)
    ref_id = f"REF{user_id}"

    # Fetch dynamic settings
    conf = get_business_config()
    referral_bonus = conf["REFERRAL_BONUS"]

    bonus_text = format_currency_dual(referral_bonus, currency, lang)
    profit_text = format_currency_dual(profit, currency, lang)

    await update.message.reply_text(
        s['REF_STATS_MSG'].format(
            invited=invited,
            active=active,
            tasks=tasks,
            profit_text=profit_text,
            bonus_text=bonus_text,
            ref_id=ref_id
        ),
        parse_mode="HTML"
    )


async def referral_list_handler_fn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List of invited users with detailed status and profit."""
    user_id = update.effective_user.id
    user_data = get_user(user_id)
    lang = user_data['language'] if user_data else 'ar'
    currency = user_data['currency'] if user_data else 'USD'
    s = STRINGS.get(lang, STRINGS['ar'])
    
    referral_data = get_referrals_list_data(user_id)
    
    if not referral_data:
        msg = s['REF_LIST_EMPTY']
    else:
        full_msg = s['REF_LIST_HEADER'].format(count=len(referral_data))
        for i, ref in enumerate(referral_data, 1):
            name = f"@{ref['username']}" if ref['username'] else (ref['full_name'] or f"ID: {ref['user_id']}")
            
            # Profit logic
            has_earned = ref['approved_tasks'] > 0
            status_icon = "✅" if has_earned else "⏳"
            status_text = s['REF_STATUS_EARNED'] if has_earned else s['REF_STATUS_PENDING']
            
            if has_earned:
                # Fetch dynamic settings
                conf = get_business_config()
                referral_bonus = conf["REFERRAL_BONUS"]
                profit = ref['approved_tasks'] * referral_bonus
                earned_text = format_currency_dual(profit, currency, lang)
            else:
                earned_text = s['REF_EARNED_NONE']
                
            # Date formatting (D/M/YYYY)
            date_obj = datetime.fromisoformat(ref['join_date'])
            date_str = date_obj.strftime("%d/%m/%Y")
            
            # Simple Arabic numeral replacement if lang is ar
            if lang == 'ar':
                arabic_digits = "٠١٢٣٤٥٦٧٨٩"
                english_digits = "0123456789"
                trans = str.maketrans(english_digits, arabic_digits)
                date_str = date_str.translate(trans)

            full_msg += s['REF_LIST_ITEM'].format(
                index=i,
                name=name,
                status_icon=status_icon,
                status_text=status_text,
                earned_text=earned_text,
                date=date_str
            )
        msg = full_msg
    
    await update.message.reply_text(msg, parse_mode="HTML")


referral_handler = MessageHandler(filters.Regex(r"^(👥 My referrals|👥 إحالاتي|🔗 Referral)$"), referral_handler_fn)
referral_link_handler = MessageHandler(filters.Regex(r"^(🔗 رابط الإحالة|🔗 Referral Link)$"), referral_link_handler_fn)
referral_stats_handler = MessageHandler(filters.Regex(r"^(📊 إحصائيات الإحالة|📊 Referral Stats)$"), referral_stats_handler_fn)
referral_list_handler = MessageHandler(filters.Regex(r"^(👥 قائمة الإحالات|👥 Referral List)$"), referral_list_handler_fn)
