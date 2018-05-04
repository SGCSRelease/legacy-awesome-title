# Standard Library
import os
from datetime import datetime

# Third-party Library
from flask import (
    current_app,
    render_template,
    request,
    redirect,
    session,
)
from flask_bcrypt import Bcrypt

# Local Library
from .db import (
    db,
    User,
    Url,
    Photo,
    Nickname,
    NickRecom,
    N,
)
from .url import addUrl


bcrypt = Bcrypt()


def add_routes(app):
    app.route("/register/", methods=["GET", "POST"])(register)
    app.route("/check_username/<username>/")(check_username)
    app.route('/api/check_pwd/', methods=["POST"])(check_password)
    app.route('/manage/password/', methods=["GET", "POST"])(change_password)
    app.route('/<logged_in_user>/manage/withdraw/')(withdraw_manager)


def register():
    """GET /register 회원가입폼 POST /register 실제회원가입."""
    if get_logged_in_username():
        return render_template(
            "_error.html",
            _error__msg="이미 로그인되어있어요!",
        ), 400

    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form['usr']
        if not username or len(username) > N:
            return render_template(
                "_error.html",
                _error__msg="Failed - username이 맞지 않습니다.",
            ), 400
        found = check_username(username, is_internal=True)
        if found:
            return render_template(
                "_error.html",
                _error__msg="Failed - username이 겹칩니다.",
            ), 400

        if not request.form['pwd']:
            return render_template(
                "_error.html",
                _error__msg="Failed - password가 맞지 않습니다.",
            ), 400
        if request.form['pwd'] != request.form['pwda']:
            return render_template(
                "_error.html",
                _error__msg="Failed - password가 맞지 않습니다.",
            ), 400
        password_hash = bcrypt.generate_password_hash(request.form['pwd'])

        realname = request.form['realname']
        if not realname or len(realname) > N:
            return render_template(
                "_error.html",
                _error__msg="Failed - 이름이 맞지 않습니다.",
            ), 400

        if len(request.form['sn']) != 8:  # 학번제한 8자
            return render_template(
                "_error.html",
                _error__msg="Failed - 학번은 여덟 자여야 합니다.",
            ), 400

        try:
            student_number = int(request.form['sn'])
        except ValueError:
            return render_template(
                "_error.html",
                _error__msg="Failed - 학번이 맞지 않습니다.",
            ), 400

        # 2000학번~현재 년도 학번까지 제한
        thisyear = (datetime.now().year+1)*10000
        if student_number < 20000000 or student_number > thisyear:
            return render_template(
                "_error.html",
                _error__msg="Failed - 학번이 맞지 않습니다.",
            ), 400

        # 이미 가입한 학번 체크
        found = User.query.filter(
            User.student_number == student_number,
        ).first()

        if found:
            return render_template(
                "_error.html",
                _error__msg="이미 가입한 학번입니다.",
            ), 400

        new_user = User()
        new_user.username = username
        new_user.password_hash = password_hash
        new_user.realname = realname
        new_user.student_number = student_number

        # XXX: 로그인한적도없는데 last_login을 넣었으므로, 회원가입하면 자동로그인ㅋㅋ
        new_user.last_login = datetime.now()
        session['username'] = request.form['usr']
        db.session.add(new_user)
        db.session.commit()

        addUrl(realname, username)
        return redirect("/")


def check_username(username, is_internal=False):
    """/check_username/<username> 유저가 존재하는지 확인합니다."""
    found = User.query.filter(
        User.username == username,
    ).first()
    if not is_internal:
        if found:
            return "Existing Username", 400
        return "Good to go!"
    else:
        if found:
            return found
        return None


def check_password():
    username = get_logged_in_username()
    password = request.form['val']
    found = check_username(username, is_internal=True)

    if not bcrypt.check_password_hash(
            found.password_hash,
            password
    ):
        return "oops", 400
    else:
        return "yeah"


def change_password():
    if request.method == "GET":
        return render_template("change_pwd.html")
    else:
        if '/manage/password/' not in request.referrer:
            return redirect('/manage/password/')
        if not request.form['new_pwd'] == request.form['new_pwda']:
            return redirect('/manage/password/')
        password_hash = bcrypt.generate_password_hash(request.form['new_pwd'])
        username = get_logged_in_username()

        found = check_username(username, is_internal=True)
        found.password_hash = password_hash
        db.session.commit()

    return redirect('/%s/' % username)


def withdraw_manager(logged_in_user):
    """ issue #44 회원탈퇴 """

    username = get_logged_in_username()

    if logged_in_user != username:
        return '누가 당신을 싫어하나봐요 ^^', 400

    return render_template(
        "manager.html",
        manager__right_html_for_menu="_includes/manager/withdrawal.html",
        currently_logged_in_user=username,
    )
