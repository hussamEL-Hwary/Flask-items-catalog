from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from model import Base, Item
from category_controller import CategoryController


engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
category_controller = CategoryController()
session = DBSession()


class ItemController():
    """ ItemController class that contains methods
        related to item
    """

    # get last added 10 items
    @property
    def get_latest_items(self):
        return session.query(Item).order_by(desc(Item.time_created))\
            .limit(10)

    # get all items in specific category
    def get_items_in_category(self, category):
        return session.query(Item).filter_by(
            category_id=category_controller.get_category_id(category)).all()

    # get item by category name and item title
    def get_item_in_category(self, category, item_title):
        return session.query(Item).filter_by(
            category_id=category_controller.get_category_id(category),
            title=item_title).first()

    # add new item to db
    def create_item(self, item):
        session.add(item)
        session.commit()

    # delete item from db
    def delete_item(self, item):
        session.delete(item)
        session.commit()
