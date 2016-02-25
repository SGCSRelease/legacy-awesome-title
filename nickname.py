# RecommendNickname
# Search????

from flask import (
    jsonify,
)

from db import (
    db,
    NickRecom,
)
from user import (
    get_logged_in_username,
    check_username,
)


def add_routes(app):
    app.route('/test/nick/recomm/<nick>/<target>/')(RecommendNickname)
    app.route('/test/nick/recomm')(Search)


# @app.route('/test/nick/recom/<nick>/<fromA>/<toB>/')
# def RecommendNickname(nick, fromA, toB):
# TODO : Change URL and Name of Function!  -- NEED TO MAKE AN ISSUE!
def RecommendNickname(nick, target):
    """Issue #9, A라는 사용자가 B라는 사용자에게 nick이라는 별명을 추천하는 함수입니다.
    하지만 정민교(크하하하하)가 로그인 되었는지 알려주는 함수를 만들었기 때문에!
    A라는 사용자의 아이디를 매번 URL로 요청받을 필요가 없어졌습니다.
    """
    username = get_logged_in_username()
    if not username:
        return '로그인이 안되어 있습니다!!!!', 400
    if not check_username(username, is_internal=True):
        return '존재하지 않는 유저에게 추천하려고 하였습니다.', 400
    new = NickRecom()
    new.nick = nick
    new.recommender = username
    new.username = target
    db.session.add(new)
    db.session.commit()
    return '추천되었습니다!'


# TODO : Change URL and Name of Function!  -- NEED TO MAKE AN ISSUE!
def Search():
    """Issue #9, 내가 추천받은 닉네임들을 보여줍니다."""
    username = get_logged_in_username()
    if not username:
        return '로그인이 안되어 있다구욧!!!!', 400

    # db 안의 toB 가 id와 일치하는 경우 모두(nick,from,toB) 출력할 것
    found = NickRecom.query.filter(
            NickRecom.username == username,
    ).all()

    result = {}
    for i in found:
        if i.nick in result:
            result[i.nick].append(i.recommender)
        else:
            result[i.nick] = [i.recommender]
    return jsonify(result)
