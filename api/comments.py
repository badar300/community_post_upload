
from flask import request, make_response, jsonify
from models import Comment


@app.route('/subscribe-community', methods=['POST'])
def subscribe_community():
    comm = request.get_json()
    post_id = comm.get('post_id')
    user_id = comm.get('user_id')
    comment = comm.get('comment')
    cs = Comment(post_id=post_id, user_id=user_id, comment=comment)
    cs.save()
    return make_response(jsonify({'msg': 'Community Added'}), 200)
