from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, Category


engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class CategoryController():
    @property
    def get_categories(self):
        return session.query(Category).all()
