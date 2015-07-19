from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from har_api import create_app
from har_api.models import db

app = create_app()

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def create(default_data=True, sample_data=False):
    """
    Creates database tables from sqlalchemy models
    """
    from flask.ext.migrate import stamp
    db.create_all()
    stamp()


if __name__ == '__main__':
    manager.run()
