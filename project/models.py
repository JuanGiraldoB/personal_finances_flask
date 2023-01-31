from flask_login import UserMixin
from .extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(300), unique=True, nullable=False)


class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    user = db.relationship('User', backref=db.backref('users', lazy=True, cascade="all, delete-orphan", passive_deletes=True))
    name = db.Column(db.String(80), nullable=False)
    balance = db.Column(db.Float, nullable=False)


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id', ondelete='CASCADE'))
    account = db.relationship(
        'Account', backref=db.backref('accounts', lazy=True, cascade="all, delete-orphan", passive_deletes=True))
    date = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(20), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(120), nullable=True)