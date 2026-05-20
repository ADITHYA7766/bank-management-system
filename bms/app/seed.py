"""Bootstrap a default admin account if none exists."""
from flask import current_app
from app import db
from app.models import Admin


def ensure_admin():
    email = current_app.config["ADMIN_EMAIL"]
    if not Admin.query.filter_by(email=email).first():
        admin = Admin(email=email)
        admin.set_password(current_app.config["ADMIN_PASSWORD"])
        db.session.add(admin)
        db.session.commit()
        print(f"[seed] Created default admin: {email}")
