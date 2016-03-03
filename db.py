from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


admin = Admin()
db = SQLAlchemy()
migrate = Migrate()
N = 50


class User(db.Model):
    __tablename__ = "user"
    username = db.Column(db.String(N), primary_key=True)
    password_hash = db.Column(db.String(N + 10), nullable=False)
    realname = db.Column(db.String(N), nullable=False)
    student_number = db.Column(db.Integer, nullable=False)
    last_login = db.Column(db.DateTime, nullable=False)


class URL(db.Model):
    __tablename__ = "URL"
    link = db.Column(db.String(N), primary_key=True)
    username = db.Column(db.String(N))


class Nickname(db.Model):
    __tablename__ = "nickname"
    idx = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(N))
    nick = db.Column(db.String(N))
    recommender = db.Column(db.String(N))


class NickRecom(db.Model):
    __tablename__ = "nickrecom"
    idx = db.Column(db.Integer, primary_key=True)
    nick = db.Column(db.String(N))
    recommender = db.Column(db.String(N))
    username = db.Column(db.String(N))


class Photo(db.Model):
    __tablename__ = "photo"
    username = db.Column(db.String(N), primary_key=True)
    photo = db.Column(db.String(N + 10))


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(URL, db.session))
admin.add_view(ModelView(NickRecom, db.session))
admin.add_view(ModelView(Photo, db.session))
