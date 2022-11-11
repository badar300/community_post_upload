
from flask import request, make_response, jsonify
from app import app, mycursor
from models import Comment


@app.route('/new_comment', methods=['POST'])
def new_comment():
    comm = request.get_json()
    post_id = comm.get('post_id')
    user_id = comm.get('user_id')
    comment = comm.get('comment')
    cs = Comment(post_id=post_id, user_id=user_id, comment=comment)
    cs.save()
    return make_response(jsonify({'msg': 'Comment Added'}), 200)


@app.route('/all_comments', methods=['POST'])
def get_all_comments():
    post = request.get_json()
    post_id = post.get('post_id')
    mycursor.execute('''
        select u.username, c.comment, c.create_dttm from comments c join user u
        on u.user_id = c.user_id
        where c.post_id = %s
        ''', (post_id,))
    comments = mycursor.fetchall()
    all_comments = []
    for comment in comments:
        all_comments.append({
            'username': comment[0],
            'comment': comment[1],
            'comment_time': comment[2]
        })
    return make_response(jsonify(all_comments), 200)


