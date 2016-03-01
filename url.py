from flask import (
    render_template,
    url_for,
    request,
    redirect,
)

from db import (
    db,
    URL,
    User,
    Photo,
    Nickname,
)


def add_routes(app):
    app.route("/<link>/")(goto)
    app.route("/<link>/manage/")(gotomanage)
    app.route("/question/", methods=["POST"])(question)


def goto(link, is_manage=False):
    """jmg) 여러 링크를 입력해도 같은 아이디의 페이지로 이동하는 함수입니다."""
    found_at_User = User.query.filter(
        User.username == link,
    ).first()
    if found_at_User:
        if is_manage:
            return usermanagepage(found_at_User)
        else:
            return userpage(found_at_User)

    found = URL.query.filter(
        URL.link == link,
    ).first()
    if found:
        this_user = User.query.filter(
            User.username == found.username,
        ).first()
        if is_manage:
            return usermanagepage(this_user)
        else:
            return userpage(this_user)
    else:
        return "존재하지 않는 페이지입니다.", 404


def gotomanage(link):
    return goto(link, is_manage=True)


def addURL(link, username):
    """jmg) 아이디에 여러 링크를 연결하는 함수입니다."""
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


def userpage(user):
    my_photo = Photo.query.filter(
        Photo.username == user.username,
    ).first()
    if my_photo:
        my_photo = url_for('uploaded_photo', filename=my_photo.photo)
    else:
        my_photo = None
    my_nicknames = Nickname.query.filter(
        Nickname.username == user.username,
    ).all()
    return render_template(
            "profile.html",
            user=user,
            photo=my_photo,
            nicknames=my_nicknames,
            loggedin=get_logged_in_username(is_boolean=True),
    )


def usermanagepage(user):
    my_photo = Photo.query.filter(
        Photo.username == user.username,
    ).first()
    if my_photo:
        my_photo = url_for('uploaded_photo', filename=my_photo.photo)
    else:
        my_photo = None
    my_nicknames = Nickname.query.filter(
        Nickname.username == user.username,
    ).all()
    return render_template(
            "profile.html",
            user=user,
            photo=my_photo,
            nicknames=my_nicknames,
            loggedin=get_logged_in_username(is_boolean=True),
    )


def question():
    if 'question' in request.form:
        return redirect("/%s/" % (request.form['who'],))
    elif 'random' in request.form:
        import random
        rand = random.randrange(0, db.session.query(User).count())
        row = db.session.query(User)[rand]
        return redirect("/%s/" % (row.username,))
    return redirect("/")
