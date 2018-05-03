# Standard Library

# Third Party
from flask import (
    jsonify,
)

# Local Application
from .db import (
    User,
    Nickname,
    NickRecom,
)
from .api import bp as api


@api.route('/nickname/<username>', methods=['GET'])
def get_nickname(username):
    found = Nickname.query.filter(
        Nickname.username == username
    ).all()

    return [jsonify(nick.to_dict()) for nick in found]


@api.route('/nickname/<username>', methods=['POST'])
def create_nickname(username):
    pass


@api.route('/nickname/<username>', methods=['PUT'])
def update_nickname(username):
    pass


@api.route('/nickname/<username>', methods=['DELETE'])
def delete_nickname(username):
    pass


@api.route('/nickname/recommend/<username>', methods=['GET'])
def get_nickrecom(username):
    found = NickRecom.query.filter(
        NickRecom.username == username
    ).all()

    return [jsonify(nick.to_dict()) for nick in found]


@api.route('/nickname/recommend/<username>', methods=['POST'])
def create_nickrecom(username):
    pass


@api.route('/nickname/recommend/<username>', methods=['PUT'])
def update_nickrecom(username):
    pass


@api.route('/nickname/recommend/<username>', methods=['DELETE'])
def delete_nickrecom(username):
    pass
