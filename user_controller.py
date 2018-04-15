from flask import abort
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, Category, User


engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class UserController():
    """UserController class that contains user methods
    """
    def create_user(self, user):
        """add new user in database"""
        session.add(user)
        session.commit()
