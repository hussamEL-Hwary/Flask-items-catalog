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
    @property
    def get_latest_items(self):
        return session.query(Item).order_by(desc(Item.time_created))\
            .limit(10)

    def get_items_in_category(self, category):
        return session.query(Item).filter_by(
            category_id=category_controller.get_category_id(category)).all()
