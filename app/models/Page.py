from app import db


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
