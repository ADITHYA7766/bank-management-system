"""Helper utilities."""
import random
from app.models import Account


def generate_account_number():
    """Generate a unique 12-digit account number."""
    while True:
        number = "".join(str(random.randint(0, 9)) for _ in range(12))
        if not Account.query.filter_by(account_number=number).first():
            return number
