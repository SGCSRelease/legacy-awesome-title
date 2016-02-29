from db import (
    db,
    URL,
    User,
)
from user import check_username


def add_routes(app):
    app.route("/<link>/")(goto)


def goto(link):
    """jmg) 여러 링크를 입력해도 같은 아이디의 페이지로 이동하는 함수입니다."""
    found_at_User = User.query.filter(
        User.username == link,
    ).first()
    if found_at_User:
        return userpage(link)

    found = URL.query.filter(
        URL.link == link,
    ).first()
    if found:
        return userpage(found.username)
    else:
        return "존재하지 않는 페이지입니다.", 404


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


# TODO : 페이지를 만들어야 합니다.
def userpage(username):
    return username + "의 페이지 입니다."
