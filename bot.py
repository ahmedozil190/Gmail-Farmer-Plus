import logging
import asyncio
import json
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler

from config import BOT_TOKEN
from database import init_db
from handlers.start import start_handler, verify_sub_handler
from handlers.tasks import tasks_conv_handler
from handlers.wallet import balance_handler, history_handler, my_accounts_handler, unified_back_handler
from handlers.support import support_handler, support_handler_fn
from handlers.withdraw import withdraw_conv_handler
from handlers.referral import (
    referral_handler, referral_link_handler, 
    referral_stats_handler, referral_list_handler
)
from handlers.settings import settings_handler, currency_handler, select_currency_handler
from handlers.language import language_handler, select_lang_handler
from handlers.admin import admin_handlers

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s — %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def post_init(application: Application):
    from config import ADMIN_ID
    try:
        await application.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🚀 <b>تم تشغيل البوت بنجاح!</b>\n\nإيدي الأدمن: <code>{ADMIN_ID}</code>\nالإشعارات: مفعلة ✅",
            parse_mode="HTML"
        )
    except Exception as e:
        logging.error(f"❌ فشل إرسال إشعار التشغيل للأدمن: {e}")

def main():
    # Initialise database
    init_db()
    logger.info("✅ Database initialised.")

    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()

    # ── Conversation handlers (must be registered BEFORE plain message handlers)
    app.add_handler(tasks_conv_handler)
    app.add_handler(withdraw_conv_handler)

    # ── Command handlers
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("support", support_handler_fn))

    # ── Plain button handlers
    app.add_handler(balance_handler)
    app.add_handler(history_handler)
    app.add_handler(my_accounts_handler)
    app.add_handler(referral_handler)
    app.add_handler(referral_link_handler)
    app.add_handler(referral_stats_handler)
    app.add_handler(referral_list_handler)
    app.add_handler(settings_handler)
    app.add_handler(currency_handler)
    app.add_handler(select_currency_handler)
    app.add_handler(language_handler)
    app.add_handler(select_lang_handler)
    app.add_handler(support_handler)
    app.add_handler(unified_back_handler)
    app.add_handler(CallbackQueryHandler(verify_sub_handler, pattern="^verify_sub$"))

    # ── Admin commands
    for handler in admin_handlers:
        app.add_handler(handler)

    # ── Event Loop Setup (Fix for Python 3.14+) ──────────────────────────────
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    print("\n" + "="*40)
    print("🚀 GMAIL BOT V3.0 - NEW LOGIC ACTIVE")
    print("="*40 + "\n")
    logger.info("🚀 Bot is running…")
    
    # Set Menu Button for Mini App
    from config import DASHBOARD_URL
    dashboard_url = DASHBOARD_URL
    if dashboard_url and "Add_In_DotEnv" not in dashboard_url:

        import urllib.request
        try:
            menu_data = json.dumps({
                "menu_button": {
                    "type": "web_app",
                    "text": "Open App",
                    "web_app": {"url": f"{dashboard_url}/app/"}
                }
            }).encode("utf-8")
            req = urllib.request.Request(
                f"https://api.telegram.org/bot{BOT_TOKEN}/setChatMenuButton",
                data=menu_data,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=5):
                logger.info(f"✅ Menu button set to: {dashboard_url}/app/")
        except Exception as e:
            logger.warning(f"⚠️ Failed to set menu button: {e}")
    
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
