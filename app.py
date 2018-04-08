from flask import Flask, render_template, request, flash, jsonify, abort
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, User, Category, Item
from category_controller import CategoryController
from item_controller import ItemController


app = Flask(__name__)
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
category_controller = CategoryController()
item_controller = ItemController()


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
