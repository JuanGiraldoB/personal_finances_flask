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


def update_account_balance(account: Account, transaction_amount: int, transaction_type: str) -> None:
    if transaction_type == "income":
        account.balance += abs(transaction_amount)
    else:
        account.balance -= abs(transaction_amount)


def get_all_transactions(account_id: int) -> Transaction:
    transactions = Transaction.query.filter_by(account_id=account_id)
    return transactions


def get_transaction(id: int) -> Transaction:
    transaction = Transaction.query.filter_by(id=id).first()
    return transaction


def create_transaction(account_id: int, date: str, type: str, amount: float, description: str) -> Transaction:
    transaction = Transaction(
        account_id=account_id,
        date=date,
        type=type,
        amount=amount,
        description=description
    )

    return transaction


def invert_transaction_type(transaction_type: str) -> str:
    return "income" if transaction_type == "expense" else "expense"


def get_sum_by_type(transactions: Transaction, type="income") -> float:
    result = 0

    for transaction in transactions:
        if transaction.type == type:
            result += transaction.amount
    
    return result
