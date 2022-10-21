from flask import request, make_response, jsonify
from flask_mail import Message
import random

from app import app, mail
from models import User


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_user = request.get_json()
    name = signup_user.get('username')
    email = signup_user.get('email')
    password = signup_user.get('password')

    if User.query.filter_by(email=email).all():
        return make_response(jsonify({'error': 'User already exist'}), 400)

    user = User(username=name, email=email, password=password)
    status = email_authentication_code(email, user)
    if status == 'Sent':
        return make_response(jsonify({'msg': 'Code has been send'}), 400)


@app.route('/verify_code', methods=['GET', 'POST'])
def signup_full():
    verify_mail = request.get_json()
    code = verify_mail.get('code')
    email = verify_mail.get('email')
    user = User.query.filter_by(email=email).first()
    if user:
        if code == user.code:
            user.is_authenticated = True
            user.save()
            return make_response(jsonify({'msg': 'Auth Success'}), 200)
        return make_response(jsonify({'msg': 'Please enter correct code'}), 401)
    return make_response(jsonify({'msg': 'No such user exist with this email'}), 200)


def email_authentication_code(email, user):
    msg = Message('Email Authentication', sender=app.config['MAIL_USERNAME'], recipients=[email])
    code = random.randint(100000, 999999)
    user.code = code
    user.save()
    msg.body = f"Code for email authentication is {code}"
    mail.send(msg)
    return "Sent"
