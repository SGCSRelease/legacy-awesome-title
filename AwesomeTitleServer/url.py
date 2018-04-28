# Third-party Library
from flask import (
    render_template,
    url_for,
    request,
    redirect,
)

# Local application
from .db import (
    db,
    Url,
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

    found = Url.query.filter(
        Url.link == link,
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
        return render_template(
                "_error.html",
                _error__msg="존재하지 않는 페이지입니다.",
        ), 404


def gotomanage(link):
    return goto(link, is_manage=True)


def addUrl(link, username):
    """jmg) 아이디에 여러 링크를 연결하는 함수입니다."""
    # link 중복 check
    found = Url.query.filter(
            Url.link == link,
    ).first()
    if found:
        return False
    newP = Url()
    newP.link = link
    newP.username = username
    db.session.add(newP)
    db.session.commit()
    return True


def get_logged_in_username(*args, **kwargs):
    """User.get_logged_in_username이랑 같아요."""
    from .user import get_logged_in_username as _get_logged_in_username
    return _get_logged_in_username(*args, **kwargs)


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
            profile__is_in_manager=False,
            profile__photo_url=my_photo,
            profile__user_class=user,
            profile__user_nickname_classes=my_nicknames,
            top_menu_nav__current_page_username=user.username,
    )


def usermanagepage(user):
    if user.username != get_logged_in_username():
        return redirect('/')

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
            "manager.html",
            manager__right_html_for_menu="_includes/profile.html",
            profile__is_in_manager=True,
            profile__photo_url=my_photo,
            profile__user_class=user,
            profile__user_nickname_classes=my_nicknames,
            top_menu_nav__current_page_username=user.username,
    )


def question():
    if 'question' in request.form:
        return redirect("/%s/" % (request.form['who'],))
    elif 'random' in request.form:
        import random
        tot = db.session.query(User).count()
        idx = random.randrange(0, tot)
        row = db.session.query(User)[idx]
        if row.username == request.form.get('current_page_username'):
            if idx is 0:
                row = db.session.query(User)[tot-1]
            else:
                row = db.session.query(User)[idx-1]
        return redirect("/%s/" % (row.username,))
    return redirect("/")
