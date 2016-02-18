# $ pip install flask
from flask import Flask, request
# $ pip install flask-sqlalchemy
from flask_sqlalchemy import SQLAlchemy
# $ pip install flask-admin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
admin = Admin(app)  # <-- Admin page Setting!

# 선언
class Person(db.Model):
    """
    $ rm test.db
    $ python 
    >>> from app import db
    >>> db.create_all()
    >>> exit()
    """
    __tablename__ = "person"
    #id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(10), primary_key=True)
    pwd = db.Column(db.String(10))
    name = db.Column(db.String(10))
    hakbun = db.Column(db.Integer)

admin.add_view(ModelView(Person, db.session))
# /admin


@app.route("/new/<user>/<pwd>/<name>/<hakbun>")
def Register(user, pwd, name, hakbun):
    # DB에 추가할 것을 만든다.
    new = Person()
    new.user = user
    new.pwd = pwd
    new.name = name
    new.hakbun = hakbun
    # DB에 추가한다!
    db.session.add(new)
    db.session.commit()
    # 사용자에게 보여준다!
    return '회원가입되셨습니다!'

@app.route("/login/<user>/<pwd>")
def LogIn(user, pwd):
    found = Person.query.filter(
            Person.user == user,
            Person.pwd == pwd
    )
    print(str(found))
    found = found.first()
    
    if found:
        return '안녕하세요 %s님(%s)' % (found.name, found.hakbun)
    else:
        return '누구세요?!'

@app.route("/search/<user>/<hakbun>")
def SearchPW(user,hakbun):
    found = Person.query.filter(
            Person.user == user,
            Person.hakbun == hakbun
    ).first()
    if found:
        return '%s님(%s)의 PW는 %s입니다.' % (found.user, found.hakbun, found.pwd)
    else:
        return '누구세요?!'

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
