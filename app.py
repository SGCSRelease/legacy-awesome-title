from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate

app = Flask(__name__)

import config
app.config.from_object(config)

from db import (
    db,
    URL,
)
db.init_app(app)
migrate = Migrate(app, db)

admin = Admin(app)
admin.add_view(ModelView(URL, db.session))


@app.route("/")
def main():
    return 'main'


@app.route("/newbie")
def register():
    return '회원가입이 들어갈 자리입니다!'


@app.route("/<link>")
def goto(link):
    """jmg) 여러 링크를 입력해도 같은 아이디의 페이지로 이동하는 함수입니다."""
    found = URL.query.filter(
        URL.link == link,
    ).first()
    if found:
        return found.ID + "의 페이지 입니다."
    else:
        return "존재하지 않는 페이지입니다.", 404


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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
