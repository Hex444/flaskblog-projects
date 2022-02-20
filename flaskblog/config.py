import os

class Config:
    SECRET_KEY = '5mLwDAO8umfBU3AYpIGsV2YlF74o0airrXZfNXfgr9J2duPtZE3mo5fTgYdd'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER="smtp.gmail.com"
    MAIL_PORT=587,
    MAIL_USERR_SSL=True,
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD=os.environ.get('MAIL_PASS')

