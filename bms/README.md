# NovaBank — Bank Management System

A beginner-friendly, fully runnable bank management system built with **Python Flask + MySQL + Bootstrap 5**.
Clean MVC structure, hashed passwords, server-side validation, atomic fund transfers.

## ✨ Features

- User registration with auto-generated account number
- Login by email **or** account number (Flask-Login sessions)
- Dashboard with balance + recent transactions
- Deposit, Withdraw, Transfer (atomic, prevents overdraft)
- Full transaction history
- Admin panel: list/search/delete users, view all transactions
- Modern responsive UI (Bootstrap 5 + custom theme)

## 📁 Project Structure

```
bms/
├── run.py                  # Entry point
├── config.py               # Loads DB & app config from .env
├── requirements.txt
├── schema.sql              # Manual MySQL schema (optional)
├── .env.example
└── app/
    ├── __init__.py         # App factory + extensions
    ├── models.py           # User, Account, Transaction, Admin
    ├── forms.py            # WTForms validation
    ├── utils.py            # Helpers (account number generator)
    ├── seed.py             # Bootstraps default admin
    ├── routes/             # Controllers (MVC)
    │   ├── main.py
    │   ├── auth.py         # register/login/logout
    │   ├── banking.py      # dashboard/deposit/withdraw/transfer/history
    │   └── admin.py        # admin panel
    ├── templates/          # Jinja2 views (Bootstrap UI)
    └── static/css/style.css
```

## 🚀 Setup (VS Code / IntelliJ / Terminal)

### 1. Prerequisites
- Python 3.10+
- MySQL Server running locally
- (Optional) MySQL Workbench

### 2. Create the database

Open MySQL CLI / Workbench and run:

```sql
CREATE DATABASE bank_management_system
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

> Tables are auto-created on first run by SQLAlchemy.
> If you prefer manual schema, run `schema.sql` instead.

### 3. Install dependencies

```bash
cd bms
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 4. Configure environment

```bash
cp .env.example .env       # macOS/Linux
copy .env.example .env     # Windows
```

The defaults already match the connection details you provided:

```
mysql://root:vijayswathi@127.0.0.1:3306/bank_management_system
```

### 5. Run

```bash
python run.py
```

Open **http://127.0.0.1:5000**

## 🔑 Default Admin

| Field    | Value             |
|----------|-------------------|
| URL      | `/admin/login`    |
| Email    | `admin@bank.local` |
| Password | `admin123`        |

Change these in `.env` before deploying.

## 🧱 Database Schema

| Table        | Key Fields |
|--------------|-----------|
| `users`      | id, full_name, email (unique), phone, address, aadhaar (unique), password_hash |
| `accounts`   | id, account_number (unique), account_type (Savings/Current), balance, user_id (FK → users) |
| `transactions` | id, account_id (FK → accounts), type, amount, balance_after, counterparty, note, created_at |
| `admins`     | id, email (unique), password_hash |

Foreign keys use `ON DELETE CASCADE` so deleting a user cleans up their account + transactions.

## 🔐 Security Notes

- Passwords stored via **Werkzeug PBKDF2** (`generate_password_hash`)
- All forms protected by **CSRF tokens** (Flask-WTF)
- Server-side input validation (WTForms validators + regex)
- Transfers use a single DB transaction (atomic)

## 🗺️ Routes

| Method | Route                            | Purpose                |
|--------|----------------------------------|------------------------|
| GET    | `/`                              | Home                   |
| GET/POST | `/register`                    | Create account         |
| GET/POST | `/login`                       | User login             |
| GET    | `/logout`                        | Logout                 |
| GET    | `/dashboard`                     | User dashboard         |
| GET/POST | `/deposit`                     | Deposit funds          |
| GET/POST | `/withdraw`                    | Withdraw funds         |
| GET/POST | `/transfer`                    | Transfer funds         |
| GET    | `/history`                       | Transaction history    |
| GET/POST | `/admin/login`                 | Admin login            |
| GET    | `/admin/dashboard`               | List/search users      |
| POST   | `/admin/users/<id>/delete`       | Delete user            |
| GET    | `/admin/transactions`            | All transactions       |

## 📦 Dependencies

Installed via `pip install -r requirements.txt`:

- Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF, WTForms
- PyMySQL (MySQL driver)
- email-validator, python-dotenv, Werkzeug

Enjoy building! 💚
