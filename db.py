# $ pip install flask-sqlalchemy
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
N = 50


class User(db.Model):
    username = db.Column(db.String(N), primary_key=True)
    password_hash = db.Column(db.String(N + 10), nullable=False)
    first_name_kr = db.Column(db.String(N), nullable=False)
    last_name_kr = db.Column(db.String(N), nullable=False)
    first_name_en = db.Column(db.String(N), nullable=False)
    middle_name_en = db.Column(db.String(N))
    last_name_en = db.Column(db.String(N), nullable=False)
    student_number = db.Column(db.Integer, nullable=False)
    last_login = db.Column(db.DateTime, nullable=False)

    """
    def __init__(self, username, password_hash, first_name_kr, last_name_kr, first_name_en, middle_name_en, last_name_en, student_number, last_login):
        self.username = username
        self.password_hash = password_hash
        self.first_name_kr = first_name_kr
        self.last_name_kr = last_name_kr
        self.first_name_en = first_name_en
        self.middle_name_en = middle_name_en
        self.last_name_en = last_name_en
        self.student_number = student_number
        self.last_login = last_login
    """

    def __repr__(self):
        return '<User %r>' % self.username


class URL(db.Model):
    __tablename__ = "URL"
    link = db.Column(db.String(N), primary_key=True)
    username = db.Column(db.String(N))


class NickRecom(db.Model):
    __tablename__ = "nickrecom"
    idx = db.Column(db.Integer, primary_key=True)
    nick = db.Column(db.String(N))
    fromA = db.Column(db.String(N))
    toB = db.Column(db.String(N))


class Photo(db.Model):
    __tablename__ = "photo"
    username = db.Column(db.String(N), primary_key=True)
    photo = db.Column(db.String(N + 10))
