#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role, Menu, MenuItem, Page, BlogPost, BlogCategory, PhotoGallery, PhotoGalleryItem
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from install import install_with_sample_content

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(
        app=app,
        db=db,
        User=User,
        Role=Role,
        Menu=Menu,
        MenuItem=MenuItem,
        Page=Page,
        BlogPost=BlogPost,
        BlogCategory=BlogCategory,
        PhotoGallery=PhotoGallery,
        PhotoGalleryItem=PhotoGalleryItem
    )


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def install():
    """Create a bunch of default data and such"""
    install_with_sample_content('aaron.crowder@gmail.com')


@manager.option('-h', '--host', dest='host', default='127.0.0.1')
@manager.option('-p', '--port', dest='port', type=int, default=6969)
@manager.option('-w', '--workers', dest='workers', type=int, default=3)
def gunicorn(host, port, workers):
    """Start the Server with Gunicorn"""
    from gunicorn.app.base import Application

    class FlaskApplication(Application):
        def init(self, parser, opts, args):
            return {
                'bind': '{0}:{1}'.format(host, port),
                'workers': workers
            }

        def load(self):
            return app

    application = FlaskApplication()
    return application.run()


if __name__ == '__main__':
    manager.run()