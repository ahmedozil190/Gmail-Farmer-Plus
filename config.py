import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ── Bot Credentials ──────────────────────────────────────────────────────────
# ملاحظة: يفضل وضع القيم الحقيقية في ملف .env وليس هنا مباشرة
BOT_TOKEN  = os.getenv("BOT_TOKEN", "Enter_Your_Token_In_DotEnv")

# تحويل آمن للـ ID لتجنب التوقف إذا كانت القيمة نصية
_admin_id_raw = os.getenv("ADMIN_ID", "0")
if _admin_id_raw.isdigit() or (_admin_id_raw.startswith("-") and _admin_id_raw[1:].isdigit()):
    ADMIN_ID = int(_admin_id_raw)
else:
    ADMIN_ID = 0



# ── Dashboard Credentials ───────────────────────────────────────────────────
DASHBOARD_USER = os.getenv("DASHBOARD_USER", "admin")
DASHBOARD_PASS = os.getenv("DASHBOARD_PASS", "admin1234")
DASHBOARD_PORT = int(os.getenv("DASHBOARD_PORT", "5000"))
DASHBOARD_URL  = os.getenv("DASHBOARD_URL", "http://localhost:5000")


# ── Business Settings ────────────────────────────────────────────────────────
BOT_NAME       = os.getenv("BOT_NAME",      "Gmail Farmer Plus")
GMAIL_PRICE    = float(os.getenv("GMAIL_PRICE",   "0.20"))   # USD per Gmail (Manual)
GMAIL_PRICE_AUTO = float(os.getenv("GMAIL_PRICE_AUTO", "0.20")) # USD per Gmail (Auto)
MIN_WITHDRAW   = float(os.getenv("MIN_WITHDRAW",  "0.20"))   # Default USD minimum (Legacy)
BASE_CURRENCY  = "USD"
REFERRAL_BONUS = float(os.getenv("REFERRAL_BONUS", "0.01")) # USD bonus per referral task
SUPPORT_LINK   = os.getenv("SUPPORT_LINK", "@A_M_E_11")
EMAILS_CHANNEL_ID = os.getenv("EMAILS_CHANNEL_ID", "Add_In_DotEnv")
WITHDRAWALS_CHANNEL_ID = os.getenv("WITHDRAWALS_CHANNEL_ID", "Add_In_DotEnv")



# ── Payment Methods ──────────────────────────────────────────────────────────
PAYMENT_METHODS = [
    "💳 Vodafone Cash",
    "🟡 Binance",
    "🟢 USDT (BEP20)",
    "💎 TRX (TRC20)",
]

MIN_WITHDRAW_METHODS_USD = {
    "💳 Vodafone Cash": float(os.getenv("MIN_WITHDRAW_VODAFONE", "0.20")),
    "🟡 Binance":       float(os.getenv("MIN_WITHDRAW_BINANCE", "0.20")),
    "🟢 USDT (BEP20)":  float(os.getenv("MIN_WITHDRAW_USDT", "0.10")),
    "💎 TRX (TRC20)":   float(os.getenv("MIN_WITHDRAW_TRX", "0.30")),
    "DEFAULT":          float(os.getenv("MIN_WITHDRAW", "0.20"))
}
