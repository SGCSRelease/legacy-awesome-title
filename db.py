# $ pip install flask-sqlalchemy
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Test(db.Model):
    __tablename__ = "test"
    idx = db.Column(db.Integer, primary_key=True)
