import os
from functools import wraps
from flask import Flask, render_template, request, Response, redirect, url_for, flash, session
import asyncio
import traceback
import json
import urllib.request
from telegram import Bot
import database
from config import GMAIL_PRICE, REFERRAL_BONUS, MIN_WITHDRAW, BOT_TOKEN, MIN_WITHDRAW_METHODS_USD, ADMIN_ID, EMAILS_CHANNEL_ID, WITHDRAWALS_CHANNEL_ID
from strings import STRINGS
from utils.currency import format_currency_dual

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.errorhandler(Exception)
def handle_exception(e):
    with open("crash.log", "a", encoding="utf-8") as f:
        f.write(f"GLOBAL 500 ERROR: {traceback.format_exc()}\n")
    return "Internal Server Error - Check crash.log", 500

# Auth configuration
def check_auth(username, password):
    from config import DASHBOARD_USER, DASHBOARD_PASS
    return username == DASHBOARD_USER and password == DASHBOARD_PASS


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
            import database
            from strings import DASHBOARD_STRINGS
            lang = database.get_business_config().get("DASHBOARD_LANG", "en")
            flash(DASHBOARD_STRINGS.get(lang, DASHBOARD_STRINGS["ar"])['ALERT_LOGIN_SUCCESS'], 'success')
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
def inject_globals():
    from strings import DASHBOARD_STRINGS
    conf = database.get_business_config()
    lang = conf.get("DASHBOARD_LANG", "en")
    strings = DASHBOARD_STRINGS.get(lang, DASHBOARD_STRINGS["ar"])

    # Pass basic stats to all templates (for sidebar etc if needed)
    total_users, approved, pending, paid = database.get_stats()
    # Also pending withdrawals
    w_pending = len(database.get_pending_withdrawals())
    return dict(
        stats_pending_tasks=pending,
        stats_pending_withdrawals=w_pending,
        strings=strings,
        dash_lang=lang,
        config=conf
    )


# ── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
@requires_auth
def index():
    con = database._conn()
    
    # User Stats
    total_users = con.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    banned_users = con.execute("SELECT COUNT(*) FROM users WHERE status = 'banned'").fetchone()[0]
    
    # Task Stats
    total_tasks = con.execute("SELECT COUNT(*) FROM submissions").fetchone()[0]
    approved_tasks = con.execute("SELECT COUNT(*) FROM submissions WHERE status = 'approved'").fetchone()[0]
    pending_tasks = con.execute("SELECT COUNT(*) FROM submissions WHERE status = 'pending'").fetchone()[0]
    rejected_tasks = con.execute("SELECT COUNT(*) FROM submissions WHERE status = 'rejected'").fetchone()[0]
    
    # Withdrawal Stats
    total_withdrawals = con.execute("SELECT COUNT(*) FROM withdrawals").fetchone()[0]
    completed_withdrawals = con.execute("SELECT COUNT(*) FROM withdrawals WHERE status = 'completed'").fetchone()[0]
    pending_withdrawals = con.execute("SELECT COUNT(*) FROM withdrawals WHERE status = 'pending'").fetchone()[0]
    rejected_withdrawals = con.execute("SELECT COUNT(*) FROM withdrawals WHERE status = 'rejected'").fetchone()[0]
    
    con.close()
    
    return render_template("index.html", 
                           total_users=total_users, 
                           banned_users=banned_users,
                           total_tasks=total_tasks,
                           approved_tasks=approved_tasks, 
                           pending_tasks=pending_tasks, 
                           rejected_tasks=rejected_tasks,
                           total_withdrawals=total_withdrawals,
                           completed_withdrawals=completed_withdrawals,
                           pending_withdrawals=pending_withdrawals,
                           rejected_withdrawals=rejected_withdrawals)

@app.route("/users")
@requires_auth
def users():
    search = request.args.get("q", "").strip()
    current_status = request.args.get("status", "all")
    page = request.args.get("page", 1, type=int)
    per_page = 20
    offset = (page - 1) * per_page
    
    con = database._conn()
    query = """
        SELECT u.*, 
        (SELECT SUM(amount) FROM withdrawals WHERE user_id = u.user_id AND status = 'completed') as paid_total,
        (SELECT COUNT(*) FROM submissions WHERE user_id = u.user_id AND status = 'approved') as approved_count,
        (SELECT COUNT(*) FROM submissions WHERE user_id = u.user_id AND status = 'rejected') as rejected_count,
        u.custom_manual_price,
        u.custom_auto_price
        FROM users u
    """
    params = []
    where_clauses = []
    
    if search:
        where_clauses.append("(u.full_name LIKE ? OR u.username LIKE ? OR CAST(u.user_id AS TEXT) LIKE ?)")
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])
    
    if current_status == 'banned':
        where_clauses.append("u.status = 'banned'")
    
    where_clause = ""
    if where_clauses:
        where_clause = " WHERE " + " AND ".join(where_clauses)
        
    # Stats
    filtered_count = con.execute("SELECT COUNT(*) FROM users u" + where_clause, params).fetchone()[0]
    total_pages = (filtered_count + per_page - 1) // per_page
    
    grand_total = con.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    banned_count = con.execute("SELECT COUNT(*) FROM users WHERE status = 'banned'").fetchone()[0]
    stats = {'total': grand_total, 'banned': banned_count}
    
    users_list = con.execute(query + where_clause + " ORDER BY u.join_date DESC LIMIT ? OFFSET ?", params + [per_page, offset]).fetchall()
    con.close()
    
    return render_template("users.html", 
                           users=users_list, 
                           search_query=search,
                           current_status=current_status,
                           page=page,
                           total_pages=total_pages,
                           total_count=filtered_count,
                           stats=stats)

