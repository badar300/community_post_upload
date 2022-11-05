from flask import make_response, jsonify, request
from sqlalchemy import text

from app import app, con
from models import CreatePost


@app.route('/create_post', methods=['POST'])
def create_post():
    post_data = request.get_json()
    user_id = post_data.get('user_id')
    community_id = post_data.get('community_id')
    post_name = post_data.get('post_name')
    description = post_data.get('description')
    post = CreatePost(user_id=user_id, community_id=community_id, post_name=post_name, description=description)
    post.save()

    return make_response(jsonify({'msg': 'post has been created'}), 200)


@app.route('/all_posts', methods=['GET'])
def get_all_posts():
    user = request.get_json()
    user_id = user.get('user_id')
    posts = all_subscribed_community_posts(user_id)
    all_posts = []
    for post in posts:
        all_posts.append({
            'post_id': post.post_id,
            'post_name': post.post_name,
            'description': post.description,
            'username': post.username,
            'community_name': post.community_name
        })
    print(all_posts)
    return make_response(jsonify(all_posts), 200)


def all_subscribed_community_posts(user_id):
    return con.execute('''
    select cp.post_id, cp.post_name, cp.description, u.username, c.community_name from create_post cp join user u
    on u.user_id = cp.user_id
    join community_subscribe cs
    on cs.community_id = cp.community_id
    join communities c on c.community_id = cp.community_id
    where cs.user_id = %s
    ''', (user_id,))
