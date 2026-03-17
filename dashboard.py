import os
from functools import wraps
from flask import Flask, render_template, request, Response, redirect, url_for, flash, session
import asyncio
import traceback
import json
import urllib.request
from telegram import Bot
import database
from config import GMAIL_PRICE, REFERRAL_BONUS, MIN_WITHDRAW, BOT_TOKEN, MIN_WITHDRAW_METHODS_USD

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Auth configuration
def check_auth(username, password):
    user = os.getenv("DASHBOARD_USER", "admin")
    pwd  = os.getenv("DASHBOARD_PASS", "admin1234")
    return username == user and password == pwd

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if check_auth(username, password):
            session['logged_in'] = True
            flash('Successfully logged in.', 'success')
            next_url = request.args.get('next')
            return redirect(next_url or url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# ── Context Processors ───────────────────────────────────────────────────────
@app.context_processor
def inject_stats():
    # Pass basic stats to all templates (for sidebar etc if needed)
    total_users, approved, pending, paid = database.get_stats()
    # Also pending withdrawals
    w_pending = len(database.get_pending_withdrawals())
    return dict(
        stats_pending_tasks=pending,
        stats_pending_withdrawals=w_pending
    )


# ── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
@requires_auth
def index():
    total_users, approved, pending, paid = database.get_stats()
    con = database._conn()
    total_withdrawn_count = con.execute("SELECT COUNT(*) as c FROM withdrawals WHERE status='completed'").fetchone()["c"]
    recent_tasks = con.execute("SELECT * FROM submissions ORDER BY submitted_at DESC LIMIT 5").fetchall()
    con.close()
    
    return render_template("index.html", 
                           total_users=total_users, 
                           approved_tasks=approved, 
                           pending_tasks=pending, 
                           total_paid=paid,
                           total_withdrawn_count=total_withdrawn_count,
                           recent_tasks=recent_tasks)

@app.route("/users")
@requires_auth
def users():
    search = request.args.get("q", "").strip()
    con = database._conn()
    
    query = """
        SELECT 
            u.*,
            (SELECT COALESCE(SUM(amount), 0) FROM withdrawals w WHERE w.user_id = u.user_id AND w.status = 'completed') as total_withdrawn,
            (SELECT COUNT(*) FROM submissions s WHERE s.user_id = u.user_id AND s.status = 'approved') as approved_count,
            (SELECT COUNT(*) FROM submissions s WHERE s.user_id = u.user_id AND s.status = 'rejected') as rejected_count
        FROM users u
    """
    
    if search:
        query += " WHERE u.username LIKE ? OR u.full_name LIKE ? OR CAST(u.user_id AS TEXT) LIKE ?"
        search_term = f"%{search}%"
        users_list = con.execute(query + " ORDER BY u.join_date DESC", (search_term, search_term, search_term)).fetchall()
    else:
        users_list = con.execute(query + " ORDER BY u.join_date DESC").fetchall()
        
    con.close()
    return render_template("users.html", users=users_list, search_query=search)

@app.route("/users/status/<int:user_id>", methods=["POST"])
@requires_auth
def user_status(user_id):
    new_status = request.form.get("status")
    if new_status in ["active", "banned"]:
        database.set_user_status(user_id, new_status)
        flash(f"User #{user_id} status updated to {new_status}.", "success")
    return redirect(url_for("users", q=request.args.get("q", "")))

@app.route("/users/balance/<int:user_id>", methods=["POST"])
@requires_auth
def user_balance(user_id):
    try:
        amount = float(request.form.get("amount", 0))
        action = request.form.get("action")
        if action == "add":
            database.adjust_user_balance(user_id, amount)
            flash(f"Added ${amount:.2f} to User #{user_id}.", "success")
        elif action == "remove":
            database.adjust_user_balance(user_id, -amount)
            flash(f"Removed ${amount:.2f} from User #{user_id}.", "success")
    except ValueError:
        flash("Invalid amount entered.", "danger")
    return redirect(url_for("users", q=request.args.get("q", "")))

@app.route("/tasks")
@requires_auth
def tasks():
    con = database._conn()
    tasks_list = con.execute("SELECT * FROM submissions ORDER BY submitted_at DESC").fetchall()
    con.close()
    return render_template("tasks.html", tasks=tasks_list)

@app.route("/tasks/<action>/<int:task_id>", methods=["POST"])
@requires_auth
def handle_task(action, task_id):
    if action == "approve":
        result = database.approve_submission(task_id)
        if result:
            flash(f"Task #{task_id} approved successfully.", "success")
            # Note: GUI approval happens here, but notifying the user requires hitting the Telegram API.
            # For a pure DB architecture, we would ideally enqueue a message for the bot to send,
            # but for MVP, we just approve it in DB. The user sees it in their balance.
        else:
            flash(f"Failed to approve Task #{task_id}.", "danger")
    elif action == "reject":
        reason = request.form.get("reason", "Not specified")
        result = database.reject_submission(task_id, reason)
        if result:
            flash(f"Task #{task_id} rejected.", "warning")
        else:
            flash(f"Failed to reject Task #{task_id}.", "danger")
            
    return redirect(url_for("tasks"))

@app.route("/withdrawals")
@requires_auth
def withdrawals():
    status_filter = request.args.get("status", "all")
    user_search = request.args.get("user_id", "").strip()
    date_filter = request.args.get("date", "")
    
    con = database._conn()
    query = "SELECT * FROM withdrawals WHERE 1=1"
    params = []
    
    if status_filter != "all":
        query += " AND status = ?"
        params.append(status_filter)
        
    if user_search:
        query += " AND CAST(user_id AS TEXT) LIKE ?"
        params.append(f"%{user_search}%")
        
    if date_filter:
        query += " AND created_at LIKE ?"
        params.append(f"{date_filter}%")
        
    query += " ORDER BY created_at DESC"
    
    w_list = con.execute(query, params).fetchall()
    con.close()
    
    return render_template("withdrawals.html", 
                           withdrawals=w_list, 
                           current_status=status_filter,
                           search_user=user_search,
                           d_date=date_filter)

@app.route("/withdrawals/paid/<int:wid>", methods=["POST"])
@requires_auth
def mark_paid(wid):
    try:
        from strings import STRINGS
        result = database.complete_withdrawal(wid)
        if result:
            user = database.get_user(result["user_id"])
            lang = user["language"] if user and user["language"] in STRINGS else "ar"
            currency_pref = user["currency"] if user else 'USD'
            
            from utils.currency import format_currency_dual
            display_cur = currency_pref
            if "Vodafone" in result["method"] and currency_pref == 'USD':
                display_cur = 'EGP'
            
            amount_text = format_currency_dual(result["amount"], display_cur, lang)

            msg = STRINGS[lang]["WITHDRAW_PAID"].format(
                amount_text=amount_text,
                method=result["method"].replace('💳','').replace('🟡','').replace('🟢','').replace('💎','').strip(),
                wallet=result["wallet_address"]
            )
            try:
                url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                data = json.dumps({"chat_id": result["user_id"], "text": msg, "parse_mode": "HTML"}).encode('utf-8')
                req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
                with urllib.request.urlopen(req, timeout=5) as response:
                    pass
            except Exception as e:
                with open("crash.log", "a", encoding="utf-8") as f:
                    f.write(f"Notification error: {str(e)}\n")
        flash(f"Withdrawal #{wid} marked as paid.", "success")
    except Exception:
        with open("crash.log", "a", encoding="utf-8") as f:
            f.write(traceback.format_exc() + "\n")
        flash("An internal error occurred. Check crash.log.", "danger")
    return redirect(url_for("withdrawals", status=request.args.get("status", "all")))

@app.route("/withdrawals/reject/<int:wid>", methods=["POST"])
@requires_auth
def reject_withdrawal_route(wid):
    try:
        from strings import STRINGS
        reason = request.form.get("reason", "No reason provided")
        result = database.reject_withdrawal(wid, reason)
        if result:
            user = database.get_user(result["user_id"])
            lang = user["language"] if user and user["language"] in STRINGS else "ar"
            currency_pref = user["currency"] if user else 'USD'
            
            from utils.currency import format_currency_dual
            display_cur = currency_pref
            if "Vodafone" in result["method"] and currency_pref == 'USD':
                display_cur = 'EGP'
            
            amount_text = format_currency_dual(result["amount"], display_cur, lang)

            msg = STRINGS[lang]["WITHDRAW_REJECTED"].format(
                amount_text=amount_text,
                wallet=result["wallet_address"]
            )
            try:
                url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                data = json.dumps({"chat_id": result["user_id"], "text": msg, "parse_mode": "HTML"}).encode('utf-8')
                req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
                with urllib.request.urlopen(req, timeout=5) as response:
                    pass
            except Exception as e:
                with open("crash.log", "a", encoding="utf-8") as f:
                    f.write(f"Notification error: {str(e)}\n")
        flash(f"Withdrawal #{wid} rejected. Funds returned to user.", "warning")
    except Exception:
        with open("crash.log", "a", encoding="utf-8") as f:
            f.write(traceback.format_exc() + "\n")
        flash("An internal error occurred. Check crash.log.", "danger")
    return redirect(url_for("withdrawals", status=request.args.get("status", "all")))

@app.route("/settings", methods=["GET", "POST"])
@requires_auth
def settings():
    if request.method == "POST":
        # In a real app writing to .env programmatically is tricky.
        # For this MVP, we will flash a message that it needs to be changed in config.py / .env.
        # Or we can write a simple regex replacement for the .env file.
        flash("Editing .env settings from GUI requires write permissions. Please restart the bot after saving.", "info")
        
        # Updated .env file directly (handled keys)
        form_data = request.form
        env_updates = {
            "GMAIL_PRICE": form_data.get("gmail_price"),
            "REFERRAL_BONUS": form_data.get("referral_bonus"),
            "MIN_WITHDRAW_VODAFONE": form_data.get("min_voda"),
            "MIN_WITHDRAW_BINANCE": form_data.get("min_binance"),
            "MIN_WITHDRAW_USDT": form_data.get("min_usdt"),
            "MIN_WITHDRAW_TRX": form_data.get("min_trx"),
        }
        
        # Update Database settings (Instant)
        database.set_setting("GMAIL_PRICE", env_updates["GMAIL_PRICE"])
        database.set_setting("REFERRAL_BONUS", env_updates["REFERRAL_BONUS"])
        database.set_setting("MIN_WITHDRAW_VODAFONE", env_updates["MIN_WITHDRAW_VODAFONE"])
        database.set_setting("MIN_WITHDRAW_BINANCE", env_updates["MIN_WITHDRAW_BINANCE"])
        database.set_setting("MIN_WITHDRAW_USDT", env_updates["MIN_WITHDRAW_USDT"])
        database.set_setting("MIN_WITHDRAW_TRX", env_updates["MIN_WITHDRAW_TRX"])

        flash("Settings updated successfully! Changes are now active for the bot.", "success")
        return redirect(url_for("settings"))

    conf = database.get_business_config()
    return render_template("settings.html", 
                           price=conf["GMAIL_PRICE"], 
                           bonus=conf["REFERRAL_BONUS"], 
                           min_voda=conf["MIN_METHODS"]["💳 Vodafone Cash"],
                           min_binance=conf["MIN_METHODS"]["🟡 Binance"],
                           min_usdt=conf["MIN_METHODS"]["🟢 USDT (BEP20)"],
                           min_trx=conf["MIN_METHODS"]["💎 TRX (TRC20)"])

@app.route("/broadcast", methods=["GET", "POST"])
@requires_auth
def broadcast():
    if request.method == "POST":
        message_text = request.form.get("message")
        if message_text:
            user_ids = database.get_all_user_ids()
            success_count = 0
            fail_count = 0
            
            async def send_broadcast():
                nonlocal success_count, fail_count
                bot = Bot(token=BOT_TOKEN)
                for uid in user_ids:
                    try:
                        await bot.send_message(chat_id=uid, text=message_text, parse_mode='HTML')
                        success_count += 1
                    except Exception as e:
                        print(f"Failed to send to {uid}: {e}")
                        fail_count += 1
            
            asyncio.run(send_broadcast())
            flash(f"Broadcast completed. Sent: {success_count}, Failed: {fail_count}", "info")
        return redirect(url_for("broadcast"))
    return render_template("broadcast.html")

if __name__ == "__main__":
    database.init_db()  # Ensure tables exist
    # Prioritize 'PORT' for Railway/Heroku, fallback to 'DASHBOARD_PORT' or 5000
    port = int(os.getenv("PORT", os.getenv("DASHBOARD_PORT", 5000)))
    app.run(host="0.0.0.0", port=port, debug=False)