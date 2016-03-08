from flask import (
    render_template,
    redirect,
    request,
)

from db import (
    db,
    NickRecom,
    Nickname,
)
from user import (
    get_logged_in_username,
    check_username,
)


def add_routes(app):
    # TODO : Change URL
    app.route('/<link>/manage/nicknames/')(ManageMyNicknames)
    app.route('/api/nickname/recommend/', methods=["POST"])(RecommendNickname)
    app.route('/api/nickname/delete/<idx>/', methods=["POST"])(DelMyNick)
    app.route('/api/nickname/manage/<idx>/', methods=["POST"])(ManageRecommNick)


def RecommendNickname():
    """Issue #9, A라는 사용자가 B라는 사용자에게 nick이라는 별명을 추천하는 함수입니다.
    하지만 정민교(크하하하하)가 로그인 되었는지 알려주는 함수를 만들었기 때문에!
    A라는 사용자의 아이디를 매번 URL로 요청받을 필요가 없어졌습니다.
    """
    username = get_logged_in_username()
    if request.method == "POST":
        target = request.form['target']
        nick = request.form['nick']
        """Issue #71, 별명의 길이가 0일 경우 에러페이지로 이동."""
        if not len(nick):
            return render_template(
                    "_error.html",
                    _error__msg='별명이 없습니다.',
            ), 400
        if not check_username(target, is_internal=True):
            return render_template(
                    "_error.html",
                    _error__msg='존재하지 않는 유저에게 추천하려고 하였습니다.',
            ), 400

        found = Nickname.query.filter(
            Nickname.username == target,
            Nickname.nick == nick,
        ).first()
        if found:
            return render_template(
                    "_error.html",
                    _error__msg='이미 해당유저가 사용중인 별명입니다.',
            ), 400

        new = NickRecom()
        new.nick = nick
        new.recommender = username
        new.username = target
        db.session.add(new)
        db.session.commit()
        return """
<html>
<head>
<META http-equiv="refresh" content="1;URL=/%s/">
</head>
<body>추천되었습니다!</body>
</html>
""" % (request.form['target'],)


def ManageMyNicknames(link):
    """
    Issue #7 내가 추천받은 닉네임들과 사용중인 닉네임들을 관리합니다.
    1. 내 닉네임들을 보여줌
    2. 내 닉네임들을 빼거나 추가할 수 있음.
      - 닉네임 등록 시 url db에 추가할지 물어보고, True일경우 추가해줌.
      - 이미 추천된 닉네임을 추가하려고할 경우, 추천받은 닉네임을 추가하는 것처럼 행동.
    3. 추천받은 닉네임 + 추천수를 보여줌
    4. 추천받은 닉네임을 추가할 수 있음.
      - 그러면 추천DB를 돌면서, 해당 닉네임을 추천한 것들을 다 지워야함.
      - recommender 채우기
    """
    username = get_logged_in_username()
    if not username:
        return render_template(
                "_error.html",
                _error__msg='로그인 해주세요!!',
        ), 400

    found = Nickname.query.filter(
        Nickname.username == username,
    ).all()

    found_recomm = NickRecom.query.filter(
        NickRecom.username == username,
    ).all()

    recomm = {}
    recomm['nick'] = []
    recomm['idx'] = []
    for nick in found_recomm:
        if nick.nick not in recomm['nick']:
            recomm['nick'].append(nick.nick)
            recomm['idx'].append(nick.idx)

    return render_template(
        "manager.html",
        manager__right_html_for_menu="_includes/manager/nicknames.html",
        manager__nickname__my_nickname_classes=found,
        manager__nickname__recommended_nicknames_for_me=recomm,
    )


def DelMyNick(idx):
    # Issue #7 내가 사용중인 닉네임을 삭제합니다.
    found = Nickname.query.filter(
        Nickname.idx == int(idx),
    ).first()

    username = get_logged_in_username()
    if not found.username == username:
        return render_template(
                "_error.html",
                _error__msg="fuck off",
        ), 400

    db.session.delete(found)
    db.session.commit()
    return redirect("/%s/manage/nicknames/" % (username,))


# TODO:나중에 추천받은 닉네임들이 중복되는 경우 하나만 출력하게 한 후 idx말고 nick으로 받아올 것.
def ManageRecommNick(idx):
    # Issue #7 내가 추천받은 닉네임을 관리합니다. submit==use: 사용 else: 거절
    found_recomm = NickRecom.query.filter(
        NickRecom.idx == idx,
    ).first()

    username = get_logged_in_username()
    if not found_recomm.username == username:
        return render_template(
                "_error.html",
                _error__msg="ㅗㅗ",
        ), 400

    nick = found_recomm.nick
    if request.form.get('use', None):
        found = NickRecom.query.filter(
            NickRecom.username == username,
            NickRecom.nick == nick,
        ).first()
        add_nick = Nickname()
        add_nick.username = username
        add_nick.nick = nick
        add_nick.recommender = found.recommender
        db.session.add(add_nick)

    RemoveRecommNick(nick)
    db.session.commit()
    return redirect("/%s/manage/nicknames/" % (username,))


def RemoveRecommNick(nick):
    # Issue #7 추천받은 닉네임을 DB에서 삭제합니다.
    found = NickRecom.query.filter(
        NickRecom.username == get_logged_in_username(),
        NickRecom.nick == nick,
    ).all()

    for i in found:
        idx = i.idx
        del_from_Recomm = NickRecom.query.filter(
            NickRecom.idx == idx,
        ).first()
        db.session.delete(del_from_Recomm)
    db.session.commit()


def has_new_nicknames():
    found = NickRecom.query.filter(
        NickRecom.username == get_logged_in_username(),
    ).first()
    return True if found else False
