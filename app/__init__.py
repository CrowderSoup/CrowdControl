import os
from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask_cloudy import Storage
from config import config
from app.jinja_filters import format_datetime

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
storage = new Storage()

login_manager = LoginManager()

def create_app(config_name):
    the_app = Flask(__name__)
    the_app.config.from_object(config[config_name])
    config[config_name].init_app(the_app)

    bootstrap.init_app(the_app)
    mail.init_app(the_app)
    moment.init_app(the_app)
    db.init_app(the_app)
    storage.init_app(the_app) 

    # Let's set up our login handlers
    import app.login_handlers
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'auth.login'
    login_manager.init_app(the_app)

    the_app.jinja_env.filters['datetime'] = format_datetime

    from app.site import site as site_blueprint
    the_app.register_blueprint(site_blueprint)

    from app.blog import blog as blog_blueprint
    the_app.register_blueprint(blog_blueprint)

    from app.admin import admin as admin_blueprint
    the_app.register_blueprint(admin_blueprint, url_prefix="/admin")

    from app.auth import auth as auth_blueprint
    the_app.register_blueprint(auth_blueprint, url_prefix="/auth")

    return the_app


app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == "__main__":
    app.run()
