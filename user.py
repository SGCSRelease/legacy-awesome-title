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
    N,
)


bcrypt = Bcrypt()


def add_routes(app):
    app.route("/register/", methods=["GET", "POST"])(register)
    app.route("/check_username/<username>/")(check_username)
    app.route('/login/', methods=["GET", "POST"])(login)
    app.route('/logout/')(logout)


def register():
    """GET /register 회원가입폼 POST /register 실제회원가입."""
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form['usr']
        if not username or len(username) > N:
            return 'Failed', 400
        found = check_username(username, is_internal=True)
        if found:
            return "Existing Username", 400

        if not request.form['pwd']:
            return 'Failed', 400
        if request.form['pwd'] != request.form['pwda']:
            return 'Failed', 400
        password_hash = bcrypt.generate_password_hash(request.form['pwd'])

        first_name_kr = request.form['fnk']
        if not first_name_kr or len(first_name_kr) > N:
            return 'Failed', 400

        last_name_kr = request.form['lnk']
        if not last_name_kr or len(last_name_kr) > N:
            return 'Failed', 400

        first_name_en = request.form['fne']
        if not first_name_en or len(first_name_en) > N:
            return 'Failed', 400

        middle_name_en = request.form['mne']
        if len(middle_name_en) > N:
            return 'Failed', 400

        last_name_en = request.form['lne']
        if not last_name_en or len(last_name_en) > N:
            return 'Failed', 400

        try:
            student_number = int(request.form['sn'])
        except ValueError:
            return 'Failed', 400

        new_user = User()
        new_user.username = username
        new_user.password_hash = password_hash
        new_user.first_name_kr = first_name_kr
        new_user.last_name_kr = last_name_kr
        new_user.first_name_en = first_name_en
        new_user.middle_name_en = middle_name_en
        new_user.last_name_en = last_name_en
        new_user.student_number = student_number

        # XXX: 로그인한적도없는데 last_login을 넣었으므로, 회원가입하면 자동로그인ㅋㅋ
        new_user.last_login = datetime.now()
        session['username'] = request.form['usr']
        db.session.add(new_user)
        db.session.commit()

        return """
        <html>
        <head>
        <meta http-equiv="refresh" content="3; url=/"></meta>
        </head>
        <body>
        성공하였습니다! 3초 후에 메인화면으로 갑니다!
        </body>
        </html>
        """


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
        if get_logged_in_username():
            return """
                <html>
                    <head>
                        <meta http-equiv="refresh" content="2; url=/"></meta>
                    </head>
                    <body>
                        이미 로그인이 되어있습니다!!
                    </body>
                </html>
            """

        return """
            <form method=POST action="/login/">
                ID: <input type=text class='usr' id=usr name=usr /> <br>
                PW: <input type=password class='pwd' id=pwd name=pwd /> <br>
                <input type=submit />
            </form>
            """
    else:
        found = check_username(request.form['usr'], is_internal=True)
        if not found:
            return "로그인 입력정보가 잘못되었습니다.", 400

        if not bcrypt.check_password_hash(
                found.password_hash,
                request.form['pwd']
        ):
            return "로그인 입력정보가 잘못되었습니다.", 400

        found.last_login = datetime.now()
        db.session.add(found)
        db.session.commit()
        session['username'] = request.form['usr']
        return redirect('/')


def logout():
    """issue #12 로그아웃"""
    session.pop('username', None)
    return """
        <html>
            <head>
                <meta http-equiv="refresh" content="2; url=/"></meta>
            </head>
            <body>
                로그아웃 합니다! 2초 후 메인페이지로 이동합니다.
            </body>
        </html>
        """
    # return redirect('/')


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
