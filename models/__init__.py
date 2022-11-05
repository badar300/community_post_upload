from app import db


class AppModel:
    def save(self):
        db.session.add(self)
        db.session.commit()


from models.user import *
from models.community import *
from models.community_subscribe import *
from models.create_post import *

