# $ pip install flask-sqlalchemy
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
N = 50


class URL(db.Model):
    __tablename__ = "URL"
    link = db.Column(db.String(N), primary_key=True)
    ID = db.Column(db.String(N))

class NickRecom(db.Model):
    __tablename__ = "nickrecom"
    idx = db.Column(db.Integer, primary_key=True)
    nick = db.Column(db.String(N))
    fromA = db.Column(db.String(N))
    toB = db.Column(db.String(N))
