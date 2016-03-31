from datetime import datetime
from flask import(
    redirect,
    render_template,
    request,
    jsonify,
)

from db import(
    db,
    ExternalAccount,
)
from user import get_logged_in_username


def add_routes(app):
    app.route("/<link>/manage/externals/", methods=["GET"])(show_externals)
    app.route("/api/externals/", methods=["GET", "POST"])(list_or_add_externals)  # 얘는 전체 리스트를 가지고 와 주던지 + 새로 1개를 추가하던지
    app.route("/api/externals/<idx>/", methods=["GET", "PUT", "DELETE"])(get_set_delete_externals)  # 딱 1놈을 가져와 주던지, 수정하던지, 삭제하던지.
    

def show_externals(link):
    username = get_logged_in_username()
    if link != username:
        return 'fuck off', 400

    found = ExternalAccount.query.filter(
        ExternalAccount.username == username,
    ).all()
    return render_template(
        "manager.html",
        manager__right_html_for_menu="_includes/manager/externals.html",
        manager__externals__my_externals_classes=found,
    )


def list_or_add_externals():
    username = get_logged_in_username()
    if request.method == "GET":
        found = ExternalAccount.query.filter(
                ExternalAccount.username == username,
        ).all()
        output = {}
        for i in found:
            output[i.idx] = _tojson(i)
        return jsonify(output)
    elif request.method == "POST":
        sitename = request.form['sitename']
        site_username = request.form['site_username']
        new = ExternalAccount()
        new.username = username
        new.sitename = sitename
        new.site_username = site_username
        new.registered_time = datetime.now()
        db.session.add(new)
        try:
            db.session.commit()
        except:  # TODO
            return "ㅇ?!?!?", 400
        return "잘 추가 됬습니다.", 200
    else:
        return "??", 400


def _tojson(i):
    return {
        'idx': i.idx,
        'sitename': i.sitename,
        'site_username': i.site_username,
        'registered_time': i.registered_time,
        'is_enabled': i.is_enabled,
    }


def get_set_delete_externals(idx):
    username = get_logged_in_username()
    found = ExternalAccount.query.get(idx)
    if not found:
        return "??!?", 404
    if request.method == "GET":
        return jsonify(_tojson(found))
    elif request.method == "PUT":
        found.site_username = request.form['site_username']
        found.registered_time = datetime.now()
        db.session.commit()
        return 'modified!'
    elif request.method == "DELETE":
        db.session.delete(found)
        db.session.commit()
        return 'deleted!'
    else:
        return "??", 400
