from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate

app = Flask(__name__)

import config
app.config.from_object(config)

from db import (
    db,
    Test,
)
db.init_app(app)
migrate = Migrate(app, db)

admin = Admin(app)
admin.add_view(ModelView(Test, db.session))


@app.route("/")
def main():
    return 'main'


@app.route("/newbie")
def register():
    return '회원가입이 들어갈 자리입니다!'


@app.route("/<link>")
def goto(link):
    return '페이지를 제공하는 자리입니다.'


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
