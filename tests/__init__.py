from flask_testing import TestCase
import unittest

from app import app
from models import User, CommunitySubscribe, CreatePost, Community


class PostUpload(TestCase, unittest.TestCase):
    def __init__(self, methodName):
        super(PostUpload, self).__init__(methodName)
        self.user = None
        self.community = None
        self.post = None

    def create_app(self):
        return app

    def setup_user(self):
        user = User(username="test", email="test@test.com", password="1234", is_authenticated=True)
        user.save()
        self.user = user

    def setup_community(self):
        community = Community(user_id=self.user.user_id, community_name='python', description='This is python communtity')
        community.save()
        self.community = community

    def setup_post(self):
        post = CreatePost(user_id=self.user.user_id, community_id=self.community.community_id, post_name='post_name', description='description')
        post.save()
        self.post = post

