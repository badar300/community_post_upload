import json

from api.signup import *
from app import app
from models import User, Community, CreatePost, CommunitySubscribe
from tests import PostUpload
from mock import patch


class TestCreatePost(PostUpload):
    def setUp(self):
        User.query.delete()
        Community.query.delete()
        CreatePost.query.delete()
        self.setup_user()
        self.setup_community()

    def test_create_post_api(self):
        with app.test_client() as c:
            response = c.post("/create_post", content_type='application/json', data=json.dumps(
                {"user_id": self.user.user_id, "community_id": self.community.community_id
                    , "post_name": "new post", "description": "this is new post"}
            ))
            self.assertEqual(response.status_code, 200)
            self.assertIsNotNone(response)
            post = CreatePost.query.count()
            self.assertEqual(post, 1)

    def test_all_posts(self):
        self.setup_post()
        sub_com = CommunitySubscribe(user_id=self.user.user_id, community_id=self.community.community_id)
        sub_com.save()

        with app.test_client() as c:
            response = c.post("/all_posts", content_type='application/json', data=json.dumps(
                {"user_id": self.user.user_id}
            ))
            self.assertEqual(response.status_code, 200)
            self.assertIsNotNone(response)





