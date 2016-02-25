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
    # TODO : Change URL
    app.route('/nickname/')(ManageMyNicknames)
    app.route('/test/nick/recomm/<nick>/<target>/')(RecommendNickname)
    app.route('/test/nick/recomm/')(RecommendedNicknamesForMe)


# TODO : 자신이 자신 추천하면 안되요 안되.
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


def RecommendedNicknamesForMe():
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


def ManageMyNicknames():
    """
    1. 내 닉네임들을 보여줌
    2. 내 닉네임들을 빼거나 추가할 수 있음.
      - 닉네임 등록 시 url db에 추가할지 물어보고, True일경우 추가해줌.
      - 이미 추천된 닉네임을 추가하려고할 경우, 추천받은 닉네임을 추가하는 것처럼 행동.
    3. 추천받은 닉네임 + 추천수를 보여줌
    4. 추천받은 닉네임을 추가할 수 있음.
      - 그러면 추천DB를 돌면서, 해당 닉네임을 추천한 것들을 다 지워야함.
      - recommender 채우기
    """
    return """."""
