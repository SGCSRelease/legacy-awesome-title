from flask import (
    Flask,
    redirect,
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
from url import goto

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


@app.route("/")
def index():
    perhaps_logged_in_username = get_logged_in_username()
    if perhaps_logged_in_username:
        return redirect("/%s/" % perhaps_logged_in_username)
    return goto("release")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
