# $ pip install flask-sqlalchemy
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
N = 50


class URL(db.Model):
    __tablename__ = "URL"
    link = db.Column(db.String(N), primary_key=True)
    ID = db.Column(db.String(N))
