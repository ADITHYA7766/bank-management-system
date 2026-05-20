"""SQLAlchemy models — Users, Accounts, Transactions, Admin."""
from datetime import datetime
from decimal import Decimal
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    aadhaar = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    account = db.relationship(
        "Account", backref="user", uselist=False, cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Account(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    account_type = db.Column(db.Enum("Savings", "Current"), nullable=False)
    balance = db.Column(db.Numeric(14, 2), nullable=False, default=Decimal("0.00"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    transactions = db.relationship(
        "Transaction", backref="account", cascade="all, delete-orphan",
        order_by="Transaction.created_at.desc()",
    )


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(
        db.Integer, db.ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False
    )
    # 'Deposit', 'Withdraw', 'Transfer-In', 'Transfer-Out'
    type = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Numeric(14, 2), nullable=False)
    balance_after = db.Column(db.Numeric(14, 2), nullable=False)
    counterparty = db.Column(db.String(20))  # other account number (transfers)
    note = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)


class Admin(UserMixin, db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # Distinguish admin sessions from user sessions in Flask-Login
    def get_id(self):
        return f"admin-{self.id}"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
