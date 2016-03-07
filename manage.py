from os import urandom

from flask_script import (
        Manager,
        prompt,
        prompt_bool,
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
        mysql=None,
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
    # XXX : Check '-m' or '--mysql' options entered.
    if mysql is None:
        use_mysql = prompt_bool("Use MySQL?", default=True)
    else:
        if mysql == "True":
            use_mysql = True
        elif mysql == "False":
            use_mysql = False
        else:
            raise Exception("`-m` or `--mysql` option needed `True` or `False`.")
    if use_mysql is True:
        # XXX : Check '-u' or '--username' options entered.
        if username is _default:
            username = prompt("MySQL DB Username", default=username)
        # XXX : Check '-p' or '--password' options entered.
        if not password:
            password = prompt_pass("MySQL DB Password")
        # XXX : Check '-s' or '--server' options entered.
        if server is _server:
            server = prompt("MySQL DB Server", default=server)
        # XXX : Check '-d' or '--database' options entered.
        if database is _default:
            database = prompt("MySQL DB Database", default=database)
    # XXX : Check '-f' or '--folder' options entered.
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
            use_mysql=use_mysql,
        ).dump("config.py")


if __name__ == '__main__':
    manager.run()