@app.route("/users/status/<int:user_id>", methods=["POST"])
@requires_auth
def user_status(user_id):
    new_status = request.form.get("status")
    if new_status in ["active", "banned"]:
        database.set_user_status(user_id, new_status)
        flash(f"User #{user_id} status updated to {new_status}.", "success")
    return redirect(url_for("users", q=request.args.get("q", ""), page=request.args.get("page", 1)))

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
    return redirect(url_for("users", q=request.args.get("q", ""), page=request.args.get("page", 1)))

@app.route("/users/custom_prices/<int:user_id>", methods=["POST"])
@requires_auth
def user_custom_prices(user_id):
    conf = database.get_business_config()
    lang = conf.get("DASHBOARD_LANG", "en")
    from strings import DASHBOARD_STRINGS
    s = DASHBOARD_STRINGS.get(lang, DASHBOARD_STRINGS["ar"])
    
    try:
        manual_p = request.form.get("manual_price", "").strip()
        auto_p = request.form.get("auto_price", "").strip()
        
        # Convert to float or None
        manual_val = float(manual_p) if manual_p else None
        auto_val = float(auto_p) if auto_p else None
        
        database.update_user_custom_prices(user_id, manual_val, auto_val)
        flash(s.get('ALERT_SETTINGS_SAVED', "Updated successfully!"), "success")
    except ValueError:
        flash("Invalid price values.", "danger")
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
    return redirect(url_for("users", q=request.args.get("q", ""), page=request.args.get("page", 1)))

