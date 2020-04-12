import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_restful import Resource, Api, reqparse


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
bcrypt = Bcrypt(app)
db = SQLAlchemy()
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
db.init_app(app)


from . import routes
