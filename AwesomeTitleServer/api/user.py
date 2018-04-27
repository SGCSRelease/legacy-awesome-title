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
from AwesomeTitleServer.auth import bp
from AwesomeTitleServer import db

from AwesomeTitleServer.db import (
    User,
    URL,
    Photo,
    Nickname,
    NickRecom,
)


@bp.route('/user/<username>', method=['GET'])
def get_user(username):
    return jsonify(User.query.get_or_404(username).to_dict())


@bp.route('/user/<username>', method=['POST'])
def create_user(username):
    pass


@bp.route('/user/<username>', method=['PUT'])
def update_user(username):
    pass


@bp.route('/user/<username>', method=['DELETE'])
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
    found = URL.query.filter(
        URL.username == username
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



