from app import db
from flask_login import UserMixin

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(24))
    username=db.Column(db.String(24))
    password=db.Column(db.String(96))
    admin=db.Column(db.Boolean)
    project_id=db.Column(db.Integer)
    # project=db.relationship('Project',backref='user',lazy='dynamic')

class Project(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(48))
    text=db.Column(db.String(1024))
    user_id=db.Column(db.Integer)
    # user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
