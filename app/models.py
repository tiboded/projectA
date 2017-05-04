from app import db
from flask_login import UserMixin

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String)
    username=db.Column(db.String)
    password=db.Column(db.String)
    admin=db.Column(db.Boolean)
    project_id=db.Column(db.Integer)
    # project=db.relationship('Project',backref='user',lazy='dynamic')

class Project(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String)
    text=db.Column(db.String)
    user_id=db.Column(db.Integer)
    # user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
