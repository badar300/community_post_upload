from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_mail import Mail
from environs import Env
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
app.config['MAIL_PASSWORD'] = 'xyz'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = True
app.config['MAIL_SUPPRESS_SEND'] = False

mail = Mail(app)
env = Env()
env.read_env()

db = SQLAlchemy(app)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], pool_size=5, pool_recycle=3600)
con = engine.connect()
from models import *

with app.app_context():
    db.create_all()


from api.signup import *
from api.login import *
from api.community import *
from api.create_post import *