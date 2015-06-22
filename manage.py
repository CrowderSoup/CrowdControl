#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role, Menu, MenuItem, Page, BlogPost, BlogPostStatus, BlogCategory, \
    PhotoGallery, PhotoGalleryItem
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
        BlogPostStatus=BlogPostStatus,
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


if __name__ == '__main__':
    manager.run()