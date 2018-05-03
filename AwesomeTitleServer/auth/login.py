# Third Party
from flask import (
    render_template,
    url_for,
)
from flask_bcrypt import Bcrypt

# Local Application
from AwesomeTitleServer import app
from .url import goto
from .auth.utils import bcrypt


@app.route('/login/', methods=['GET', 'POST'])
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
        return redirect(url_for(goto, username))


@app.route('/logout/')
def logout():
    '''
    issue #12 Logout
    '''
    session.pop('username', None)
    return redirect('/')
