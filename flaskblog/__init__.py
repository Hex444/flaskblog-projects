from distutils.log import debug
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SECRET_KEY"] = '5mLwDAO8umfBU3AYpIGsV2YlF74o0airrXZfNXfgr9J2duPtZE3mo5fTgYdd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' 

db = SQLAlchemy(app)

from flaskblog import routes