# Standard Library

# Third Party
from flask import (
    render_template,
)

# Local Application
from AwesomeTitleServer.user import get_logged_in_username


def login_required(func):
    def wrapper_function(*args, **kwargs):
        if not get_logged_in_username():
            return render_template(
                '_error.html',
                _error__msg='Not logged in',
            )
        return func(*args, **kwargs)
    return wrapper_function
