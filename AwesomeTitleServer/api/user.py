# Standard Library
import os

# Third-party Library
from flask import (
    redirect,
    jsonify,
    current_app,
    session,
)

# local applications
from . import bp
from AwesomeTitleServer.db import (
    N,
    db,
    User,
    Url,
    Photo,
    Nickname,
    NickRecom,
)



@bp.route('/user/<username>', methods=['GET'])
def get_user(username):
    return jsonify(User.query.get_or_404(username).to_dict())


@bp.route('/user/<username>', methods=['POST'])
def create_user(username):
    '''
    Form

    'pwd': 'password'
    'pwda': 'password repeat'
    'realname' 'real name'
    'sn': 'school number'
    '''

    # TODO: 에러에 더 추가할 것은 없나?
    error = {
        'error_msg': '',
    }

    # 유저 정보 유효성 체크
    if not username or len(username) > N:
        error['error_msg'] = 'username이 맞지 않습니다.'
        response = jsonify(error)
        response.status_code = 400
        return response

    found = check_username(username, is_internal=true)
    if found:
        error['error_msg'] = 'username이 겹칩니다.'
        response = jsonify(error)
        response.status_code = 400
        return response

    if not request.form['pwd'] or request.form['pwd'] != request.form['pwda']:
        error['error_msg'] = 'password가 맞지 않습니다.'
        response = jsonify(error)
        response.status_code = 400
        return response
    password_hash = bcrypt.generate_password_hash(request.form['pwd'])

    realname = request.form['realname']
    if not realname or len(realname) > n:
        error['error_msg'] = '이름이 맞지 않습니다.'
        response = jsonify(error)
        response.status_code = 400
        return response

    if len(request.form['sn']) != 8:  # 학번제한 8자
        error['error_msg'] = '학번은 여덟 자여야 합니다.'
        response = jsonify(error)
        response.status_code = 400
        return response

    try:
        student_number = int(request.form['sn'])
    except valueerror:
        error['error_msg'] = '학번이 맞지 않습니다.'
        response = jsonify(error)
        response.status_code = 400
        return response

    # 2000학번~현재 년도 학번까지 제한
    next_year = (datetime.now().year+1)*10000
    if student_number < 20000000 or student_number > next_year:
        error['error_msg'] = '학번이 맞지 않습니다.'
        response = jsonify(error)
        response.status_code = 400
        return response

    # 이미 가입한 학번 체크
    found = user.query.filter(
        user.student_number == student_number,
    ).first()

    if found:
        error['error_msg'] = '이미 가입한 학번입니다.'
        response = jsonify(error)
        response.status_code = 400
        return response

    # 유저 생성
    new_user = User()
    new_user.username = username
    new_user.password_hash = password_hash
    new_user.realname = realname
    new_user.student_number = student_number

    # xxx: 로그인한적도없는데 last_login을 넣었으므로, 회원가입하면 자동로그인ㅋㅋ
    new_user.last_login = datetime.now()
    session['username'] = username
    db.session.add(new_user)
    db.session.commit()

    addurl(realname, username)

    response = get_user(username)
    response.status_code = 201

    return response


@bp.route('/user/<username>', methods=['PUT'])
def update_user(username):
    pass


@bp.route('/user/<username>', methods=['DELETE'])
def delete_user(username):
    '''
    REST API
    method: delete
    uri: /user/<username>

    delete user and all related db
    '''
    if session.get('username') != username:
        return 'Somebody might hate you ;^;', 400

    # Delete User DB
    found = User.query.filter(
        User.username == username
    ).first()
    db.session.delete(found)

    # Delete URL DB
    found = Url.query.filter(
        Url.username == username
    ).all()
    for url in found:
        db.session.delete(url)

    # Delete Photo DB
    found = Photo.query.filter(
        Photo.username == username
    ).first()
    if found:
        db.session.delete(found)
        os.remove(os.path.join(
            current_app.config['UPLOAD_FOLDER'],
            found.photo
            )
        )

    # Delete Nickname DB
    found = Nickname.query.filter(
        Nickname.username == username
    ).all()
    for nick in found:
        db.session.delete(nick)

    # Delete NickRecom DB
    found = NickRecom.query.filter(
        NickRecom.username == username
    ).all()
    for nick in found:
        db.session.delete(nick)

    db.session.commit()

    session.pop('username', None)
    return redirect('/')