@app.route("/tasks")
@requires_auth
def tasks():
    status_filter = request.args.get("status", "all")
    user_search = request.args.get("user_id", "").strip()
    date_filter = request.args.get("date", "")
    page = request.args.get("page", 1, type=int)
    per_page = 20
    offset = (page - 1) * per_page
    
    import datetime
    now = datetime.datetime.now()
    d1 = (now - datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    d2 = (now - datetime.timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S')
    d3 = (now - datetime.timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S')

    con = database._conn()
    base_query = " FROM submissions WHERE 1=1"
    params = []
    
    if status_filter == "1d":
        base_query += " AND status = 'pending' AND submitted_at <= ? AND submitted_at > ?"
        params.extend([d1, d2])
    elif status_filter == "2d":
        base_query += " AND status = 'pending' AND submitted_at <= ? AND submitted_at > ?"
        params.extend([d2, d3])
    elif status_filter in ["3d", "ready"]:
        base_query += " AND status = 'pending' AND submitted_at <= ?"
        params.append(d3)
    elif status_filter != "all":
        base_query += " AND status = ?"
        params.append(status_filter)
        
    if user_search:
        clean_id = user_search.lstrip('#').lstrip('0')
        base_query += " AND (CAST(user_id AS TEXT) LIKE ? OR CAST(id AS TEXT) LIKE ? OR CAST(id AS TEXT) = ? OR gmail_account LIKE ?)"
        params.extend([f"%{user_search}%", f"%{user_search}%", clean_id, f"%{user_search}%"])
        
    if date_filter:
        base_query += " AND submitted_at LIKE ?"
        params.append(f"{date_filter}%")
        
    # Stats
    total_count = con.execute("SELECT COUNT(*)" + base_query, params).fetchone()[0]
    total_pages = (total_count + per_page - 1) // per_page
    
    # Global stats for tabs
    stats_query = "SELECT status, COUNT(*) FROM submissions WHERE 1=1"
    stats_params = []
    if user_search:
        clean_id = user_search.lstrip('#').lstrip('0')
        stats_query += " AND (CAST(user_id AS TEXT) LIKE ? OR CAST(id AS TEXT) LIKE ? OR CAST(id AS TEXT) = ? OR gmail_account LIKE ?)"
        stats_params.extend([f"%{user_search}%", f"%{user_search}%", clean_id, f"%{user_search}%"])
    if date_filter:
        stats_query += " AND submitted_at LIKE ?"
        stats_params.append(f"{date_filter}%")
    stats_query += " GROUP BY status"
    raw_stats = con.execute(stats_query, stats_params).fetchall()
    stats = {row[0]: row[1] for row in raw_stats}
    stats['total'] = sum(stats.values())
    
    # Ready/Age stats (Buckets)
    def get_count(q_filter, p_filter):
        q = f"SELECT COUNT(*) FROM submissions WHERE status = 'pending' AND {q_filter}"
        p = list(p_filter)
        if user_search:
            q += " AND (CAST(user_id AS TEXT) LIKE ? OR CAST(id AS TEXT) LIKE ? OR gmail_account LIKE ?)"
            p.extend([f"%{user_search}%", f"%{user_search}%", f"%{user_search}%"])
        if date_filter:
            q += " AND submitted_at LIKE ?"
            p.append(f"{date_filter}%")
        return con.execute(q, p).fetchone()[0]

    stats['1d'] = get_count("submitted_at <= ? AND submitted_at > ?", (d1, d2))
    stats['2d'] = get_count("submitted_at <= ? AND submitted_at > ?", (d2, d3))
    stats['3d'] = get_count("submitted_at <= ?", (d3,))
    stats['ready'] = stats['3d']
        
    query = "SELECT *" + base_query + " ORDER BY submitted_at DESC LIMIT ? OFFSET ?"
    tasks_list = con.execute(query, params + [per_page, offset]).fetchall()
    con.close()
    
    import datetime
    now = datetime.datetime.now()
    three_days_ago = now - datetime.timedelta(days=3)
    
    # Process tasks to add 'is_ready' flag
    processed_tasks = []
    for t in tasks_list:
        # Convert row to dict for easier manipulation
        task_dict = dict(t)
        try:
            # Assuming submitted_at is row[index] or accessible via keys
            submitted_at = datetime.datetime.strptime(task_dict['submitted_at'], '%Y-%m-%d %H:%M:%S')
            task_dict['is_ready'] = task_dict['status'] == 'pending' and submitted_at <= three_days_ago
            
            # Simple "days ago" logic
            diff = now - submitted_at
            if diff.days >= 1:
                task_dict['age_text'] = f"{diff.days}d ago"
            else:
                task_dict['age_text'] = "Today"
        except:
            task_dict['is_ready'] = False
            task_dict['age_text'] = "N/A"
        processed_tasks.append(task_dict)
        
    return render_template("tasks.html", 
                           tasks=processed_tasks,
                           current_status=status_filter,
                           search_user=user_search,
                           d_date=date_filter,
                           page=page,
                           total_pages=total_pages,
                           total_count=total_count,
                           stats=stats)

@app.route("/tasks/<action>/<int:task_id>", methods=["POST"])
@requires_auth
def handle_task(action, task_id):
    from strings import STRINGS
    from utils.currency import format_currency_dual

    if action == "approve":
        result = database.approve_submission(task_id)
        if result:
            flash(f"Task #{task_id} approved successfully.", "success")
            # Send notification to user
            try:
                user = database.get_user(result["user_id"])
                lang = user["language"] if user and user["language"] in STRINGS else "ar"
                currency_pref = user["currency"] if user else "USD"
                reward = result["price"] if "price" in result else GMAIL_PRICE
                price_text = format_currency_dual(reward, currency_pref, lang)
                msg = STRINGS[lang]["TASK_APPROVED"].format(
                    gmail=result["gmail_account"],
                    price=price_text
                )
                url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                data = json.dumps({"chat_id": result["user_id"], "text": msg, "parse_mode": "HTML"}).encode('utf-8')
                req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
                with urllib.request.urlopen(req, timeout=5) as response:
                    pass
            except Exception as e:
                with open("crash.log", "a", encoding="utf-8") as f:
                    f.write(f"Task approve notification error: {str(e)}\n")
        else:
            flash(f"Failed to approve Task #{task_id}.", "danger")
    elif action == "reject":
        result = database.reject_submission(task_id, "")
        if result:
            flash(f"Task #{task_id} rejected.", "warning")
            # Send notification to user
            try:
                user = database.get_user(result["user_id"])
                lang = user["language"] if user and user["language"] in STRINGS else "ar"
                msg = STRINGS[lang]["TASK_REJECTED"].format(
                    gmail=result["gmail_account"]
                )
                url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                data = json.dumps({"chat_id": result["user_id"], "text": msg, "parse_mode": "HTML"}).encode('utf-8')
                req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
                with urllib.request.urlopen(req, timeout=5) as response:
                    pass
            except Exception as e:
                with open("crash.log", "a", encoding="utf-8") as f:
                    f.write(f"Task reject notification error: {str(e)}\n")
        else:
            flash(f"Failed to reject Task #{task_id}.", "danger")
            
    return redirect(url_for("tasks", 
                           status=request.args.get("status", "all"),
                           user_id=request.args.get("user_id", ""),
                           date=request.args.get("date", ""),
                           page=request.args.get("page", 1)))

@app.route("/withdrawals")
@requires_auth
def withdrawals():
    status_filter = request.args.get("status", "all")
    user_search = request.args.get("user_id", "").strip()
    date_filter = request.args.get("date", "")
    page = request.args.get("page", 1, type=int)
    per_page = 20
    offset = (page - 1) * per_page
    
    con = database._conn()
    base_query = " FROM withdrawals WHERE 1=1"
    params = []
    
    if status_filter != "all":
        base_query += " AND status = ?"
        params.append(status_filter)
        
    if user_search:
        clean_id = user_search.lstrip('#').lstrip('0')
        base_query += " AND (CAST(user_id AS TEXT) LIKE ? OR CAST(id AS TEXT) LIKE ? OR CAST(id AS TEXT) = ? OR wallet_address LIKE ?)"
        params.extend([f"%{user_search}%", f"%{user_search}%", clean_id, f"%{user_search}%"])
        
    if date_filter:
        base_query += " AND created_at LIKE ?"
        params.append(f"{date_filter}%")
        
    # Stats
    total_count = con.execute("SELECT COUNT(*)" + base_query, params).fetchone()[0]
    total_pages = (total_count + per_page - 1) // per_page
    
    # Global stats for tabs
    stats_query = "SELECT status, COUNT(*) FROM withdrawals WHERE 1=1"
    stats_params = []
    if user_search:
        clean_id = user_search.lstrip('#').lstrip('0')
        stats_query += " AND (CAST(user_id AS TEXT) LIKE ? OR CAST(id AS TEXT) LIKE ? OR CAST(id AS TEXT) = ? OR wallet_address LIKE ?)"
        stats_params.extend([f"%{user_search}%", f"%{user_search}%", clean_id, f"%{user_search}%"])
    if date_filter:
        stats_query += " AND created_at LIKE ?"
        stats_params.append(f"{date_filter}%")
    stats_query += " GROUP BY status"
    raw_stats = con.execute(stats_query, stats_params).fetchall()
    stats = {row[0]: row[1] for row in raw_stats}
    stats['total'] = sum(stats.values())
        
    query = "SELECT *" + base_query + " ORDER BY created_at DESC LIMIT ? OFFSET ?"
    w_list = con.execute(query, params + [per_page, offset]).fetchall()
    con.close()
    
    return render_template("withdrawals.html", 
                           withdrawals=w_list, 
                           current_status=status_filter,
                           search_user=user_search,
                           d_date=date_filter,
                           page=page,
                           total_pages=total_pages,
                           total_count=total_count,
                           stats=stats)

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
    return redirect(url_for("withdrawals", 
                           status=request.args.get("status", "all"),
                           user_id=request.args.get("user_id", ""),
                           date=request.args.get("date", "")))

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
    return redirect(url_for("withdrawals", 
                           status=request.args.get("status", "all"),
                           user_id=request.args.get("user_id", ""),
                           date=request.args.get("date", "")))

@app.route("/settings", methods=["GET", "POST"])
@requires_auth
def settings():
    if request.method == "POST":
        # Updated .env file directly (handled keys)
        form_data = request.form
        env_updates = {
            "GMAIL_PRICE": form_data.get("gmail_price"),
            "GMAIL_PRICE_AUTO": form_data.get("gmail_price_auto"),
            "REFERRAL_BONUS": form_data.get("referral_bonus"),
            "MIN_WITHDRAW_VODAFONE": form_data.get("min_voda"),
            "MIN_WITHDRAW_BINANCE": form_data.get("min_binance"),
            "MIN_WITHDRAW_USDT": form_data.get("min_usdt"),
            "MIN_WITHDRAW_TRX": form_data.get("min_trx"),
            "BUYING_ACTIVE": form_data.get("buying_active", "0"),
            "DASHBOARD_LANG": form_data.get("dash_lang", "ar"),
            "REQUIRED_CHANNELS": form_data.get("required_channels", ""),
            "EMAILS_CHANNEL_ID": form_data.get("emails_channel", ""),
            "WITHDRAWALS_CHANNEL_ID": form_data.get("withdrawals_channel", ""),
            "GMAIL_MANUAL_PWD": form_data.get("gmail_manual_pwd", "Aa612003@"),
        }
        
        # Update Database settings (Instant)
        database.set_setting("GMAIL_PRICE", env_updates["GMAIL_PRICE"])
        database.set_setting("GMAIL_PRICE_AUTO", env_updates["GMAIL_PRICE_AUTO"])
        database.set_setting("REFERRAL_BONUS", env_updates["REFERRAL_BONUS"])
        database.set_setting("MIN_WITHDRAW_VODAFONE", env_updates["MIN_WITHDRAW_VODAFONE"])
        database.set_setting("MIN_WITHDRAW_BINANCE", env_updates["MIN_WITHDRAW_BINANCE"])
        database.set_setting("MIN_WITHDRAW_USDT", env_updates["MIN_WITHDRAW_USDT"])
        database.set_setting("MIN_WITHDRAW_TRX", env_updates["MIN_WITHDRAW_TRX"])
        database.set_setting("BUYING_ACTIVE", env_updates["BUYING_ACTIVE"])
        database.set_setting("DASHBOARD_LANG", env_updates["DASHBOARD_LANG"])
        database.set_setting("REQUIRED_CHANNELS", env_updates["REQUIRED_CHANNELS"])
        database.set_setting("EMAILS_CHANNEL_ID", env_updates["EMAILS_CHANNEL_ID"])
        database.set_setting("WITHDRAWALS_CHANNEL_ID", env_updates["WITHDRAWALS_CHANNEL_ID"])
        database.set_setting("GMAIL_MANUAL_PWD", env_updates["GMAIL_MANUAL_PWD"])

        from strings import DASHBOARD_STRINGS
        lang = env_updates["DASHBOARD_LANG"]
        flash(DASHBOARD_STRINGS.get(lang, DASHBOARD_STRINGS["ar"])['ALERT_SETTINGS_SAVED'], "success")
        return redirect(url_for("settings"))

    conf = database.get_business_config()
    return render_template("settings.html", 
                           price=conf["GMAIL_PRICE"], 
                           price_auto=conf["GMAIL_PRICE_AUTO"],
                           bonus=conf["REFERRAL_BONUS"], 
                           min_voda=conf["MIN_METHODS"]["💳 Vodafone Cash"],
                           min_binance=conf["MIN_METHODS"]["🟡 Binance"],
                           min_usdt=conf["MIN_METHODS"]["🟢 USDT (BEP20)"],
                           min_trx=conf["MIN_METHODS"]["💎 TRX (TRC20)"],
                           buying_active=conf["BUYING_ACTIVE"],
                           required_channels=conf["REQUIRED_CHANNELS"])

@app.route("/admin/reset_global", methods=["POST"])
@requires_auth
def reset_global():
    success = database.global_bot_reset()
    lang = database.get_setting("DASHBOARD_LANG", "en")
    from strings import DASHBOARD_STRINGS
    s = DASHBOARD_STRINGS.get(lang, DASHBOARD_STRINGS["ar"])
    if success:
        flash(s['ALERT_RESET_SUCCESS'], "success")
    else:
        flash(s['ALERT_RESET_ERROR'], "danger")
    return redirect(url_for("settings"))

@app.route("/admin/reset_user", methods=["POST"])
@requires_auth
def reset_user_data():
    user_id_str = request.form.get("user_id", "").strip()
    lang = database.get_setting("DASHBOARD_LANG", "en")
    from strings import DASHBOARD_STRINGS
    s = DASHBOARD_STRINGS.get(lang, DASHBOARD_STRINGS["ar"])
    
    if not user_id_str:
        flash(s['ALERT_RESET_ERROR'], "danger")
        return redirect(url_for("settings"))
    
    try:
        user_id = int(user_id_str)
        success = database.user_data_reset(user_id)
        if success:
            flash(s['ALERT_RESET_SUCCESS'], "success")
        else:
            flash(s['ALERT_RESET_ERROR'], "danger")
    except ValueError:
        flash(s['ALERT_RESET_ERROR'], "danger")
        
    return redirect(url_for("settings"))

@app.route("/broadcast", methods=["GET", "POST"])
@requires_auth
def broadcast():
    if request.method == "POST":
        message_text = request.form.get("message")
        target_user_id = request.form.get("user_id", "").strip()
        
        if message_text:
            if target_user_id:
                # Send to specific user
                try:
                    user_ids = [int(target_user_id)]
                except ValueError:
                    flash("Invalid User ID format.", "danger")
                    return redirect(url_for("broadcast"))
            else:
                # Broadcast to all
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
            
            if target_user_id:
                if success_count > 0:
                    flash(f"Message sent successfully to User {target_user_id}.", "success")
                else:
                    flash(f"Failed to send message to User {target_user_id}. They may have blocked the bot.", "danger")
            else:
                flash(f"Broadcast completed. Sent: {success_count}, Failed: {fail_count}", "info")
                
        return redirect(url_for("broadcast"))
    return render_template("broadcast.html")


# ══════════════════════════════════════════════════════════════════════════════
# Helper for async notifications
def send_webapp_notification(chat_id, message):
    async def _send():
        try:
            bot = Bot(token=BOT_TOKEN)
            await bot.send_message(chat_id=chat_id, text=message, parse_mode='HTML', disable_notification=False)
            return True
        except Exception as e:
            with open("crash.log", "a", encoding="utf-8") as f:
                f.write(f"Notification Error [{chat_id}]: {str(e)}\n")
            return False
    return asyncio.run(_send())

import hashlib
import hmac
from urllib.parse import parse_qs, unquote

def validate_telegram_data(init_data: str) -> dict | None:
    """Validate Telegram WebApp initData using HMAC-SHA256."""
    try:
        with open("crash.log", "a", encoding="utf-8") as f:
            f.write(f"Validating initData: {init_data[:100]}...\n")
        parsed = dict(parse_qs(init_data, keep_blank_values=True))
        # Flatten single-value lists
        parsed = {k: v[0] if len(v) == 1 else v for k, v in parsed.items()}

        received_hash = parsed.pop("hash", None)
        if not received_hash:
            return None

        # Build data-check-string
        data_check = "\n".join(
            f"{k}={parsed[k]}" for k in sorted(parsed.keys())
        )

        secret_key = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
        calculated_hash = hmac.new(secret_key, data_check.encode(), hashlib.sha256).hexdigest()

        if calculated_hash != received_hash:
            with open("crash.log", "a", encoding="utf-8") as f:
                f.write(f"HMAC Mismatch!\nData Checklist:\n{data_check}\nCalc: {calculated_hash}\nRecv: {received_hash}\n")
            return None

        # Parse user JSON
        user_data = json.loads(parsed.get("user", "{}"))
        return user_data
    except Exception as e:
        with open("crash.log", "a", encoding="utf-8") as f:
            f.write(f"HMAC Validation Error: {str(e)}\n")
        return None


def get_webapp_user():
    """Get user from initData, perform auto-registration, and detect language."""
    try:
        from strings import WEBAPP_STRINGS
        init_data = request.args.get("initData") or request.headers.get("X-InitData", "")
        
        tg_user = None
        if init_data:
            tg_user = validate_telegram_data(init_data)
            if tg_user:
                session["tg_user_id"] = tg_user["id"]
        
        user_id = session.get("tg_user_id")
        if not user_id and not tg_user:
            return None, None, False

        if tg_user:
            user_id = tg_user["id"]

        # Check database and perform auto-registration
        user = database.get_user(user_id)
        if not user and tg_user:
            # Auto-register
            full_name = tg_user.get("first_name", "")
            if tg_user.get("last_name"):
                full_name += f" {tg_user['last_name']}"
            username = tg_user.get("username")
            database.create_user(user_id, username, full_name)
            user = database.get_user(user_id)
            # Use Telegram language as default if available
            lang = tg_user.get("language_code", "ar")
            if lang not in ("ar", "en"): lang = "ar"
            database.update_user_language(user_id, lang)
        
        if not user:
            return None, None, False

        # sqlite3.Row does not have a .get method, convert to dict first
        user_dict = dict(user)
        is_banned = user_dict.get("status") == "banned"
        
        lang = user_dict.get("language", "ar")
        if lang not in WEBAPP_STRINGS: lang = "ar"
        
        return user_dict, WEBAPP_STRINGS[lang], is_banned
    except Exception as e:
        print(f"get_webapp_user CRASH: {traceback.format_exc()}")
        with open("crash.log", "a", encoding="utf-8") as f:
            f.write(f"get_webapp_user CRASH: {traceback.format_exc()}\n")
        return None, None, False


@app.route("/app/")
def app_home():
    try:
        user, strings, is_banned = get_webapp_user()
        if is_banned:
            return render_template("app/banned.html", strings=strings), 403
        if not user:
            return render_template("app/error.html", user=None, strings=None), 403

        user_id = user["user_id"]
        balance = user["balance"]
        pending = user["pending_balance"]

        # Task stats
        con = database._conn()
        approved_tasks = con.execute(
            "SELECT COUNT(*) FROM submissions WHERE user_id = ? AND status = 'approved'", (user_id,)
        ).fetchone()[0]
        pending_tasks = con.execute(
            "SELECT COUNT(*) FROM submissions WHERE user_id = ? AND status = 'pending'", (user_id,)
        ).fetchone()[0]
        rejected_tasks = con.execute(
            "SELECT COUNT(*) FROM submissions WHERE user_id = ? AND status = 'rejected'", (user_id,)
        ).fetchone()[0]
        recent = con.execute(
            "SELECT * FROM submissions WHERE user_id = ? ORDER BY submitted_at DESC LIMIT 5", (user_id,)
        ).fetchall()
        con.close()

        return render_template("app/home.html",
            active_page="home",
            user=user,
            strings=strings,
            balance=balance,
            pending=pending,
            approved_tasks=approved_tasks,
            pending_tasks=pending_tasks,
            rejected_tasks=rejected_tasks,
            recent_tasks=recent
        )
    except Exception as e:
        return f"<pre>Error Route /app/:\n{traceback.format_exc()}</pre>", 500


@app.route("/app/tasks")
def app_tasks():
    user, strings, is_banned = get_webapp_user()
    if is_banned:
        return render_template("app/banned.html", strings=strings), 403
    if not user:
        return redirect(url_for("app_home"))

    user_id = user["user_id"]
    all_tasks = database.get_user_submissions(user_id)
    conf = database.get_business_config()
    manual_price = user["custom_manual_price"] if user.get("custom_manual_price") is not None else conf["GMAIL_PRICE"]
    auto_price = user["custom_auto_price"] if user.get("custom_auto_price") is not None else conf["GMAIL_PRICE_AUTO"]

    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 20
    total_tasks = len(all_tasks)
    total_pages = (total_tasks + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    tasks = all_tasks[start:end]

    return render_template("app/tasks.html",
        page=page,
        active_page="tasks",
        total_pages=total_pages,
        user=user,
        strings=strings,
        tasks=tasks,
        gmail_price=manual_price,
        gmail_price_auto=auto_price,
        buying_active=conf["BUYING_ACTIVE"]
    )


@app.route("/app/tasks/manual")
def app_task_manual():
    user, strings, is_banned = get_webapp_user()
    if is_banned:
        return render_template("app/banned.html", strings=strings), 403
    if not user:
        return redirect(url_for("app_home"))
    return render_template("app/task_manual.html", active_page="tasks", user=user, strings=strings)


@app.route("/app/tasks/auto")
def app_task_auto():
    user, strings, is_banned = get_webapp_user()
    if is_banned:
        return render_template("app/banned.html", strings=strings), 403
    if not user:
        return redirect(url_for("app_home"))
    
    from utils.name_generator import generate_account_data
    auto_data = generate_account_data()
    
    return render_template("app/task_auto.html", active_page="tasks", user=user, strings=strings, auto=auto_data)



@app.route("/app/tasks/api/generate")
def app_task_api_generate():
    user, _, is_banned = get_webapp_user()
    if is_banned or not user:
        return {"error": "Unauthorized"}, 403
        
    from utils.name_generator import generate_account_data
    auto_data = generate_account_data()
    return auto_data, 200


@app.route("/app/tasks/submit_auto", methods=["POST"])
def app_task_submit_auto():
    user, strings, is_banned = get_webapp_user()
    if is_banned or not user:
        return redirect(url_for("app_home"))

    user_id = user["user_id"]
    gmail = request.form.get("gmail", "").strip()
    password = request.form.get("password", "").strip()

    if not gmail or "@" not in gmail:
        flash(strings.get("FLASH_INVALID_GMAIL", "Invalid Gmail"), "danger")
        return redirect(url_for("app_task_start"))

    if database.is_gmail_already_submitted(gmail):
        flash(strings.get("FLASH_ALREADY_SUBMITTED", "Already submitted"), "warning")
        return redirect(url_for("app_tasks"))
        
    conf = database.get_business_config()
    auto_price = user["custom_auto_price"] if user.get("custom_auto_price") is not None else conf["GMAIL_PRICE_AUTO"]
    sub_id = database.add_submission(user_id, gmail, password, price=auto_price)

    try:
        username = f"@{user.get('username')}" if user.get('username') else user.get('full_name', 'Unknown')
        admin_user = database.get_user(ADMIN_ID)
        a_lang = admin_user['language'] if admin_user else 'ar'
        a_s = STRINGS.get(a_lang, STRINGS['ar'])
        
        gmail_price = conf.get("GMAIL_PRICE_AUTO", 0.20)
        from utils.currency import format_currency_dual
        price_text = format_currency_dual(gmail_price, 'USD', a_lang)
        from datetime import datetime
        current_date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        status_text = a_s.get('DASH_FILTER_PENDING', 'Pending')

        import html
        admin_msg = a_s['ADMIN_NOTIFY_GMAIL'].format(
            status=html.escape(str(status_text)),
            sub_id=html.escape(str(sub_id)),
            gmail=html.escape(str(gmail)),
            pwd=html.escape(str(password)),
            price=html.escape(str(price_text)),
            date=html.escape(str(current_date_str)),
            user_id=html.escape(str(user_id))
        )

        send_webapp_notification(ADMIN_ID, admin_msg)
            
        ch_id = conf.get("EMAILS_CHANNEL_ID")
        if ch_id and "Add_In_DotEnv" not in str(ch_id):
            send_webapp_notification(ch_id, admin_msg)
    except Exception as e:
        pass # Handle silently

    flash(strings.get("FLASH_TASK_SUCCESS", "Task submitted!"), "success")
    return redirect(url_for("app_tasks"))


@app.route("/app/tasks/submit", methods=["POST"])
def app_task_submit():
    user, strings, is_banned = get_webapp_user()
    if is_banned or not user:
        return redirect(url_for("app_home"))

    user_id = user["user_id"]
    gmail = request.form.get("gmail", "").strip()

    if not gmail or "@" not in gmail:
        flash(strings.get("FLASH_INVALID_GMAIL", "Invalid Gmail"), "danger")
        return redirect(url_for("app_task_start"))

    # Check if already submitted
    if database.is_gmail_already_submitted(gmail):
        flash(strings.get("FLASH_ALREADY_SUBMITTED", "Already submitted"), "warning")
        return redirect(url_for("app_tasks"))

    conf = database.get_business_config()
    manual_price = user["custom_manual_price"] if user.get("custom_manual_price") is not None else conf["GMAIL_PRICE"]
    password = conf.get("GMAIL_MANUAL_PWD", "Aa612003@")
    sub_id = database.add_submission(user_id, gmail, password, price=manual_price)

    try:
        username = f"@{user.get('username')}" if user.get('username') else user.get('full_name', 'Unknown')
        
        # Get admin language
        admin_user = database.get_user(ADMIN_ID)
        a_lang = admin_user['language'] if admin_user else 'ar'
        a_s = STRINGS.get(a_lang, STRINGS['ar'])
        
        # Dynamic stats for notification
        gmail_price = conf.get("GMAIL_PRICE", 0.20)
        from utils.currency import format_currency_dual
        price_text = format_currency_dual(gmail_price, 'USD', a_lang)
        from datetime import datetime
        current_date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        status_text = a_s.get('DASH_FILTER_PENDING', 'Pending')

        import html
        admin_msg = a_s['ADMIN_NOTIFY_GMAIL'].format(
            status=html.escape(str(status_text)),
            sub_id=html.escape(str(sub_id)),
            gmail=html.escape(str(gmail)),
            pwd=html.escape(str(password)),
            price=html.escape(str(price_text)),
            date=html.escape(str(current_date_str)),
            user_id=html.escape(str(user_id))
        )

        # Notify admin
        send_webapp_notification(ADMIN_ID, admin_msg)
            
        # Also to channel
        ch_id = conf.get("EMAILS_CHANNEL_ID")
        if ch_id and "Add_In_DotEnv" not in str(ch_id):
            send_webapp_notification(ch_id, admin_msg)
    except Exception as e:
        with open("crash.log", "a", encoding="utf-8") as f:
            f.write(f"WebApp task notification error: {str(e)}\n")

    flash(strings.get("FLASH_TASK_SUCCESS", "Task submitted!"), "success")
    return redirect(url_for("app_tasks"))


@app.route("/app/wallet")
def app_wallet():
    user, strings, is_banned = get_webapp_user()
    if is_banned:
        return render_template("app/banned.html", strings=strings), 403
    if not user:
        return redirect(url_for("app_home"))

    try:
        user_id = user["user_id"]
        balance = user["balance"]
        pending = user["pending_balance"]

        conf = database.get_business_config()
        min_methods = conf["MIN_METHODS"]
        min_withdraw = min(min_methods.values())

        # Get withdrawals
        con = database._conn()
        all_withdrawals = con.execute(
            "SELECT * FROM withdrawals WHERE user_id = ? ORDER BY created_at DESC", (user_id,)
        ).fetchall()
        con.close()

        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = 20
        total_items = len(all_withdrawals)
        total_pages = (total_items + per_page - 1) // per_page
        start = (page - 1) * per_page
        end = start + per_page
        withdrawals = all_withdrawals[start:end]

        return render_template("app/wallet.html",
            page=page,
            active_page="wallet",
            total_pages=total_pages,
            user=user,
            strings=strings,
            balance=balance,
            pending=pending,
            min_withdraw=min_withdraw,
            methods=[m for m in min_methods.keys() if m != 'DEFAULT'],
            min_methods=min_methods,
            withdrawals=withdrawals
        )
    except Exception as e:
        with open("crash.log", "a", encoding="utf-8") as f:
            f.write(f"Wallet Page Error: {traceback.format_exc()}\n")
        return f"Internal Server Error - Check crash.log", 500


@app.route("/app/wallet/withdraw", methods=["POST"])
def app_wallet_withdraw():
    user, strings, is_banned = get_webapp_user()
    if is_banned or not user:
        return redirect(url_for("app_home"))

    user_id = user["user_id"]
    balance = user["balance"]

    method = request.form.get("method", "")
    wallet = request.form.get("wallet", "").strip()
    try:
        amount = float(request.form.get("amount", 0))
    except (ValueError, TypeError):
        flash(strings.get("FLASH_INVALID_AMOUNT", "Invalid amount"), "danger")
        return redirect(url_for("app_wallet"))

    conf = database.get_business_config()
    min_methods = conf["MIN_METHODS"]
    method_min = min_methods.get(method, min_methods.get("DEFAULT", 0.50))

    if round(float(balance), 2) < round(float(method_min), 2):
        flash(strings.get("FLASH_BALANCE_BELOW_MIN", "Balance below minimum").format(method_min), "danger")
        return redirect(url_for("app_wallet"))

    if amount < method_min:
        flash(strings.get("FLASH_METHOD_MIN", "Min limit error").format(method_min), "danger")
        return redirect(url_for("app_wallet"))

    if amount > balance:
        flash(strings.get("FLASH_INSUFFICIENT", "Insufficient balance"), "danger")
        return redirect(url_for("app_wallet"))
    if not wallet:
        flash(strings.get("FLASH_NO_WALLET", "No wallet"), "danger")
        return redirect(url_for("app_wallet"))

    wid = database.add_withdrawal(user_id, amount, method, wallet)

    try:
        username = f"@{user.get('username')}" if user.get('username') else user.get('full_name', 'Unknown')
        
        # Get admin language and currency
        admin_user = database.get_user(ADMIN_ID)
        a_lang = admin_user['language'] if admin_user else 'ar'
        a_currency = admin_user['currency'] if admin_user else 'USD'
        a_s = STRINGS.get(a_lang, STRINGS['ar'])
        
        amount_text = format_currency_dual(amount, a_currency, a_lang)
        
        import html
        admin_msg = a_s['ADMIN_NOTIFY_WITHDRAW'].format(
            source="Panel",
            wid=html.escape(str(wid)), 
            user_name=html.escape(str(username)), 
            user_id=html.escape(str(user_id)),
            amount_text=html.escape(str(amount_text)), 
            method=html.escape(str(method)), 
            wallet=html.escape(str(wallet))
        )

        # Notify admin
        send_webapp_notification(ADMIN_ID, admin_msg)

        # Also to channel
        ch_id = conf.get("WITHDRAWALS_CHANNEL_ID")
        if ch_id and "Add_In_DotEnv" not in str(ch_id):
            send_webapp_notification(ch_id, admin_msg)
    except Exception as e:
        with open("crash.log", "a", encoding="utf-8") as f:
            f.write(f"WebApp withdraw notification error: {str(e)}\n")

    flash(strings.get("FLASH_WITHDRAW_SUCCESS", "Request submitted!"), "success")
    return redirect(url_for("app_wallet"))


@app.route("/app/referrals")
def app_referrals():
    user, strings, is_banned = get_webapp_user()
    if is_banned:
        return render_template("app/banned.html", strings=strings), 403
    if not user:
        return redirect(url_for("app_home"))

    user_id = user["user_id"]
    invited, active, tasks_total, profit = database.get_referral_detailed_stats(user_id)
    all_referrals = database.get_referrals_list_data(user_id)

    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 20
    total_items = len(all_referrals)
    total_pages = (total_items + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    referrals = all_referrals[start:end]

    conf = database.get_business_config()
    ref_bonus = conf["REFERRAL_BONUS"]

    bot_username = os.getenv("BOT_USERNAME", "")
    if not bot_username:
        # Try to get from bot API
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=5) as resp:
                bot_info = json.loads(resp.read().decode())
                bot_username = bot_info.get("result", {}).get("username", "")
        except Exception:
            bot_username = "your_bot"

    ref_link = f"https://t.me/{bot_username}?start=REF{user_id}"

    return render_template("app/referrals.html",
        page=page,
        active_page="referrals",
        total_pages=total_pages,
        user=user,
        strings=strings,
        ref_link=ref_link,
        ref_bonus=ref_bonus,
        invited=invited,
        active=active,
        profit=profit,
        referrals=referrals
    )



if __name__ == "__main__":
    database.init_db()  # Ensure tables exist
    # Prioritize 'PORT' for Railway/Heroku, fallback to 'DASHBOARD_PORT' or 5000
    port = int(os.getenv("PORT", os.getenv("DASHBOARD_PORT", 5000)))
    app.run(host="0.0.0.0", port=port, debug=False)