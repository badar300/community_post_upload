from flask import make_response, jsonify, request
from sqlalchemy import text

from app import app, mycursor, mydb, db
from models import CreatePost, LikePost, SavePost, CommunitySubscribe


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


@app.route('/all_posts', methods=['POST'])
def get_all_posts():
    user = request.get_json()
    user_id = user.get('user_id')
    posts = all_subscribed_community_posts(user_id)
    all_posts = []
    for post in posts:
        likes = LikePost.query.filter(LikePost.post_id == post[0]).count()
        is_subscribed = CommunitySubscribe.query.filter_by(community_id=post[6], user_id=user_id).first()
        if is_subscribed:
            all_posts.append({
                'post_id': post[0],
                'post_name': post[1],
                'description': post[2],
                'username': post[3],
                'community_name': post[4],
                "total_likes": likes,
                "posted_time": post[5]
            })
    print(all_posts)
    return make_response(jsonify(all_posts), 200)


def all_subscribed_community_posts(user_id):
    mycursor.execute('''
    select cp.post_id, cp.post_name, cp.description, u.username, c.community_name, cp.create_dttm, c.community_id from create_post cp
    join user u on u.user_id = cp.user_id
    join communities c on c.community_id = cp.community_id
    order by cp.create_dttm desc
    -- where cp.user_id = %s
    ''')
    # ''', (user_id,))
    data = mycursor.fetchall()
    mydb.commit()
    return data


@app.route('/like_post', methods=['POST'])
def like_post():
    comm_subs = request.get_json()
    post_id = comm_subs.get('post_id')
    user_id = comm_subs.get('user_id')
    lk = LikePost.query.filter_by(post_id=post_id, user_id=user_id).first()
    if lk:
        return make_response(jsonify({'msg': 'Post already liked'}), 400)
    cs = LikePost(post_id=post_id, user_id=user_id)
    cs.save()
    lk = LikePost.query.filter_by(post_id=post_id).count()
    return make_response(jsonify({'msg': 'You liked this post', 'total_likes': lk}), 200)


@app.route('/dislike', methods=['POST'])
def dislike():
    comm_subs = request.get_json()
    post_id = comm_subs.get('post_id')
    user_id = comm_subs.get('user_id')
    lk = LikePost.query.filter_by(post_id=post_id, user_id=user_id).delete()
    db.session.commit()
    # if lk:
    #     return make_response(jsonify({'msg': 'Post already liked'}), 400)
    # cs = LikePost(post_id=post_id, user_id=user_id)
    # cs.save()
    lk = LikePost.query.filter_by(post_id=post_id).count()
    return make_response(jsonify({'msg': 'You dislike this post', 'total_likes': lk}), 200)


@app.route('/save_post', methods=['POST'])
def save_post():
    save = request.get_json()
    post_id = save.get('post_id')
    user_id = save.get('user_id')
    sp = SavePost.query.filter_by(post_id=post_id, user_id=user_id).first()
    if sp:
        return make_response(jsonify({'msg': 'Post already in saved list'}), 400)
    cs = SavePost(post_id=post_id, user_id=user_id)
    cs.save()
    return make_response(jsonify({'msg': 'You saved this post'}), 200)


@app.route('/all_saved_posts', methods=['POST'])
def get_all_saved_posts():
    user = request.get_json()
    user_id = user.get('user_id')
    posts = all_saved_posts(user_id)
    all_posts = []
    for post in posts:
        likes = LikePost.query.filter(LikePost.post_id == post[0]).count()
        all_posts.append({
            'post_id': post[0],
            'post_name': post[1],
            'description': post[2],
            'username': post[3],
            'community_name': post[4],
            "total_likes": likes,
            "posted_time": post[5]
        })
    print(all_posts)
    return make_response(jsonify(all_posts), 200)


def all_saved_posts(user_id):
    mycursor.execute('''
    select cp.post_id, cp.post_name, cp.description, u.username, c.community_name, cp.create_dttm from create_post cp join user u
    on u.user_id = cp.user_id
    join community_subscribe cs
    on cs.community_id = cp.community_id
    join communities c on c.community_id = cp.community_id
    join save_post sp on sp.post_id = cp.post_id
    where sp.user_id = %s
    ''', (user_id,))
    data = mycursor.fetchall()
    mydb.commit()
    return data
