from app import db
from app.models.User import User
from app.models.Role import Role
from app.models.Page import Page
from app.models.BlogPost import BlogPost
from app.models.BlogCategory import BlogCategory
from app.models.BlogPostStatus import BlogPostStatus
from app.models.PhotoGallery import PhotoGallery
from app.models.PhotoGalleryItem import PhotoGalleryItem
from flask.ext.login import current_user
from flask.ext.restless import APIManager, ProcessingException


# Create API authentication methods
def check_user_auth(instance_id=None, **kw):
    if current_user.is_anonymous() == True or \
            current_user.id != int(instance_id) or \
            current_user.has_role('Admin') != True:
        raise ProcessingException(description='Not Authorized', code=401)


def check_auth(instance_id=None, **kw):
    if current_user.is_anonymous() == True or \
        current_user.has_role('Admin') != True:
        raise ProcessingException(description='Not Authorized', code=401)


def build_api(app):
    # Create the API Manager
    api_manager = APIManager(app, flask_sqlalchemy_db=db)

    # Add API Endpoints
    api_manager.create_api(User, methods=['GET', 'POST', 'DELETE'],
                           preprocessors=dict(
                               GET_SINGLE=[check_user_auth]
                           ))
    api_manager.create_api(Role, methods=['GET', 'POST', 'DELETE'],
                           preprocessors=dict(
                               GET_SINGLE=[check_auth]
                           ))
    api_manager.create_api(Page, methods=['GET', 'POST', 'DELETE'],
                           preprocessors=dict(
                               GET_SINGLE=[check_auth]
                           ))
    api_manager.create_api(BlogPost, methods=['GET', 'POST', 'DELETE'],
                           preprocessors=dict(
                               GET_SINGLE=[check_auth]
                           ))
    api_manager.create_api(BlogCategory, methods=['GET', 'POST', 'DELETE'],
                           preprocessors=dict(
                               GET_SINGLE=[check_auth]
                           ))
    api_manager.create_api(BlogPostStatus, methods=['GET', 'POST', 'DELETE'],
                           preprocessors=dict(
                               GET_SINGLE=[check_auth]
                           ))
    api_manager.create_api(PhotoGallery, methods=['GET', 'POST', 'DELETE'],
                           preprocessors=dict(
                               GET_SINGLE=[check_auth]
                           ))
    api_manager.create_api(PhotoGalleryItem, methods=['GET', 'POST', 'DELETE'],
                           preprocessors=dict(
                               GET_SINGLE=[check_auth]
                           ))

    return api_manager