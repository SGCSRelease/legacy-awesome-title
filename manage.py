# manage.py
from app import app  # app.py파일의 app변수를 가져온다.

from flask_script import Manager
from flask_migrate import MigrateCommand

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
        manager.run()
