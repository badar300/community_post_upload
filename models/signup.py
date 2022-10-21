from app import db
from models import AppModel


class Signup(db.Model, AppModel):
    __tablename__ = 'signup'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    email = db.Column(db.String(256))
    password = db.Column(db.String(20))
    is_authenticated = db.Column(db.Boolean, default=False)
