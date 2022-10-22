import json

from api.signup import *
from app import app
from models import User
from tests import PostUpload
from mock import patch


class TestSignUp(PostUpload):
    def setUp(self):
        User.query.delete()

    @patch('api.signup.email_authentication_code', return_value='sent')
    def test_signup_api(self, email_authentication_code):
        with app.test_client() as c:
            response = c.post("/signup", content_type='application/json', data=json.dumps({'username': "test", "email": "test@test.com", "password": "12345"}))
            self.assertEqual(response.status_code, 200)
