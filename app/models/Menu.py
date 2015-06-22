from app import db


class Menu(db.Model):
    __tablename__ = 'menus'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    menu_items = db.relationship('MenuItem', backref='menu', lazy='dynamic')
    pages = db.relationship('Page', backref='menu', lazy='dynamic')
    created_on = db.Column(db.DateTime)

    def __repr__(self):
        return '<Menu {!r}>'.format(self.name)
