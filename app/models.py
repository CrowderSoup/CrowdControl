from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import db, login_manager


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')
    created_on = db.Column(db.DateTime)

    def __repr__(self):
        return '<Role {!r}>'.format(self.name)


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    pages = db.relationship('Page', backref='user', lazy='dynamic')
    blogposts = db.relationship('BlogPost', backref='user', lazy='dynamic')
    created_on = db.Column(db.DateTime)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_role(self, role):
        return role == self.role.name

    def __repr__(self):
        return '<User {!r}>'.format(self.username)


class Menu(db.Model):
    __tablename__ = 'menus'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    menu_items = db.relationship('MenuItem', backref='menu', lazy='dynamic')
    pages = db.relationship('Page', backref='menu', lazy='dynamic')
    created_on = db.Column(db.DateTime)

    def __repr__(self):
        return '<Menu {!r}>'.format(self.name)


class MenuItem(db.Model):
    __tablename__ = 'menuitems'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    slug = db.Column(db.String(256))
    weight = db.Column(db.Integer, default=1)
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'))
    created_on = db.Column(db.DateTime)

    def __repr__(self):
        return '<MenuItem {!r}'.format(self.name)


class Page(db.Model):
    __tablename__ = 'pages'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    slug = db.Column(db.String(256), unique=True, index=True)
    content = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'))
    created_on = db.Column(db.DateTime)
    published_on = db.Column(db.DateTime)
    is_homepage = db.Column(db.Boolean)

    def __repr__(self):
        return '<Page {!r}>'.format(self.title)


class BlogPost(db.Model):
    __tablename__ = 'blogposts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    slug = db.Column(db.String(256), unique=True, index=True)
    content = db.Column(db.Text, nullable=True)
    blogcategory_id = db.Column(db.Integer, db.ForeignKey('blogcategories.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_on = db.Column(db.DateTime)
    published_on = db.Column(db.DateTime)

    def __repr__(self):
        return '<BlogPost {!r}>'.format(self.title)


class BlogCategory(db.Model):
    __tablename__ = 'blogcategories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(512), nullable=True)
    blogposts = db.relationship('BlogPost', backref='blogcategory', lazy='dynamic')
    created_on = db.Column(db.DateTime)

    def __repr__(self):
        return '<BlogCategory {!r}>'.format(self.name)


class PhotoGallery(db.Model):
    __tablename__ = 'photogalleries'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    slug = db.Column(db.String(256), unique=True, index=True)
    description = db.Column(db.Text, nullable=True)
    photogalleryitems = db.relationship('PhotoGalleryItem', backref='photogallery', lazy='dynamic')
    created_on = db.Column(db.DateTime)

    def __repr__(self):
        return '<PhotoGallery {!r}>'.format(self.title)


class PhotoGalleryItem(db.Model):
    __tablename__ = 'photogalleryitems'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True)
    description = db.Column(db.String(512))
    url = db.Column(db.String(2000), unique=True)
    photogallery_id = db.Column(db.Integer, db.ForeignKey('photogalleries.id'))
    created_on = db.Column(db.DateTime)

    def __repr__(self):
        return '<PhotoGalleryItem {!r}'.format(self.title)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
