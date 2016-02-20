from datetime import datetime

from flask import Flask, jsonify, render_template, request
from flask.ext.bcrypt import Bcrypt
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate

app = Flask(__name__)

import config
app.config.from_object(config)

from db import (
    db,
    User,
    URL,
    NickRecom,
)
db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(URL, db.session))
admin.add_view(ModelView(NickRecom, db.session))


@app.route("/")
def main():
    return 'main'


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form['usr']
        if not username: return 'Failed', 400
        if len(username)>50: return 'Failed', 400
        found = User.query.filter(
                User.username == username,
                ).first()
        if found: return "Existing Username", 400

        if not request.form['pwd']: return 'Failed', 400
        if request.form['pwd'] != request.form['pwda']: return 'Failed', 400
        password_hash = bcrypt.generate_password_hash(request.form['pwd'])

        first_name_kr = request.form['fnk']
        if not first_name_kr or len(first_name_kr)>50: return 'Failed', 400

        last_name_kr = request.form['lnk']
        if not last_name_kr or len(last_name_kr)>50: return 'Failed', 400

        first_name_en = request.form['fne']
        if not first_name_en or len(first_name_en)>50: return 'Failed', 400

        middle_name_en = request.form['mne']
        if len(middle_name_en)>50: return 'Failed', 400

        last_name_en = request.form['lne']
        if not last_name_en or len(last_name_en)>50: return 'Failed', 400

        try:
            student_number = int(request.form['sn'])
        except ValueError:
            return 'Failed', 400

        last_login = datetime.now()

        new_user = User()
        new_user.username = username
        new_user.password_hash = password_hash
        new_user.first_name_kr = first_name_kr
        new_user.last_name_kr = last_name_kr
        new_user.first_name_en = first_name_en
        new_user.middle_name_en = middle_name_en
        new_user.last_name_en = last_name_en
        new_user.student_number = student_number
        new_user.last_login = last_login

        db.session.add(new_user)
        db.session.commit()
        return "성공하였습니다!"

@app.route("/check_username/<username>")
def check_username(username):
    found = User.query.filter(
            User.username == username,
    ).first()
    if found:
        return "Existing Username", 400
    return "Good to go!"

@app.route("/<link>")
def goto(link):
    """jmg) 여러 링크를 입력해도 같은 아이디의 페이지로 이동하는 함수입니다."""
    found = URL.query.filter(
            URL.link == link,
    ).first()
    if found:
        return userpage(found.ID)
    else:
        return "존재하지 않는 페이지입니다.", 404


def userpage(id):
    return id + "의 페이지 입니다."


# TODO : 테스트 용이 아니라 다른 친구들이 사용할 수 있도록 함수로 만들어주세요. 그러니까 나중에는 URL을 빼주세요!
@app.route("/test/add_URL/<link>/<id>")
def addURL(link, id):
    """jmg) 아이디에 여러 링크를 연결하는 함수입니다."""
    # TODO : 광희랑 이야기해서 ID가 있는지 확인하는 함수를 호출해 주세요. 
    # link 중복 check
    found = URL.query.filter(
            URL.link == link,
    ).first()
    if found:
        return "이미 생성된 링크입니다.", 400
    newP = URL()
    newP.link = link
    newP.ID = id
    db.session.add(newP)
    db.session.commit()
    return "등록됐습니다."


@app.route('/test/nick/recom/<nick>/<fromA>/<toB>/')
def RecommendNickname(nick, fromA, toB):
    new = NickRecom()
    new.nick = nick
    new.fromA = fromA
    new.toB = toB
    db.session.add(new)
    db.session.commit()
    return '추천되었습니다!'


@app.route('/test/nick/recom/<id>')
def Search(id):
    #db 안의 toB 가 id와 일치하는 경우 모두(nick,from,toB) 출력할 것
    found = NickRecom.query.filter(
            NickRecom.toB == id,
    ).all()
    result = {}
    for i in found:	
        if i.nick in result:
            result[i.nick].append(i.fromA)
        else:
            result[i.nick] = [i.fromA]
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
