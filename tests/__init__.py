from flask_testing import TestCase
import unittest

from app import app
from models import User


class PostUpload(TestCase, unittest.TestCase):
    def __init__(self, methodName):
        super(PostUpload, self).__init__(methodName)

    def create_app(self):
        return app

    def setup_user(self):
        user = User(username="test", email="test@test.com", password="1234", is_authenticated=True)
        user.save()
        self.user = user

