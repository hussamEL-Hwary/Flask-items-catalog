from wtforms import Form, BooleanField, StringField,\
    validators, PasswordField, SelectField, TextAreaField
from wtforms.validators import DataRequired, \
    Email, Length, Required, EqualTo
from validator_util import Unique
from model import User
from user_controller import UserController
from category_controller import CategoryController

user_controller = UserController()
category_controller = CategoryController()


# sign up form
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


# login form
class LoginForm(Form):
    """class LoginForm that contains info required to login user
    Attributes:
        name: name of user
        email: user email
    """
    email = StringField(
        'email', validators=
        [Required(message="email Required"),
         Email("invalid email address")])

    password = PasswordField('password', validators=
        [DataRequired(message="password required")])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        re = Form.validate(self)
        if not re:
            return False

        user = user_controller.get_user_by_email(self.email.data)
        if user is None:
            self.user.errors.append("unknown email")
            return False

        if not user.verify_password(self.password.data):
            self.password.errors.append("invalid password")
            return False

        self.user = user
        return True


# new item form
class NewItemForm(Form):
    """class NewItemForm that contains info required to add new item
        Attributes:
            title: item title
            description: item description
            category: category that item belongs to
        """
    title = StringField(
        'title', validators=
        [DataRequired(message="title required"),
         Length(min=5,
                message="title must be at least 5 characters")])

    description = TextAreaField(
        'description', validators=
        [DataRequired(message="description required"),
         Length(min=10,
                message="description must be at least 10 characters")])

    category = SelectField(
        'category', validators=
        [DataRequired(message="select category")], coerce=int)
