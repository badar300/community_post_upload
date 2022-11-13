from flask import make_response, jsonify, request, redirect
from sqlalchemy import text, engine

from app import app
from models import Community, CommunitySubscribe


@app.route('/add_community', methods=['POST'])
def add_community():
    community = request.get_json()
    user_id = community.get('user_id')
    community_name = community.get('community_name')
    description = community.get('description')

    community = Community(user_id=user_id, community_name=community_name, description=description)
    community.save()
    cs = CommunitySubscribe(user_id=user_id, community_id=community.community_id)
    cs.save()

    return make_response(jsonify({'msg': 'Community has been added'}), 200)


@app.route('/all_communities', methods=['GET'])
def get_all_communities():
    communities = Community.get_all_communities()
    communities_list = []
    for community in communities:
        communities_list.append({
            'community_id': community.community_id,
            'community_name': community.community_name,
            'description': community.description
        })
    return make_response(jsonify(communities_list), 200)


@app.route('/all_communities/<int:user_id>', methods=['GET'])
def get_user_communities(user_id):
    communities = Community.get_community_by_user_id(user_id)
    communities_list = []
    for community in communities:
        communities_list.append({
            'community_id': community.community_id,
            'community_name': community.community_name,
            'description': community.description
        })
    return make_response(jsonify(communities_list), 200)


@app.route('/subscribe-community', methods=['POST'])
def subscribe_community():
    comm_subs = request.get_json()
    community_id = comm_subs.get('community_id')
    user_id = comm_subs.get('user_id')
    cs = CommunitySubscribe.query.filter_by(community_id=community_id, user_id=user_id).first()
    if cs:
        return make_response(jsonify({'msg': 'Community already subscribed'}), 400)
    cs = CommunitySubscribe(community_id=community_id, user_id=user_id)
    cs.save()
    return make_response(jsonify({'msg': 'Community Added'}), 200)


@app.route('/subscribed-community', methods=['POST'])
def all_subscribed_communities():
    user = request.get_json()
    user_id = user.get('user_id')
    communities = CommunitySubscribe.get_all_subscribed_communities(user_id)
    all_comm = []
    for community in communities:
       all_comm.append({
           'community_id': community.community_id,
           'community_name': community.community_name
       })
    print(all_comm)
    return make_response(jsonify(all_comm), 200)


