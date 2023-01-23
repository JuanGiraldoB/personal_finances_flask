from flask import (
    Flask,
    render_template,
    redirect,
    flash,
    url_for,
    session,
    request
)

from datetime import timedelta
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)
from werkzeug.routing import BuildError


from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash

from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

from app import create_app, db, login_manager, bcrypt
from models import User, Account, Transaction
from forms import login_form, register_form, account_form, transaction_form

# Used by Flask-Login to load the user from the database when it is neeeded
# for example, when a user request a page that requires authentication
# if the user is logged in it will let it proceed, if not, will be redirected to login page
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app = create_app()

# Home route
@app.route("/", methods=("GET", "POST"), strict_slashes=False)
def index():

    if not current_user.is_authenticated:
        return render_template("index.html", title="Home")

    try:
        account = Account.query.filter_by(user_id=current_user.id).first()

        if not account:
            return redirect(url_for("create_wallet"))

    except Exception as e:
        flash(e, "danger")

    return redirect(url_for("dashboard"))

# Create wallet route
@app.route("/create_wallet/", methods=("GET", "POST"), strict_slashes=False)
@login_required
def create_wallet():
    form = account_form()

    if form.validate_on_submit():
        try:
            acc_name = form.name.data
            acc_initial_balance = form.initial_balance.data
            acc_type = form.type.data
            acc_user_id = current_user.id

            new_account = Account(
                user_id=acc_user_id,
                name=acc_name,
                type=acc_type,
                balance=acc_initial_balance
            )

            db.session.add(new_account)
            db.session.commit()
            flash(f"Wallet Succesfully created", "success")

            return redirect(url_for('dashboard'))

        except Exception as e:
            flash(e, "danger")

    return render_template("create_wallet.html", title=f'Welcome {current_user.name}', form=form)

# Dashboard route
@app.route("/dashboard/", methods=("GET", "POST"), strict_slashes=False)
@login_required
def dashboard():
    form = transaction_form()

    if form.validate_on_submit():
        try:
            account = Account.query.filter_by(user_id=current_user.id).first()

            new_transaction = Transaction(
                account_id=account.id,
                date=form.date.data,
                type=form.type.data,
                amount=form.amount.data,
                description=form.description.data
            )

            account.balance += form.amount.data

            db.session.add(new_transaction)
            db.session.commit()
            
            flash(f"Transaction Succesfully Created", "success")

            return redirect(url_for("dashboard"))

        except Exception as e:
            print("what")
            flash(e, "danger")

    account = Account.query.filter_by(user_id=current_user.id).first()

    try:
        transactions = Transaction.query.filter_by(account_id=account.id)
    except Exception as e:
        flash(e, "danger")

    return render_template("dashboard.html", title=f"{current_user.name}'s Dashboard", form=form, balance=account.balance, transactions=transactions)

# Login route
@app.route("/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
    form = login_form()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()

            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash("Invalid name or password!", "danger")

        except Exception as e:
            flash(e, "danger")

    return render_template("auth.html", form=form, btn_action="Login")

# Register route
@app.route("/register/", methods=("GET", "POST"), strict_slashes=False)
def register():
    form = register_form()

    if form.validate_on_submit():
        try:
            email = form.email.data
            password = form.password.data
            name = form.name.data

            new_user = User(
                name=name,
                email=email,
                password=bcrypt.generate_password_hash(password).decode('utf8'),
            )

            db.session.add(new_user)
            db.session.commit()
            flash(f"Account Succesfully created", "success")

            return redirect(url_for("login"))

        except Exception as e:
            flash(e, "danger")

    return render_template("auth.html", form=form, btn_action="Register")

# Logout route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")