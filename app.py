# Standard Library
from os import urandom, makedirs
from os.path import abspath, dirname, exists, join

# Third-party Library
import click
from flask_migrate import Migrate
from jinja2 import Template

# Local application
from AwesomeTitleServer import app, db


_default = 'awesometitle'
_server = 'localhost'
_folder = 'datas/DOWNLOADED/'

migrate = Migrate(app, db)


@app.cli.command()
@click.option('--mysql', default=None,
              help='Whether use mysql')
@click.option('--username', default=None,
              help='Mysql username')
@click.option('--password', default=None,
              prompt=True, confirmation_prompt=True, hide_input=True,
              help='Mysql password')
@click.option('--server', default=None,
              help='Mysql server')
@click.option('--database', default=None,
              help='Mysql database')
@click.option('--folder', default=None,
              help='Image upload folder')
def config(
        mysql,
        username,
        password,
        server,
        database,
        folder,
):
    """Generate config.py for AwesomeTitle.

    If there were some given parameters, those questions will be handled
    automatically.
    """
    # TODO : Is Existed config.py?

    base = dirname(abspath(__file__))

    # XXX : Check '-m' or '--mysql' options entered.
    if mysql is None:
        use_mysql = click.confirm("Use MySQL?", default=True)
    else:
        if mysql == "True":
            use_mysql = True
        elif mysql == "False":
            use_mysql = False
        else:
            raise Exception("`-m` or `--mysql` needed `True` or `False`.")
    if use_mysql is True:
        # XXX : Check '-u' or '--username' options entered.
        if username is None:
            username = click.prompt("MySQL DB Username", default=username)
        # XXX : Check '-p' or '--password' options entered.
        if not password:
            password = click.prompt("MySQL DB Password", hide_input=True)
        # XXX : Check '-s' or '--server' options entered.
        if server is None:
            server = click.prompt("MySQL DB Server", default=_server)
        # XXX : Check '-d' or '--database' options entered.
        if database is None:
            database = click.prompt("MySQL DB Database", default=_default)
    # XXX : Check '-f' or '--folder' options entered.
    if folder is None:
        folder = click.prompt("Image Upload Folder", default=_folder)
    folder = join(base, folder)
    if not exists(folder):
        makedirs(folder)
    secret_key = urandom(24)
    with open("confs/config.py.tmpl") as tmpl:
        Template(
            tmpl.read()
        ).stream(
            base=base,
            username=username,
            password=password,
            server=server,
            database=database,
            folder=folder,
            secret_key=secret_key,
            use_mysql=use_mysql,
        ).dump("AwesomeTitleServer/config.py")
