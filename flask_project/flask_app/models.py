from . import db
from datetime import datetime
from flask_login import UserMixin


# Model of a user in the database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    first_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    post = db.relationship('ForumPost', backref='poster', lazy=True)
    about = db.Column(db.String(150))
    avatar = db.Column(db.String(50), default='../static/images/default.png')

    def __repr__(self):
        return (
            f"User('{self.username}', '{self.first_name}', \
            '{self.last_name}', '{self.email}', '{self.about}, {self.avatar})'"
        )


# Model of a forum in the database
class ForumPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    post = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.title}', '{self.post}', '{self.date}', \
         '{self.poster}','{self.id_user}', )"
