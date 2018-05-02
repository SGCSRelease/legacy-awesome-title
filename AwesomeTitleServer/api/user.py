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
from AwesomeTitleServer.api import bp
from AwesomeTitleServer.db import (
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
    pass


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
