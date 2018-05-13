# Third-party Library
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


    def to_dict(self):
        # TODO: _link element for using api contents
        return {
            'username': self.username,
            'realname': self.realname,
            'student_number': self.student_number,
            'last_login': self.last_login.isoformat() + 'Z'
        }


class Url(db.Model):
    __tablename__ = "URL"
    link = db.Column(db.String(N), primary_key=True)
    username = db.Column(db.String(N))


class Nickname(db.Model):
    __tablename__ = "nickname"
    idx = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(N))
    nick = db.Column(db.String(N))
    recommender = db.Column(db.String(N))


    def to_dict(self):
        # TODO: _link element for using api contents
        return {
            'id': self.idx,
            'username': self.username,
            'nickname': self.nick,
            'recommender': self.recommender,
        }


class NickRecom(db.Model):
    __tablename__ = "nickrecom"
    idx = db.Column(db.Integer, primary_key=True)
    nick = db.Column(db.String(N))
    recommender = db.Column(db.String(N))
    username = db.Column(db.String(N))


    def to_dict(self):
        return {
            'id': self.idx,
            'username': self.username,
            'nickname': self.nick,
            'recommender': self.recommender,
        }


class Photo(db.Model):
    __tablename__ = "photo"
    username = db.Column(db.String(N), primary_key=True)
    photo = db.Column(db.String(N + 10))


class MyModelView(ModelView):
    column_display_pk = True


admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Url, db.session))
admin.add_view(MyModelView(Nickname, db.session))
admin.add_view(MyModelView(NickRecom, db.session))
admin.add_view(MyModelView(Photo, db.session))
