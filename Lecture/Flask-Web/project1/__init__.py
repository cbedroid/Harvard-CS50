import os
import jinja2
from flask import Flask,session,request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_restful import Resource, Api, reqparse
from urllib.parse import unquote
from datetime import timedelta

# import database uri  credential from file 
try: 
    from .myuri import DATABASE_URL
except:
    DATABASE_URL = None

#read database uri from file. Fallback on environment variable on error. 

database = DATABASE_URL or os.environ.get("DATABASE_URL")
if not database:  raise RuntimeError("DATABASE_URL is not set")

# Add  Flask database: using heroku database 
app = Flask(__name__,template_folder='templates',static_url_path='')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["SQLALCHEMY_DATABASE_URI"] =  database

#secrets.token_hex(32) 32 bytes: increase bytes value for better encryption
app.config['SECRET_KEY'] = '9744fea133cd127d1d0b67f3d7e54be7dfe039e7d9f42935832e17be46102d00c0c9c30260a0745d09b360b32c1b43006d64f408a66e3c6c57631110576be7e3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['JSON_SORT_KEYS'] = False
env = jinja2.Environment()

env.globals.update(zip=zip)
app.jinja_env.globals.update(zip=zip)

env.filters['unquote'] = lambda url: unquote(url)
app.jinja_env.filters['unquote'] = lambda url: unquote(url)



@app.before_request
def session_inactivity_timeout(duration=15):
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=duration)

bcrypt = Bcrypt(app)
db = SQLAlchemy()
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

db.init_app(app)

from .routes import user_routes, main_routes

