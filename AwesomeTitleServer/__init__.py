# Third Party
from flask import (
    Flask,
    redirect,
)

# Local Application
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


def create_app():
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

    return app


app = create_app()


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
    }
