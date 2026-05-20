"""User registration, login, logout."""
from decimal import Decimal
from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Account, Transaction
from app.forms import RegisterForm, LoginForm
from app.utils import generate_account_number

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Uniqueness checks
        if User.query.filter_by(email=form.email.data.lower()).first():
            flash("Email already registered.", "danger")
            return render_template("register.html", form=form)
        if User.query.filter_by(aadhaar=form.aadhaar.data).first():
            flash("Aadhaar already registered.", "danger")
            return render_template("register.html", form=form)

        try:
            user = User(
                full_name=form.full_name.data.strip(),
                email=form.email.data.lower().strip(),
                phone=form.phone.data.strip(),
                address=form.address.data.strip(),
                aadhaar=form.aadhaar.data.strip(),
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.flush()  # get user.id

            initial = Decimal(form.initial_deposit.data)
            account = Account(
                account_number=generate_account_number(),
                account_type=form.account_type.data,
                balance=initial,
                user_id=user.id,
            )
            db.session.add(account)
            db.session.flush()

            # Record opening deposit
            db.session.add(Transaction(
                account_id=account.id,
                type="Deposit",
                amount=initial,
                balance_after=initial,
                note="Opening deposit",
            ))
            db.session.commit()

            flash(f"Account created! Your account number is {account.account_number}", "success")
            return redirect(url_for("auth.login"))
        except Exception as e:
            db.session.rollback()
            flash(f"Registration failed: {e}", "danger")
    return render_template("register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        identifier = form.identifier.data.strip().lower()
        # Allow login by email or account number
        user = User.query.filter_by(email=identifier).first()
        if not user:
            account = Account.query.filter_by(account_number=identifier).first()
            if account:
                user = account.user
        if user and user.check_password(form.password.data):
            login_user(user)
            session["role"] = "user"
            flash("Welcome back!", "success")
            return redirect(url_for("banking.dashboard"))
        flash("Invalid credentials.", "danger")
    return render_template("login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop("role", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("main.home"))
