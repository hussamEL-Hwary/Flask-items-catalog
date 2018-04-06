from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from passlib.apps import custom_app_context as pwd_context


Base = declarative_base()


class User(Base):
    """
        Class user maps user properties to DB table

        Attributes:
            id: user unique id
            username: username for login
            email: user email
            password: user hashed password
    """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), index=True)
    email = Column(String)
    password = Column(String(64))

    """convert password to hashed password"""
    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    """verify entered password against hashed password """
    def verify_password(self, password):
        return pwd_context.verify(password, self.password)


class Category(Base):
    """
        Class category maps app categories to DB table

        Attributes:
            id: category unique id
            name: a string contains category name
    """
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)


class Item(Base):
    """
        Class item maps different user items to DB table

        Attributes:
            id: unique id for item
            title: a string contains item title
            description: a string contains description about item
            time_created: contains create date and time of a specific item
            user_id: foreign key that specify which user created the item
            category_id: foreign key specify which category item belongs to
    """
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    title = Column(String(32), nullable=False)
    description = Column(String, nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey('user.id'))
    category_id = Column(Integer, ForeignKey('category.id'))
    user = relationship(User)
    category = relationship(Category)


engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
