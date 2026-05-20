"""Admin panel — separate login + management."""
from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request, session, abort
from flask_login import login_user, logout_user, current_user
from app import db
from app.models import Admin, User, Account, Transaction
from app.forms import AdminLoginForm

admin_bp = Blueprint("admin", __name__)


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or session.get("role") != "admin":
            flash("Admin login required.", "warning")
            return redirect(url_for("admin.login"))
        return f(*args, **kwargs)
    return wrapper


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data.lower().strip()).first()
        if admin and admin.check_password(form.password.data):
            login_user(admin)
            session["role"] = "admin"
            flash("Welcome, admin.", "success")
            return redirect(url_for("admin.dashboard"))
        flash("Invalid admin credentials.", "danger")
    return render_template("admin_login.html", form=form)


@admin_bp.route("/logout")
def logout():
    logout_user()
    session.pop("role", None)
    flash("Admin logged out.", "info")
    return redirect(url_for("main.home"))


@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    q = request.args.get("q", "").strip()
    users_q = User.query
    if q:
        # search by account number, email or name
        account = Account.query.filter_by(account_number=q).first()
        if account:
            users_q = users_q.filter(User.id == account.user_id)
        else:
            users_q = users_q.filter(
                (User.email.ilike(f"%{q}%")) | (User.full_name.ilike(f"%{q}%"))
            )
    users = users_q.order_by(User.created_at.desc()).all()
    stats = {
        "users": User.query.count(),
        "accounts": Account.query.count(),
        "transactions": Transaction.query.count(),
    }
    return render_template("admin_dashboard.html", users=users, q=q, stats=stats)


@admin_bp.route("/users/<int:user_id>/delete", methods=["POST"])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    try:
        db.session.delete(user)
        db.session.commit()
        flash(f"Deleted user {user.email}", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Delete failed: {e}", "danger")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/transactions")
@admin_required
def transactions():
    txns = Transaction.query.order_by(Transaction.created_at.desc()).limit(500).all()
    return render_template("admin_transactions.html", transactions=txns)
