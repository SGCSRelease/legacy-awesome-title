from os import urandom

from flask_script import (
        Manager,
        prompt,
        prompt_pass,
)
from flask_migrate import MigrateCommand
from jinja2 import Template

from app import app  # app.py파일의 app변수를 가져온다.


manager = Manager(app)
manager.add_command('db', MigrateCommand)
_default = 'awesometitle'
_server = 'localhost'
_folder = './DOWNLOADED/'


@manager.command
def config(
        username=_default,
        password=None,
        server=_server,
        database=_default,
        folder=_folder,
):
    """Generate config.py for AwesomeTitle.

    If there were some given parameters, those questions will be handled
    automatically.
    """
    # TODO : Is Existed config.py?
    if username is _default:
        username = prompt("MySQL DB Username", default=username)
    if not password:
        password = prompt_pass("MySQL DB Password")
    if server is _server:
        server = prompt("MySQL DB Server", default=server)
    if database is _default:
        database = prompt("MySQL DB Database", default=database)
    if folder is _folder:
        folder = prompt("Image Upload Folder", default=folder)
    secret_key = urandom(24)
    with open("config.py.tmpl") as tmpl:
        Template(
                tmpl.read()
        ).stream(
            username=username,
            password=password,
            server=server,
            database=database,
            folder=folder,
            secret_key=secret_key,
        ).dump("config.py")


if __name__ == '__main__':
    manager.run()
