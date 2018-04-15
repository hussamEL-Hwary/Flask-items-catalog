from wtforms import Form, BooleanField, StringField, validators, PasswordField
from wtforms.validators import DataRequired, Email, Length, Required, EqualTo
from validator_util import Unique
from model import User


class SignupForm(Form):
    """class SignupForm that contains info required to sign up new user
    Attributes:
        name: name of user
        email: user email
        password: user password
        confirm: user password confirmation

    """
    name = StringField(
        'name', validators=
        [DataRequired(), Length(min=2, max=32,
         message="length must be between 2 to 32 characters")])

    email = StringField(
        'email', validators=
        [Required(message="email required"),
         Email(message="invalid email address"),
         Unique(User, User.email,
         message='There is already an account with that email.')])

    password = PasswordField(
        'password', validators=
        [DataRequired(message="password required"),
         EqualTo('confirm', message="password must match"),
         Length(min=6, message="password length must be more than 6 characters")])

    confirm = PasswordField('password repeat')
