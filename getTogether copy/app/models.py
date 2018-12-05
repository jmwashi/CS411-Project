from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    meet_ups = db.relationship('Meet', backref='User', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)  

class Meet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), index=True,nullable=True)
    description = db.Column(db.String(280),index=True,nullable=True)
    city = db.Column(db.String(120),index=True,nullable=True)
    events = db.relationship('Event', backref='Meet', lazy=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), index=True,nullable=True)
    address= db.Column(db.String(120), index=True,nullable=True)
    city = db.Column(db.String(120), index=True,nullable=True)
    state = db.Column(db.String(30), index=True,nullable=True)
    time = db.Column(db.String(30), index=True)
    description = db.Column(db.String(280),index = True, nullable = True)
    this_id = db.Column(db.Integer, db.ForeignKey('meet.id'),
        nullable=False)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))