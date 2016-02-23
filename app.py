from datetime import datetime
import os

from flask import (
        Flask,
        jsonify,
        render_template,
        request,
        send_from_directory,
        redirect,
        url_for,
)
from flask.ext.bcrypt import Bcrypt
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from werkzeug import secure_filename

app = Flask(__name__)

import config
app.config.from_object(config)
app.config['UPLOAD_FOLDER'] = './DOWNLOADED/'

from db import (
    db,
    User,
    URL,
    NickRecom,
    Photo,
)
db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(URL, db.session))
admin.add_view(ModelView(NickRecom, db.session))


@app.route("/")
def main():
    return 'main'

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form['usr']
        if not username: return 'Failed', 400
        if len(username)>50: return 'Failed', 400
        found = check_username(username, is_internal=True)
        if found: return "Existing Username", 400

        if not request.form['pwd']: return 'Failed', 400
        if request.form['pwd'] != request.form['pwda']: return 'Failed', 400
        password_hash = bcrypt.generate_password_hash(request.form['pwd'])

        first_name_kr = request.form['fnk']
        if not first_name_kr or len(first_name_kr)>50: return 'Failed', 400

        last_name_kr = request.form['lnk']
        if not last_name_kr or len(last_name_kr)>50: return 'Failed', 400

        first_name_en = request.form['fne']
        if not first_name_en or len(first_name_en)>50: return 'Failed', 400

        middle_name_en = request.form['mne']
        if len(middle_name_en)>50: return 'Failed', 400

        last_name_en = request.form['lne']
        if not last_name_en or len(last_name_en)>50: return 'Failed', 400

        try:
            student_number = int(request.form['sn'])
        except ValueError:
            return 'Failed', 400

        last_login = datetime.now()

        new_user = User()
        new_user.username = username
        new_user.password_hash = password_hash
        new_user.first_name_kr = first_name_kr
        new_user.last_name_kr = last_name_kr
        new_user.first_name_en = first_name_en
        new_user.middle_name_en = middle_name_en
        new_user.last_name_en = last_name_en
        new_user.student_number = student_number
        new_user.last_login = last_login

        db.session.add(new_user)
        db.session.commit()
        return "성공하였습니다!"

@app.route("/check_username/<username>")
def check_username(username, is_internal=False):
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

@app.route("/<link>")
def goto(link):
    """jmg) 여러 링크를 입력해도 같은 아이디의 페이지로 이동하는 함수입니다."""
    found = URL.query.filter(
            URL.link == link,
    ).first()
    if found:
        return userpage(found.username)
    else:
        return "존재하지 않는 페이지입니다.", 404

#TODO : 페이지를 만들어야 합니다.
def userpage(id):
    return id + "의 페이지 입니다."


def addURL(link, username):
    """jmg) 아이디에 여러 링크를 연결하는 함수입니다."""
    # ID가 있는지 확인하는 함수 
    found = check_username(username, is_internal=True)
    if not found:
        return "존재하지 않는 아이디입니다.", 400
    
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


@app.route('/test/nick/recom/<nick>/<fromA>/<toB>/')
def RecommendNickname(nick, fromA, toB):
    new = NickRecom()
    new.nick = nick
    new.fromA = fromA
    new.toB = toB
    db.session.add(new)
    db.session.commit()
    return '추천되었습니다!'


@app.route('/test/nick/recom/<id>')
def Search(id):
    #db 안의 toB 가 id와 일치하는 경우 모두(nick,from,toB) 출력할 것
    found = NickRecom.query.filter(
            NickRecom.toB == id,
    ).all()
    result = {}
    for i in found:	
        if i.nick in result:
            result[i.nick].append(i.fromA)
        else:
            result[i.nick] = [i.fromA]
    return jsonify(result)

@app.route('/test/upload/<username>', methods=["GET", "POST"])
def file_upload(username):
    # jmg) 파일을 업로드해 서버에 저장하는 함수입니다.
    user_found = check_username(username, is_internal=True)
    if not user_found :
        return "존재하지 않는 아이디입니다.", 400

    # 파일을 업로드
    if request.method == "GET":
        return """
        <FORM METHOD=POST ENCTYPE="multipart/form-data" ACTION="/test/upload/%s">
            File to upload: <INPUT TYPE=FILE NAME="upfile" accept="image/*"><BR> 
            <INPUT TYPE=SUBMIT VALUE="Submit"> 
        </FORM>
        """ % (username,)
    
    # 파일을 업로드 후 저장
    else :
        file = request.files['upfile']
        filename = username + os.path.splitext(file.filename)[1]

        #폴더가 없다면 만들어줍니다.
        if not os.path.exists(app.config['UPLOAD_FOLDER']) :
                os.makedirs(app.config['UPLOAD_FOLDER'])
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
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

        #Photo db에 저장이 되어있으면 db의 photo부분을 수정
        else :
            found.photo = filename
            db.session.add(found)
            db.session.commit()
        
        return redirect(url_for('uploaded_file', filename=filename))

@app.route('/uploaded_file/<filename>')
def uploaded_file(filename):
    #jmg) 업로드한 파일을 보여주는 함수입니다.
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
