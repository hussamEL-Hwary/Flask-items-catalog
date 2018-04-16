# flask
from flask import Flask, render_template, request, flash,\
    jsonify, abort, redirect, url_for
from flask_login import LoginManager, UserMixin, login_required,\
    login_user, logout_user, current_user
from urlparse import urlparse, urljoin
from flask import make_response
import requests
import random
import string
import httplib2
import json

# forms
from forms import SignupForm, LoginForm

# controllers
from category_controller import CategoryController
from item_controller import ItemController
from user_controller import UserController

# sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, User, Category, Item

# oauth
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError


app = Flask(__name__)
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
category_controller = CategoryController()
item_controller = ItemController()
user_controller = UserController()
login_manager = LoginManager()
login_manager.init_app(app)

# google client secret
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']


# check if url is safe
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


# load user
@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)


# sign up user
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        flash("you are logged in")
        return redirect(url_for('home'))

    signup_form = SignupForm(request.form)
    if request.method == 'POST' and signup_form.validate():
        user = User(username=signup_form.name.data, email=signup_form.email.data)
        user.hash_password(signup_form.password.data)
        user_controller.create_user(user)
        return redirect(url_for('home'))
    return render_template('signup.html', form=signup_form)


# login user by email and password
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("you are logged in")
        return redirect(url_for('home'))

    login_form = LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        login_user(login_form.user)
        flash('successfully logged in')
        next = request.args.get('next')

        if not is_safe_url(next):
            abort(404)
        return redirect(next or url_for('home'))
    return render_template('login.html', form=login_form)


@app.route('/')
def home():
    return render_template('home.html',
                           categories=category_controller.get_categories,
                           latest_items=item_controller.get_latest_items)


@app.route('/catalog/<string:category>/items')
def category_items(category):
    items = item_controller.get_items_in_category(category)
    return render_template('items.html', items=items, category=category,
                           categories=category_controller.get_categories,
                           items_length=len(items))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
