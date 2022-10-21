from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import pymysql

app = Flask(__name__)

app.secret_key = 'abc123'
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:badar@localhost:3306/user_post'

pymysql.install_as_MySQLdb()

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'abc'
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = True
app.config['MAIL_SUPPRESS_SEND'] = False

mail = Mail(app)


db = SQLAlchemy(app)
from models import *

with app.app_context():
    db.create_all()


from api.signup import *
