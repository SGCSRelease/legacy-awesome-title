from flask import (
    Flask,
    render_template,
)

import config
from db import (
    admin,
    db,
    migrate,
)
from nickname import add_routes as add_nickname_routes
from photo import add_routes as add_photo_routes
from user import add_routes as add_user_routes
from user import (
    bcrypt,
    get_logged_in_username,
)
from url import add_routes as add_url_routes

app = Flask(__name__)

app.config.from_object(config)

admin.init_app(app)
bcrypt.init_app(app)
db.init_app(app)
migrate.init_app(app, db)

add_user_routes(app)
add_nickname_routes(app)
add_photo_routes(app)
add_url_routes(app)


# TODO : 릴리즈페이지를 보여주도록 수정!
@app.route("/")
def index():
    perhaps_logged_in_username = get_logged_in_username(is_boolean=False)
    if perhaps_logged_in_username:
        return render_template(
                "main.html",
                naeyoung='',
                loggedin=True,
        )
    return render_template(
            "main.html",
            naeyoung='로그인안하셨어요 /login 가 보세요',
            loggedin=False,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
