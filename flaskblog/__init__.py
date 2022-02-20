from distutils.log import debug
from pickle import TRUE
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LOGIN_MESSAGE, LoginManager
import os
from flask_mail import Mail

app = Flask(__name__)
app.config["SECRET_KEY"] = '5mLwDAO8umfBU3AYpIGsV2YlF74o0airrXZfNXfgr9J2duPtZE3mo5fTgYdd'
bcrypt = Bcrypt(app)
# db
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' 

# login_manager
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

# email
app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=587,
    MAIL_USERR_SSL=True,
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
    MAIL_PASSWORD=os.environ.get('MAIL_PASS')
)
app.config['MAIL_USE_TLS'] = True
mail=Mail(app)

from flaskblog.users.routes import users
from flaskblog.posts.routes import posts
from flaskblog.main.routes import main

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)