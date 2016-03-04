from datetime import datetime

from flask import (
    render_template,
    session,
    request,
    redirect,
)
from flask.ext.bcrypt import Bcrypt

from db import (
    db,
    User,
    URL,
    Photo,
    Nickname,
    NickRecom,
    N,
)

import os

from url import addURL


bcrypt = Bcrypt()


def add_routes(app):
    app.route("/register/", methods=["GET", "POST"])(register)
    app.route("/check_username/<username>/")(check_username)
    app.route('/login/', methods=["GET", "POST"])(login)
    app.route('/logout/')(logout)
    app.route('/api/check_pwd/', methods=["POST"])(check_password)
    app.route('/manage/password/', methods=["GET", "POST"])(change_password)
    app.route('/<link>/manage/withdrawal/')(withdraw_member)


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

        addURL(realname, username)
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


def login():
    """Issue #12, 로그인 /login"""
    if request.method == "GET":
        return render_template("login.html")
    else:
        found = check_username(request.form['usr'], is_internal=True)
        if not found:
            return render_template(
                    "_error.html",
                    _error__msg="로그인 입력정보가 잘못되었습니다.",
            ), 400

        if not bcrypt.check_password_hash(
                found.password_hash,
                request.form['pwd']
        ):
            return render_template(
                    "_error.html",
                    _error__msg="로그인 입력정보가 잘못되었습니다.",
            ), 400

        username = request.form['usr']
        found.last_login = datetime.now()
        db.session.add(found)
        db.session.commit()
        session['username'] = username
        return redirect('/%s/' % username)


def logout():
    """issue #12 로그아웃"""
    session.pop('username', None)
    return redirect('/')


def get_logged_in_username():
    """issue #12 로그인 됬는지 확인하여 Username을 리턴합니다 (없으면 None).

    사실 아래를 짯습니다.
    >>> if 'username' in session:
    ...     return session['username']
    ... return None

    근데 민호형이 이렇게 바꾸었습니다.
    >>> try:
    ...     return session['username']
    ... except KeyError:
    ...     return None

    한번 더 바꾸면 아래처럼 됩니다.
    """
    return session.get('username')  # 없으면 None이 출력됨.


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


def withdraw_member(link):
    """ issue #44 회원탈퇴 """

    username = get_logged_in_username()

    found = User.query.filter(
            User.username == username,
    ).first()
    
    db.session.delete(found)
    
    while True:
        found = URL.query.filter(
               URL.username == username,
        ).first()

        if found:
            db.session.delete(found)
        else:
            break;
   
    found = Photo.query.filter(
            Photo.username == username,
    ).first()

    filename = found.photo

    if found:
        db.session.delete(found)
    
    os.remove("./DOWNLOADED/%s" % filename)

    while True:
        found = NickRecom.query.filter(
                NickRecom.username == username,
        ).first()

        if found:
            db.session.delete(found)
        else:
            break;

    while True:
        found = Nickname.query.filter(
                Nickname.username == username,
        ).first()

        if found:
            db.session.delete(found)
        else:
            break;

    db.session.commit()

    session.pop('username', None)
    return redirect('/')
