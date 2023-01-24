from models import User, Account, Transaction
from app import bcrypt

# TODO: annotate functions


def get_user(email=None, user_id=None) -> User:
    if user_id:
        user = User.query.get(user_id)
    else:
        user = User.query.filter_by(email=email).first()

    return user


def create_user(name: str, email: str, password: str) -> User:
    user = User(
        name=name,
        email=email,
        password=bcrypt.generate_password_hash(password).decode('utf8')
    )

    return user


def verify_user_password(user_password: str, input_password: str) -> bool:
    return bcrypt.check_password_hash(user_password, input_password)


def get_account(user_id: int) -> Account:
    account = Account.query.filter_by(user_id=user_id).first()
    return account


def create_account(user_id: int, name: str, balance: float) -> Account:
    account = Account(
        user_id=user_id,
        name=name,
        balance=balance
    )

    return account


def get_transactions(account_id: int) -> Transaction:
    transactions = Transaction.query.filter_by(account_id=account_id)
    return transactions


def create_transaction(account_id: int, date: str, type: str, amount: float, description: str) -> Transaction:
    transaction = Transaction(
        account_id=account_id,
        date=date,
        type=type,
        amount=amount,
        description=description
    )

    return transaction