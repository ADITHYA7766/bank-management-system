"""WTForms — input validation lives here."""
from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, DecimalField, SelectField, SubmitField, TextAreaField,
)
from wtforms.validators import (
    DataRequired, Email, Length, Regexp, NumberRange, EqualTo,
)


class RegisterForm(FlaskForm):
    full_name = StringField("Full Name", validators=[DataRequired(), Length(2, 120)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    phone = StringField(
        "Phone Number",
        validators=[DataRequired(), Regexp(r"^\d{10}$", message="Enter a valid 10-digit phone")],
    )
    address = TextAreaField("Address", validators=[DataRequired(), Length(5, 255)])
    aadhaar = StringField(
        "Aadhaar Number",
        validators=[DataRequired(), Regexp(r"^\d{12}$", message="Aadhaar must be 12 digits")],
    )
    account_type = SelectField(
        "Account Type", choices=[("Savings", "Savings"), ("Current", "Current")],
        validators=[DataRequired()],
    )
    initial_deposit = DecimalField(
        "Initial Deposit (₹)", places=2,
        validators=[DataRequired(), NumberRange(min=500, message="Minimum ₹500")],
    )
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match")],
    )
    submit = SubmitField("Create Account")


class LoginForm(FlaskForm):
    identifier = StringField("Email or Account Number", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class AmountForm(FlaskForm):
    amount = DecimalField(
        "Amount (₹)", places=2,
        validators=[DataRequired(), NumberRange(min=1, message="Amount must be positive")],
    )
    note = StringField("Note (optional)", validators=[Length(max=255)])
    submit = SubmitField("Submit")


class TransferForm(FlaskForm):
    recipient_account = StringField(
        "Recipient Account Number",
        validators=[DataRequired(), Regexp(r"^\d{10,16}$", message="Invalid account number")],
    )
    amount = DecimalField(
        "Amount (₹)", places=2,
        validators=[DataRequired(), NumberRange(min=1)],
    )
    note = StringField("Note (optional)", validators=[Length(max=255)])
    submit = SubmitField("Transfer")


class AdminLoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login as Admin")
