from datetime import datetime

from api import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    email = db.Column(db.String(64), unique=True)
    nickname = db.Column(db.String(32), unique=True)
    description = db.Column(db.Text)
    haikus = db.relationship('Haiku', backref='user', lazy='dynamic')

    # oauth stuff
    PROVIDER_GMAIL = 1
    PROVIDER_FACEBOOK = 2
    oauth_provider = db.Column(db.Integer)
    access_token = db.Column(db.Text)

class Haiku(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    first_line = db.Column(db.Text) 
    second_line = db.Column(db.Text) 
    third_line = db.Column(db.Text) 
