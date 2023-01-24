from wtforms import (
    StringField,
    PasswordField,
    SelectField,
    FloatField,
    BooleanField,
    IntegerField,
    DateField,
    TextAreaField,
)

from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, EqualTo, Email, Regexp, Optional
import email_validator
from flask_login import current_user
from wtforms import ValidationError, validators
from models import User


class register_form(FlaskForm):
    name = StringField(
        validators=[InputRequired(),
                    Length(
                        3, 20, message="Provide a name that has between 3 and 20 characters"),
                    Regexp(
            "^[A-Za-z][A-Za-z0-9_.]*$",
            0,
            "Names must have only letters, " "numbers, dots or underscores",
        ),
        ]
    )

    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    password = PasswordField(validators=[InputRequired(), Length(8, 72)])
    verify_password = PasswordField(
        validators=[
            InputRequired(),
            Length(8, 72),
            EqualTo("password", message="Passwords must match !"),
        ]
    )

    # WTForms automatically calls the methods that start with "validate_"
    # Is called after the form is submitted and the form fields are validated.
    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Email already registered!")

    # WTForms automatically calls the methods that start with "validate_"
    # Is called after the form is submitted and the form fields are validated.
    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("Username already taken!")


class login_form(FlaskForm):
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=72)])

    # Placeholder labels to enable form rendering
    username = StringField(
        validators=[Optional()]
    )

class account_form(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(5, 30)])
    initial_balance = FloatField(validators=[InputRequired(), validators.NumberRange(min=0)])

class transaction_form(FlaskForm):
    amount = FloatField(validators=[InputRequired()])
    description = StringField(validators=[Length(0, 100)])
    date = DateField(validators=[InputRequired()])
    
    type_choices = [("income", "Income"), ("expense", "Expense")]
    type = SelectField(choices=type_choices, validators=[InputRequired()])