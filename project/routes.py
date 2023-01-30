from flask import (
    render_template,
    redirect,
    flash,
    url_for,
    Blueprint
)


from flask_login import (
    login_user,
    current_user,
    logout_user,
    login_required,
)

from .extensions import db, login_manager
from .forms import LoginForm, RegisterForm, AccountForm, TransactionForm
from .utils.db_utilities import (
    get_user,
    create_user,
    verify_user_password,
    get_account,
    create_account,
    update_account_balance,
    get_all_transactions,
    get_transaction,
    create_transaction,
    invert_transaction_type,
    get_sum_by_type
)

main = Blueprint("main", __name__)


# Used by Flask-Login to load the user from the database when it is neeeded
# for example, when a user request a page that requires authentication
# if the user is logged in it will let it proceed, if not, will be redirected to login page
@login_manager.user_loader
def load_user(user_id):
    return get_user(user_id=user_id)


# Home route
@main.route("/", methods=("GET",))
def index():

    if not current_user.is_authenticated:
        return render_template("index.html", title="Home")

    try:
        account = get_account(current_user.id)

        if not account:
            return redirect(url_for("main.create_wallet"))

    except Exception as e:
        flash(e, "danger")

    return redirect(url_for("main.dashboard"))


# Create wallet route
@main.route("/create_wallet/", methods=("GET", "POST"))
@login_required
def create_wallet():
    form = AccountForm()

    if form.validate_on_submit():
        try:
            new_account = create_account(
                current_user.id,
                form.name.data,
                form.initial_balance.data
            )

            db.session.add(new_account)
            db.session.commit()

            flash(f"Wallet Succesfully created", "success")

            return redirect(url_for('main.dashboard'))

        except Exception as e:
            flash(e, "danger")

    return render_template("create_wallet.html", title=f'Welcome {current_user.name}', form=form)


# Dashboard route
@main.route("/dashboard/", methods=("GET", "POST"))
@login_required
def dashboard():
    form = TransactionForm()

    if form.validate_on_submit():
        try:
            account = get_account(current_user.id)

            new_transaction = create_transaction(
                account.id,
                form.date.data,
                form.type.data,
                form.amount.data,
                form.description.data,
            )

            update_account_balance(account, form.amount.data, form.type.data)

            db.session.add(new_transaction)
            db.session.commit()

            flash(f"Transaction Succesfully Created", "success")

            return redirect(url_for("main.dashboard"))

        except Exception as e:
            flash(e, "danger")

    account = get_account(current_user.id)

    try:
        transactions = get_all_transactions(account.id)
        total_expenses = get_sum_by_type(transactions, type="expense")
        total_income = get_sum_by_type(transactions)

    except Exception as e:
        flash(e, "danger")

    return render_template("dashboard.html", title=f"{current_user.name}'s Dashboard", form=form, balance=account.balance, transactions=transactions, expenses=total_expenses, income=total_income)


# Delete transaction route
@main.route("/dashboard/delete_transaction/<int:transaction_id>/", methods=("POST",))
@login_required
def delete_transaction(transaction_id: int):
    try:
        transaction = get_transaction(transaction_id)
        transaction_type = invert_transaction_type(transaction.type)

        account = get_account(current_user.id)
        update_account_balance(account, transaction.amount, transaction_type)

        db.session.delete(transaction)
        db.session.commit()

    except Exception as e:
        flash(e, "danger")

    return redirect(url_for("main.dashboard"))


# Edit transaction route
@main.route("/dashboard/edit_transaction/<int:transaction_id>/", methods=("GET", "POST"))
@login_required
def edit_transaction(transaction_id: int):
    form = TransactionForm()

    try:
        transaction = get_transaction(transaction_id)
        transaction_type = invert_transaction_type(transaction.type)

        account = get_account(current_user.id)
        update_account_balance(account, transaction.amount, transaction_type)
    except Exception as e:
        flash(e, "danger")

    if form.validate_on_submit():
        try:
            transaction.type = form.type.data
            transaction.amount = form.amount.data
            transaction.description = form.description.data
            transaction.date = form.date.data

            account = get_account(current_user.id)
            update_account_balance(
                account, transaction.amount, transaction.type)

            db.session.commit()

        except Exception as e:
            flash(e, "Danger")

        return redirect(url_for("main.dashboard"))

    return render_template("edit_transaction.html", title="Edit Transaction", form=form, transaction=transaction)


# Login route
@main.route("/login/", methods=("GET", "POST"))
def login():
    form = LoginForm()

    if form.validate_on_submit():
        try:
            user = get_user(email=form.email.data)

            if not user:
                flash("User does not exists", "danger")
                return redirect(url_for("main.login"))

            if verify_user_password(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('main.index'))
            else:
                flash("Invalid name or password!", "danger")

        except Exception as e:
            flash(e, "danger")

    return render_template("auth.html", form=form, btn_action="Login")


# Register route
@main.route("/register/", methods=("GET", "POST"))
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        try:
            new_user = create_user(
                form.name.data,
                form.email.data,
                form.password.data
            )

            db.session.add(new_user)
            db.session.commit()

            flash(f"Account Succesfully created", "success")

            return redirect(url_for("main.login"))

        except Exception as e:
            flash(e, "danger")

    return render_template("auth.html", form=form, btn_action="Register")


# Logout route
@main.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))
