from wtforms.validators import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, User


engine = create_engine('postgresql://catalog:password@localhost/catalog')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class Unique(object):
    """Unique class that used in form validation to
       check if element is in db or not
    """
    def __init__(self, model, field, message=u'This element already exists.'):
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form, field):
        check = session.query(self.model).\
            filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)
