# Standard
from datetime import datetime

# Third Party
from flask import (
    request,
    session,
    render_template,
    url_for,
    redirect,
)
from flask_bcrypt import Bcrypt

# Local Application
from AwesomeTitleServer.db import db
from AwesomeTitleServer.user import check_username
from . import bp
from .utils import bcrypt


@bp.route('/login/', methods=['GET', 'POST'])
def login():
    '''
    issue #12 Login
    '''
    if request.method == 'GET':
        return render_template('login.html')
    else:
        found = check_username(request.form['usr'], is_internal=True)
        if not found:
            return render_template(
                    '_error.html',
                    _error__msg='wrong login information'
                ), 400
        if not bcrypt.check_password_hash(
                found.password_hash,
                request.form['pwd'],
            ):
            return render_template(
                    '_error.html',
                    _error__msg='wrong login information'
                ), 400

        username = request.form['usr']
        found.last_login = datetime.now()
        db.session.add(found)
        db.session.commit()
        session['username'] = username
        return redirect(url_for('goto', link=username))


@bp.route('/logout/')
def logout():
    '''
    issue #12 Logout
    '''
    session.pop('username', None)
    return redirect('/')
