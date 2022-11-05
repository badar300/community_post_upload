from app import db, con
from models import AppModel, User, CommunitySubscribe
from sqlalchemy.orm import relationship


class CreatePost(db.Model, AppModel):
    __tablename__ = 'create_post'
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    community_id = db.Column(db.Integer)
    post_name = db.Column(db.String(20))
    description = db.Column(db.String(256))

    @staticmethod
    def get_posts_by_user_id(user_id):
        return CreatePost.query.filter_by(user_id=user_id).all()


