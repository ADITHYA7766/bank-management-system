"""Dashboard, deposit, withdraw, transfer, history."""
from decimal import Decimal
from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from sqlalchemy import or_
from app import db
from app.models import Account, Transaction, User
from app.forms import AmountForm, TransferForm

banking_bp = Blueprint("banking", __name__)


def _require_user_account():
    if not isinstance(current_user._get_current_object(), User):
        abort(403)
    return current_user.account


@banking_bp.route("/dashboard")
@login_required
def dashboard():
    account = _require_user_account()
    recent = Transaction.query.filter_by(account_id=account.id)\
        .order_by(Transaction.created_at.desc()).limit(5).all()
    return render_template("dashboard.html", account=account, transactions=recent)


@banking_bp.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit():
    account = _require_user_account()
    form = AmountForm()
    if form.validate_on_submit():
        amount = Decimal(form.amount.data)
        try:
            account.balance = account.balance + amount
            db.session.add(Transaction(
                account_id=account.id, type="Deposit",
                amount=amount, balance_after=account.balance,
                note=form.note.data or "Cash deposit",
            ))
            db.session.commit()
            flash(f"Deposited ₹{amount}", "success")
            return redirect(url_for("banking.dashboard"))
        except Exception as e:
            db.session.rollback()
            flash(f"Deposit failed: {e}", "danger")
    return render_template("deposit.html", form=form, account=account)


@banking_bp.route("/withdraw", methods=["GET", "POST"])
@login_required
def withdraw():
    account = _require_user_account()
    form = AmountForm()
    if form.validate_on_submit():
        amount = Decimal(form.amount.data)
        if amount > account.balance:
            flash("Insufficient balance.", "danger")
            return render_template("withdraw.html", form=form, account=account)
        try:
            account.balance = account.balance - amount
            db.session.add(Transaction(
                account_id=account.id, type="Withdraw",
                amount=amount, balance_after=account.balance,
                note=form.note.data or "Cash withdrawal",
            ))
            db.session.commit()
            flash(f"Withdrew ₹{amount}", "success")
            return redirect(url_for("banking.dashboard"))
        except Exception as e:
            db.session.rollback()
            flash(f"Withdrawal failed: {e}", "danger")
    return render_template("withdraw.html", form=form, account=account)


@banking_bp.route("/transfer", methods=["GET", "POST"])
@login_required
def transfer():
    account = _require_user_account()
    form = TransferForm()
    if form.validate_on_submit():
        recipient = Account.query.filter_by(account_number=form.recipient_account.data.strip()).first()
        amount = Decimal(form.amount.data)
        if not recipient:
            flash("Recipient account not found.", "danger")
        elif recipient.id == account.id:
            flash("You cannot transfer to your own account.", "danger")
        elif amount > account.balance:
            flash("Insufficient balance.", "danger")
        else:
            try:
                # Atomic: both updates in a single transaction
                account.balance = account.balance - amount
                recipient.balance = recipient.balance + amount

                db.session.add(Transaction(
                    account_id=account.id, type="Transfer-Out",
                    amount=amount, balance_after=account.balance,
                    counterparty=recipient.account_number,
                    note=form.note.data or f"Transfer to {recipient.account_number}",
                ))
                db.session.add(Transaction(
                    account_id=recipient.id, type="Transfer-In",
                    amount=amount, balance_after=recipient.balance,
                    counterparty=account.account_number,
                    note=form.note.data or f"Transfer from {account.account_number}",
                ))
                db.session.commit()
                flash(f"Transferred ₹{amount} to {recipient.account_number}", "success")
                return redirect(url_for("banking.dashboard"))
            except Exception as e:
                db.session.rollback()
                flash(f"Transfer failed: {e}", "danger")
    return render_template("transfer.html", form=form, account=account)


@banking_bp.route("/history")
@login_required
def history():
    account = _require_user_account()
    txns = Transaction.query.filter_by(account_id=account.id)\
        .order_by(Transaction.created_at.desc()).all()
    return render_template("history.html", account=account, transactions=txns)
