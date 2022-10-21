from flask import request, session, make_response, jsonify
from flask_mail import Message
import random

from app import app, mail
from models import Signup


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signup = request.get_json()
    name = signup.get('username')
    email = signup.get('email')
    password = signup.get('password')

    if Signup.query.filter_by(email=email).all():
        return make_response(jsonify({'error': 'User already exist'}), 400)

    user = Signup(username=name, email=email, password=password)
    status = email_authentication_code(email, user)
    if status == 'Sent':
        return make_response(jsonify({'msg': 'Code has been send'}), 400)


@app.route('/verify_code', methods=['GET', 'POST'])
def signup_full():
    signup = request.get_json()
    code = signup.get('code')
    if code == str(session['code']):
        user = Signup(username=name, email=email, password=password)
        user.save()


def email_authentication_code(email, user):
    msg = Message('Email Authentication', sender=app.config['MAIL_USERNAME'], recipients=[email])
    code = random.randint(100000, 999999)
    user.code = code
    user.save()
    msg.body = f"Code for email authentication is {code}"
    mail.send(msg)
    return "Sent"
