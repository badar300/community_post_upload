import json

from api.signup import *
from app import app
from models import User
from tests import PostUpload
from mock import patch


class TestSignUp(PostUpload):
    def setUp(self):
        User.query.delete()
        self.setup_user()

    def test_login_api(self):
        with app.test_client() as c:
            response = c.post("/login", content_type='application/json', data=json.dumps({"email": "test@test.com", "password": "1234"}))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['email'], "test@test.com")
            # self.assertEqual(user.username, "test")
