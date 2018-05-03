# Third Party
from flask import (
    session,
)
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def get_logged_in_username():
    """issue #12 로그인 됬는지 확인하여 Username을 리턴합니다 (없으면 None).

    사실 아래를 짯습니다.
    >>> if 'username' in session:
    ...     return session['username']
    ... return None

    근데 민호형이 이렇게 바꾸었습니다.
    >>> try:
    ...     return session['username']
    ... except KeyError:
    ...     return None

    한번 더 바꾸면 아래처럼 됩니다.
    """
    return session.get('username')  # 없으면 None이 출력됨.
