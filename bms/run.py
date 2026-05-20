"""Entry point. Run with: python run.py"""
from app import create_app, db
from app.models import User, Account, Transaction, Admin
from app.seed import ensure_admin

app = create_app()

with app.app_context():
    db.create_all()
    ensure_admin()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
