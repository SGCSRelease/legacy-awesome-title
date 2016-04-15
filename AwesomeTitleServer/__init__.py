from flask import (
    Flask,
    redirect,
)

from .db import (
    admin,
    db,
    migrate,
)
from .nickname import add_routes as add_nickname_routes
from .nickname import has_new_nicknames
from .photo import add_routes as add_photo_routes
from .user import add_routes as add_user_routes
from .user import (
    bcrypt,
    get_logged_in_username,
)
from .url import add_routes as add_url_routes
from .url import goto
from .Achievements.views import add_routes as add_achievements_routes
from .cookie import get_cookie

app = Flask(__name__)

try:
    from . import config
    app.config.from_object(config)
except ImportError as e:
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    if __name__ == "__main__":
        raise Exception("Please run `python manage.py config` first.")

admin.init_app(app)
bcrypt.init_app(app)
db.init_app(app)
migrate.init_app(app, db)

add_user_routes(app)
add_nickname_routes(app)
add_photo_routes(app)
add_url_routes(app)
add_achievements_routes(app)


@app.route("/")
def index():
    perhaps_logged_in_username = get_logged_in_username()
    if perhaps_logged_in_username:
        return redirect("/%s/" % perhaps_logged_in_username)
    return goto("release")


@app.context_processor
def _set_global_variable_for_templates():
    """render_template()에 변수를 넘기지 않고도 사용할 수 있어요!

    Flask의 render_template()는 사실 Jinja2라는 Template Engine을 이용해 제공됩니다.
    근데 여기에 전역변수를 선언할 수 있다네요. WOW!
    """
    return {
            "get_logged_in_username": get_logged_in_username(),
            "has_new_nicknames": has_new_nicknames,
            "get_cookie": get_cookie,
            "get_variable": get_variable,
    }

@app.before_first_request
def _init_database():
    from .Achievements.defaults import update_default_categories, update_default_achievement
    update_default_categories()
    update_default_achievement()


def get_variable(_from, _import):
    # TODO: still not safe -> WHITELIST!!!!! with DECORATOR!
    if not _from or _from[0] != '.':
        return None

    _safety_scope_globals = {
        '__package__': 'AwesomeTitleServer',
    }
    _safety_scope_locals = {}

    # XXX: function call okay! -> NOT SAFE!!
    real_import = _import[:_import.find('(')] if '(' in _import else _import

    exec(
        "from {} import {}".format(_from, real_import),
        _safety_scope_globals,
        _safety_scope_locals
    )
    return eval(
            _import,
            _safety_scope_globals,
            _safety_scope_locals
    )
