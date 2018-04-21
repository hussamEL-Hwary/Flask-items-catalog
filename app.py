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
from forms import SignupForm, LoginForm, NewItemForm

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


# google login
@app.route('/gconnect', methods=['POST'])
def gconnect():
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()

    # create new user if it isn't exist
    username = data['name']
    email = data['email']
    user = user_controller.get_user_by_email(email)
    if user is None:
        user = User(username=username, email=email)
        random_password = ''.join(random.choice(string.ascii_uppercase+string.digits)
                                  for x in xrange(16))
        user.hash_password(random_password)
        user_controller.create_user(user)

    # log user in
    login_user(user)
    flash("you are now logged in")

    # redirect to home page
    return redirect(url_for('home'))


# logout user
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


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


# show item in category
@app.route('/catalog/<string:category>/<string:item_title>')
def show_item(category, item_title):
    item = item_controller.get_item_in_category(category, item_title)
    if item is None:
        abort(404)
    return render_template('item.html', item=item)


# add item in category
@app.route('/catalog/new', methods=['GET', 'POST'])
@login_required
def add_item():
    new_item_form = NewItemForm(request.form)
    new_item_form.category.choices = [(cat.id, cat.name) for cat in session.query(Category).all()]
    if request.method == 'POST' and new_item_form.validate():
        item = Item(title=new_item_form.title.data,
                    description=new_item_form.description.data,
                    category_id=new_item_form.category.data,
                    user_id=current_user.id)
        item_controller.create_item(item)
        flash("new Item successfully added")
        return redirect(url_for('home'))

    return render_template('new_item.html', form=new_item_form)


# delete item
@app.route('/catalog/<string:category>/<string:item_title>/delete', methods=['GET', 'POST'])
@login_required
def delete_item(category, item_title):
    item = item_controller.get_item_in_category(category, item_title)
    if item is None:
        abort(404)
    if request.method == 'POST' and current_user.id == item.user.id:
        item_controller.delete_item(item)
        flash("item successfully deleted")
        return redirect(url_for('home'))
    return render_template('confirm_delete.html', item=item)


# JSON Endpoints

@app.route('/category.json')
def categories_json():
    categories = session.query(Category).all()
    return jsonify(categories=[cat.serialize for cat in categories])


@app.route('/item.json')
def items_json():
    items = session.query(Item).all()
    return jsonify(items=[item.serialize for item in items])


# handel 404 error
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# handel 401 error
@app.errorhandler(401)
def permission_denied(e):
    return render_template('401.html'), 401


if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
