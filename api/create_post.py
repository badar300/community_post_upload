from flask import make_response, jsonify, request

from app import app
from models import Community


@app.route('/create_post', methods=['POST'])
def create_post():
    post_data = request.get_json()
    user_id = post_data.get('user_id')
    community_id = post_data.get('community_id')
    community_name = post_data.get('community_name')
    description = post_data.get('description')

    community = Community(user_id=user_id, community_name=community_name, description=description)
    community.save()

    return make_response(jsonify({'msg': 'Community has been added'}), 200)


@app.route('/all_communities/<int:user_id>', methods=['GET'])
def get_user_posts(user_id):
    communities = Community.get_community_by_user_id(user_id)
    communities_list = []
    for community in communities:
        communities_list.append({
            'community_name': community.community_name,
            'description': community.description
        })
    return make_response(jsonify(communities_list), 200)