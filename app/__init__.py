from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_mail import Mail
from environs import Env
from flask_cors import CORS
import pymysql
import mysql.connector

app = Flask(__name__)
CORS(app)
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
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = True
app.config['MAIL_SUPPRESS_SEND'] = False

mail = Mail(app)
env = Env()
env.read_env()

db = SQLAlchemy(app)

from models import *

with app.app_context():
    db.create_all()

mydb = mysql.connector.connect(
  host=env.str('HOST'),
  user=env.str('USER'),
  password=env.str('PASSWORD'),
  database=env.str('DATABASE')
)
mycursor = mydb.cursor()


from api.signup import *
from api.login import *
from api.community import *
from api.create_post import *
from api.comments import *