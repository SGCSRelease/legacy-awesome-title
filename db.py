# $ pip install flask-sqlalchemy
from app import app  # app.py파일의 app변수를 가져온다.

from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import MigrateCommand

manager = Manager(app)
manager.add_command('db', MigrateCommand)

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


if __name__ == '__main__':
        manager.run()
