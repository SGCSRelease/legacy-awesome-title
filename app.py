from flask import Flask

import config
from db import (
    admin,
    db,
    migrate,
    URL,
)
from nickname import add_routes as add_nickname_routes
from photo import add_routes as add_photo_routes
from user import add_routes as add_user_routes
from user import (
    bcrypt,
    check_username,
    get_logged_in_username,
)

app = Flask(__name__)

app.config.from_object(config)

admin.init_app(app)
bcrypt.init_app(app)
db.init_app(app)
migrate.init_app(app, db)

add_user_routes(app)
add_nickname_routes(app)
add_photo_routes(app)


@app.route("/")
def index():
    perhaps_logged_in_username = get_logged_in_username()
    if perhaps_logged_in_username:
        return '안녕하세요 %s님!' % (perhaps_logged_in_username,)
    return '로그인안하셨어요 /login 가 보세요'


@app.route("/<link>")
def goto(link):
    """jmg) 여러 링크를 입력해도 같은 아이디의 페이지로 이동하는 함수입니다."""
    found = URL.query.filter(
            URL.link == link,
    ).first()
    if found:
        return userpage(found.username)
    else:
        return "존재하지 않는 페이지입니다.", 404


# TODO : 페이지를 만들어야 합니다.
def userpage(id):
    return id + "의 페이지 입니다."


def addURL(link, username):
    """jmg) 아이디에 여러 링크를 연결하는 함수입니다."""
    # ID가 있는지 확인하는 함수.
    found = check_username(username, is_internal=True)
    if not found:
        return "존재하지 않는 아이디입니다.", 400

    # link 중복 check
    found = URL.query.filter(
            URL.link == link,
    ).first()
    if found:
        return "이미 생성된 링크입니다.", 400
    newP = URL()
    newP.link = link
    newP.username = username
    db.session.add(newP)
    db.session.commit()
    return "등록됐습니다."


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
