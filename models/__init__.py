from app import db


class AppModel():
    def save(self):
        db.session.add(self)
        db.session.commit()


from models.signup import *

