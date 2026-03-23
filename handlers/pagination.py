from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler

async def pagination_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Dispatcher for inline pagination buttons."""
    query = update.callback_query
    data = query.data
    
    if not data.startswith("page:"):
        return
        
    _, context_name, page_num = data.split(":")
    page = int(page_num)
    
    if context_name == 'accounts':
        from handlers.wallet import my_accounts_handler_fn
        await my_accounts_handler_fn(update, context, page=page)
    elif context_name == 'referrals':
        from handlers.referral import referral_list_handler_fn
        await referral_list_handler_fn(update, context, page=page)

pagination_handler = CallbackQueryHandler(pagination_callback_handler, pattern="^page:")
