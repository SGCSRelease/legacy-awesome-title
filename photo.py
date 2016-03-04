import os

from flask import (
    current_app,
    request,
    redirect,
    send_from_directory,
    render_template,
)

from db import (
    db,
    Photo,
)
from user import get_logged_in_username


def add_routes(app):
    app.route('/<link>/manage/photo/', methods=["GET", "POST"])(photo_upload)
    app.route('/uploaded_photo/<filename>/')(uploaded_photo)
    app.route('/delete_photo/', methods=["POST"])(delete_photo)

def photo_upload(link):
    """Issue #11, jmg) 사진을 업로드해 서버에 저장하는 함수입니다.
    /upload GET/POST
    """
    username = get_logged_in_username()
    if not username:
        return render_template(
                "_error.html",
                _error__msg="로그인이 되어있지 않습니다.",
        ), 400
    if not link == username:
        return render_template(
                "_error.html",
                _error__msg="자신이 아닙니다!",
        ), 400

    # 파일을 업로드
    if request.method == "GET":
        return render_template(
                "manager.html",
                manager__right_html_for_menu="_includes/manager/photo.html",
        )

    # 파일을 업로드 후 저장
    else:
        file = request.files['upfile']
        if not file:
            return render_template(
                    "_error.html",
                    _error__msg="이미지를 업로드하지 않았습니다.",
            ), 400
        filename = username + os.path.splitext(file.filename)[1]

        # 폴더가 없다면 만들어줍니다.
        if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
            os.makedirs(current_app.config['UPLOAD_FOLDER'])
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        found = Photo.query.filter(
                Photo.username == username,
        ).first()

        # Photo db에 저장이 되어있지 않으면 db에 추가
        if not found:
            new_photo = Photo()
            new_photo.username = username
            new_photo.photo = filename

            db.session.add(new_photo)
            db.session.commit()

        # Photo db에 저장이 되어있으면 db의 photo부분을 수정
        else:
            found.photo = filename
            db.session.add(found)
            db.session.commit()

        return redirect("/%s/manage/" % (username, ))

def delete_photo():
    username = get_logged_in_username()
    if not username:
        return render_template(
                "_error.html",
                _error__msg="당신 계정으로 들어가시죠?",
                ), 400

    found = Photo.query.filter(
        Photo.username == username,
    ).first()

    if not found:
         return render_template(
                "_error.html",
                _error__msg="삭제할 사진이 없어요!",
                ), 400

    filename = found.photo

    db.session.delete(found)
    db.session.commit()
    os.remove(
        os.path.join(
            current_app.config['UPLOAD_FOLDER'],
            filename,
        )
    )
    return redirect("/%s/manage/" % (username, ))


# TODO(정민교): 로그인 안하고도 볼 수 있는데 이게 맞나요?
def uploaded_photo(filename):
    """Issue #11, jmg) 업로드한 사진을 보여주는 함수입니다.
    /uploaded_photo/<filename>
    """
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
