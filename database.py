import sqlite3
from datetime import datetime
from config import GMAIL_PRICE, REFERRAL_BONUS

import os
import secrets

# Use absolute path to ensure both bot and dashboard use the same DB file
DB_PATH = os.getenv("DB_PATH")
if not DB_PATH:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "gmail_store.db")


# ── Connection helper ────────────────────────────────────────────────────────
def _conn():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c


def _generate_unique_id(table: str) -> int:
    con = _conn()
    while True:
        # Generate random 8-digit number (10,000,000 to 99,999,999)
        new_id = secrets.randbelow(90000000) + 10000000
        # Check if it exists
        exists = con.execute(f"SELECT 1 FROM {table} WHERE id = ?", (new_id,)).fetchone()
        if not exists:
            con.close()
            return new_id


# ── Initialise schema ────────────────────────────────────────────────────────
def init_db():
    con = _conn()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id         INTEGER PRIMARY KEY,
            username        TEXT,
            full_name       TEXT,
            balance         REAL    DEFAULT 0,
            pending_balance REAL    DEFAULT 0,
            referrer_id     INTEGER,
            join_date       TEXT,
            language        TEXT    DEFAULT 'ar',
            currency        TEXT    DEFAULT 'USD',
            status          TEXT    DEFAULT 'active'
        )
    """)

    # Migration: Add language column if it doesn't exist
    try:
        cur.execute("ALTER TABLE users ADD COLUMN language TEXT DEFAULT 'ar'")
    except sqlite3.OperationalError:
        pass  # Column already exists

    # Migration: Add status column if it doesn't exist
    try:
        cur.execute("ALTER TABLE users ADD COLUMN status TEXT DEFAULT 'active'")
    except sqlite3.OperationalError:
        pass

    # Migration: Add custom price columns if they don't exist
    try:
        cur.execute("ALTER TABLE users ADD COLUMN custom_manual_price REAL DEFAULT NULL")
    except sqlite3.OperationalError:
        pass
    try:
        cur.execute("ALTER TABLE users ADD COLUMN custom_auto_price REAL DEFAULT NULL")
    except sqlite3.OperationalError:
        pass

    cur.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id       INTEGER,
            gmail_account TEXT,
            gmail_password TEXT,
            status        TEXT    DEFAULT 'pending',
            submitted_at  TEXT,
            reviewed_at   TEXT,
            reject_reason TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS withdrawals (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id        INTEGER,
            amount         REAL,
            method         TEXT,
            wallet_address TEXT,
            status         TEXT DEFAULT 'pending',
            created_at     TEXT,
            reject_reason  TEXT
        )
    """)

    # Migration: Add reject_reason column if it doesn't exist
    try:
        cur.execute("ALTER TABLE withdrawals ADD COLUMN reject_reason TEXT")
    except sqlite3.OperationalError:
        pass

    # Migration: Add price column to submissions if it doesn't exist
    try:
        cur.execute(f"ALTER TABLE submissions ADD COLUMN price REAL DEFAULT {GMAIL_PRICE}")
    except sqlite3.OperationalError:
        pass

    # Migration: Add settings Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key   TEXT PRIMARY KEY,
            value TEXT
        )
    """)

    con.commit()
    con.close()


# ── User helpers ─────────────────────────────────────────────────────────────
def get_user(user_id: int):
    con = _conn()
    row = con.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
    con.close()
    return row


def create_user(user_id: int, username: str, full_name: str, referrer_id: int = None, language: str = 'ar'):
    con = _conn()
    con.execute(
        """INSERT OR IGNORE INTO users
           (user_id, username, full_name, balance, pending_balance, referrer_id, join_date, language)
           VALUES (?, ?, ?, 0, 0, ?, ?, ?)""",
        (user_id, username, full_name, referrer_id, datetime.now().isoformat(), language),
    )
    con.commit()
    con.close()


def update_user_info(user_id: int, username: str, full_name: str):
    con = _conn()
    con.execute(
        "UPDATE users SET username = ?, full_name = ? WHERE user_id = ?",
        (username, full_name, user_id)
    )
    con.commit()
    con.close()


def update_user_language(user_id: int, language: str):
    con = _conn()
    con.execute("UPDATE users SET language = ? WHERE user_id = ?", (language, user_id))
    con.commit()
    con.close()


def update_user_currency(user_id: int, currency: str):
    con = _conn()
    con.execute("UPDATE users SET currency = ? WHERE user_id = ?", (currency, user_id))
    con.commit()
    con.close()


def set_user_status(user_id: int, status: str):
    con = _conn()
    con.execute("UPDATE users SET status = ? WHERE user_id = ?", (status, user_id))
    con.commit()
    con.close()


def update_user_custom_prices(user_id: int, manual_p: float = None, auto_p: float = None):
    con = _conn()
    con.execute(
        "UPDATE users SET custom_manual_price = ?, custom_auto_price = ? WHERE user_id = ?",
        (manual_p, auto_p, user_id)
    )
    con.commit()
    con.close()


def adjust_user_balance(user_id: int, delta: float):
    con = _conn()
    # Rounding to 2 decimal places to prevent floating point precision issues
    con.execute("UPDATE users SET balance = ROUND(balance + ?, 2) WHERE user_id = ?", (delta, user_id))
    con.commit()
    con.close()


def get_balance(user_id: int):
    user = get_user(user_id)
    if user:
        return user["balance"], user["pending_balance"]
    return 0.0, 0.0


def get_all_user_ids():
    con = _conn()
    rows = con.execute("SELECT user_id FROM users").fetchall()
    con.close()
    return [r["user_id"] for r in rows]


def get_referral_detailed_stats(user_id: int):
    con = _conn()
    # Invited friends
    invited = con.execute(
        "SELECT user_id FROM users WHERE referrer_id = ?", (user_id,)
    ).fetchall()
    invited_ids = [r["user_id"] for r in invited]
    
    invited_count = len(invited_ids)
    active_count = 0
    tasks_total = 0
    profit_total = 0.0
    
    if invited_ids:
        placeholders = ', '.join(['?'] * len(invited_ids))
        
        # Total tasks (approved) by referrals
        row = con.execute(
            f"SELECT COUNT(*) as cnt FROM submissions WHERE user_id IN ({placeholders}) AND status = 'approved'",
            invited_ids
        ).fetchone()
        tasks_total = row["cnt"] if row else 0
        # Use dynamic referral bonus from DB settings
        conf = get_business_config()
        ref_bonus = conf["REFERRAL_BONUS"]
        profit_total = tasks_total * ref_bonus
        
        # Active referrals: referred users who have at least one approved task
        active_row = con.execute(
            f"SELECT COUNT(DISTINCT user_id) as cnt FROM submissions WHERE user_id IN ({placeholders}) AND status = 'approved'",
            invited_ids
        ).fetchone()
        active_count = active_row["cnt"] if active_row else 0
        
    con.close()
    return invited_count, active_count, tasks_total, profit_total


def get_referrals_list_data(referrer_id: int):
    con = _conn()
    # Get all users referred by this user
    referrals = con.execute(
        "SELECT user_id, username, full_name, join_date FROM users WHERE referrer_id = ?",
        (referrer_id,)
    ).fetchall()
    
    data = []
    for r in referrals:
        # Get approved tasks for this referral
        tasks = con.execute(
            "SELECT COUNT(*) as cnt FROM submissions WHERE user_id = ? AND status = 'approved'",
            (r["user_id"],)
        ).fetchone()["cnt"]
        
        data.append({
            "user_id": r["user_id"],
            "username": r["username"],
            "full_name": r["full_name"],
            "join_date": r["join_date"],
            "approved_tasks": tasks
        })
        
    con.close()
    return data


def get_stats():
    con = _conn()
    users = con.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    approved = con.execute("SELECT COUNT(*) FROM submissions WHERE status = 'approved'").fetchone()[0]
    pending = con.execute("SELECT COUNT(*) FROM submissions WHERE status = 'pending'").fetchone()[0]
    paid = con.execute("SELECT SUM(amount) FROM withdrawals WHERE status = 'completed'").fetchone()[0] or 0.0
    con.close()
    return users, approved, pending, float(paid)


# ── Submission helpers ───────────────────────────────────────────────────────
def add_submission(user_id: int, gmail: str, password: str, price: float = None) -> int:
    # Fetch real-time price if not provided
    if price is None:
        conf = get_business_config()
        price = conf["GMAIL_PRICE"]
    
    new_id = _generate_unique_id("submissions")
    
    con = _conn()
    cur = con.cursor()
    cur.execute(
        """INSERT INTO submissions (id, user_id, gmail_account, gmail_password, status, submitted_at, price)
           VALUES (?, ?, ?, ?, 'pending', ?, ?)""",
        (new_id, user_id, gmail, password, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), price)
    )
    # Add to pending balance
    con.execute(
        "UPDATE users SET pending_balance = pending_balance + ? WHERE user_id = ?",
        (price, user_id),
    )
    con.commit()
    con.close()
    return new_id


def get_pending_submissions():
    con = _conn()
    rows = con.execute(
        "SELECT * FROM submissions WHERE status = 'pending' ORDER BY submitted_at"
    ).fetchall()
    con.close()
    return rows


def get_user_submissions(user_id: int):
    con = _conn()
    rows = con.execute(
        "SELECT * FROM submissions WHERE user_id = ? ORDER BY submitted_at DESC",
        (user_id,),
    ).fetchall()
    con.close()
    return rows


def is_gmail_already_submitted(gmail: str) -> bool:
    con = _conn()
    row = con.execute(
        "SELECT 1 FROM submissions WHERE LOWER(gmail_account) = LOWER(?)",
        (gmail,),
    ).fetchone()
    con.close()
    return row is not None


def approve_submission(sub_id: int):
    con = _conn()
    cur = con.cursor()
    sub = cur.execute("SELECT * FROM submissions WHERE id = ?", (sub_id,)).fetchone()
    if not sub or sub["status"] != "pending":
        con.close()
        return None

    cur.execute(
        "UPDATE submissions SET status='approved', reviewed_at=? WHERE id=?",
        (datetime.now().isoformat(), sub_id),
    )
    # Use the price locked at submission time
    reward = sub["price"] if "price" in sub.keys() else GMAIL_PRICE
    cur.execute(
        """UPDATE users
           SET balance = balance + ?, pending_balance = pending_balance - ?
           WHERE user_id = ?""",
        (reward, reward, sub["user_id"]),
    )
    # Referral bonus
    ref = cur.execute(
        "SELECT referrer_id FROM users WHERE user_id = ?", (sub["user_id"],)
    ).fetchone()
    if ref and ref["referrer_id"]:
        # Dynamic referral bonus
        conf = get_business_config()
        ref_bonus = conf["REFERRAL_BONUS"]
        cur.execute(
            "UPDATE users SET balance = balance + ? WHERE user_id = ?",
            (ref_bonus, ref["referrer_id"]),
        )
    con.commit()
    result = dict(sub)
    con.close()
    return result


def reject_submission(sub_id: int, reason: str = ""):
    con = _conn()
    cur = con.cursor()
    sub = cur.execute("SELECT * FROM submissions WHERE id = ?", (sub_id,)).fetchone()
    if not sub or sub["status"] != "pending":
        con.close()
        return None

    cur.execute(
        "UPDATE submissions SET status='rejected', reviewed_at=?, reject_reason=? WHERE id=?",
        (datetime.now().isoformat(), reason, sub_id),
    )
    # Use the price locked at submission time
    reward = sub["price"] if "price" in sub.keys() else GMAIL_PRICE
    cur.execute(
        "UPDATE users SET pending_balance = pending_balance - ? WHERE user_id = ?",
        (reward, sub["user_id"]),
    )
    con.commit()
    result = dict(sub)
    con.close()
    return result


# ── Withdrawal helpers ───────────────────────────────────────────────────────
def add_withdrawal(user_id: int, amount: float, method: str, wallet: str) -> int:
    new_id = _generate_unique_id("withdrawals")
    
    con = _conn()
    cur = con.cursor()
    con.execute(
        "UPDATE users SET balance = balance - ? WHERE user_id = ?",
        (amount, user_id),
    )
    cur.execute(
        """INSERT INTO withdrawals (id, user_id, amount, method, wallet_address, status, created_at)
           VALUES (?, ?, ?, ?, ?, 'pending', ?)""",
        (new_id, user_id, amount, method, wallet, datetime.now().isoformat()),
    )
    con.commit()
    con.close()
    return new_id


def complete_withdrawal(wid: int):
    con = _conn()
    cur = con.cursor()
    row = cur.execute("SELECT * FROM withdrawals WHERE id=?", (wid,)).fetchone()
    if row:
        cur.execute("UPDATE withdrawals SET status='completed' WHERE id=?", (wid,))
        con.commit()
        result = dict(row)
        con.close()
        return result
    con.close()
    return None


def reject_withdrawal(wid: int, reason: str):
    con = _conn()
    cur = con.cursor()
    row = cur.execute("SELECT * FROM withdrawals WHERE id=?", (wid,)).fetchone()
    if row and row["status"] == "pending":
        # Refund user balance (rounded)
        cur.execute(
            "UPDATE users SET balance = ROUND(balance + ?, 2) WHERE user_id = ?",
            (row["amount"], row["user_id"])
        )
        # Update withdrawal status
        cur.execute(
            "UPDATE withdrawals SET status='rejected', reject_reason=? WHERE id=?",
            (reason, wid)
        )
        con.commit()
        result = dict(row)
        con.close()
        return result
    con.close()
    return None


def get_pending_withdrawals():
    con = _conn()
    rows = con.execute(
        "SELECT * FROM withdrawals WHERE status='pending' ORDER BY created_at"
    ).fetchall()
    con.close()
    return rows


def get_user_withdrawals(user_id: int):
    con = _conn()
    rows = con.execute(
        "SELECT * FROM withdrawals WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,),
    ).fetchall()
    con.close()
    return rows


# ── Dynamic Settings ─────────────────────────────────────────────────────────
def get_setting(key: str, default=None):
    con = _conn()
    row = con.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
    con.close()
    if row:
        return row["value"]
    return str(default) if default is not None else None

def set_setting(key: str, value: str):
    con = _conn()
    con.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, str(value)))
    con.commit()
    con.close()

def get_business_config():
    """Returns all relevant business settings as a dict with correct types."""
    from config import GMAIL_PRICE, GMAIL_PRICE_AUTO, REFERRAL_BONUS, EMAILS_CHANNEL_ID, WITHDRAWALS_CHANNEL_ID
    
    # Withdrawal Methods mapping
    voda = float(get_setting("MIN_WITHDRAW_VODAFONE", 0.20))
    bina = float(get_setting("MIN_WITHDRAW_BINANCE", 0.20))
    usdt = float(get_setting("MIN_WITHDRAW_USDT", 0.10))
    trx  = float(get_setting("MIN_WITHDRAW_TRX", 0.30))
    
    return {
        "GMAIL_PRICE":    float(get_setting("GMAIL_PRICE", GMAIL_PRICE)),
        "GMAIL_PRICE_AUTO": float(get_setting("GMAIL_PRICE_AUTO", GMAIL_PRICE_AUTO)),
        "GMAIL_MANUAL_PWD": get_setting("GMAIL_MANUAL_PWD", "Aa612003@"),
        "REFERRAL_BONUS": float(get_setting("REFERRAL_BONUS", REFERRAL_BONUS)),
        "BUYING_ACTIVE":  get_setting("BUYING_ACTIVE", "1") == "1",
        "REQUIRED_CHANNELS": get_setting("REQUIRED_CHANNELS", ""),
        "EMAILS_CHANNEL_ID":      get_setting("EMAILS_CHANNEL_ID", EMAILS_CHANNEL_ID),
        "WITHDRAWALS_CHANNEL_ID": get_setting("WITHDRAWALS_CHANNEL_ID", WITHDRAWALS_CHANNEL_ID),
        "MIN_METHODS": {
            "💳 Vodafone Cash": voda,
            "🟡 Binance":       bina,
            "🟢 USDT (BEP20)":  usdt,
            "💎 TRX (TRC20)":   trx,
            "DEFAULT":          voda # fallback
        },
        "DASHBOARD_LANG": get_setting("DASHBOARD_LANG", "en")
    }

def global_bot_reset():
    """Clears all submissions, withdrawals, and resets balances for all users."""
    con = _conn()
    try:
        con.execute("DELETE FROM submissions")
        con.execute("DELETE FROM withdrawals")
        con.execute("UPDATE users SET balance = 0, pending_balance = 0")
        con.commit()
        return True
    except Exception:
        return False
    finally:
        con.close()

def user_data_reset(user_id: int):
    """Resets balance and clears specific data for one user."""
    con = _conn()
    try:
        # Check if user exists
        exists = con.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,)).fetchone()
        if not exists:
            return False
        
        con.execute("DELETE FROM submissions WHERE user_id = ?", (user_id,))
        con.execute("DELETE FROM withdrawals WHERE user_id = ?", (user_id,))
        con.execute("UPDATE users SET balance = 0, pending_balance = 0 WHERE user_id = ?", (user_id,))
        con.commit()
        return True
    except Exception:
        return False
    finally:
        con.close()
