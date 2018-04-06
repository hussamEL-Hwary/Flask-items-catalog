from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from model import Base, Item


engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class ItemController():
    @property
    def get_latest_items(self):
        return session.query(Item).order_by(desc(Item.time_created))\
            .limit(10)
