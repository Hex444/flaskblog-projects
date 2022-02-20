from distutils.log import debug
from pickle import TRUE
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LOGIN_MESSAGE, LoginManager
import os
from flask_mail import Mail
from flaskblog.config import Config

app = Flask(__name__)
bcrypt = Bcrypt(app)
# db
db = SQLAlchemy(app)


# login_manager
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

app.config.from_object(Config)

mail=Mail(app)

from flaskblog.users.routes import users
from flaskblog.posts.routes import posts
from flaskblog.main.routes import main

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)