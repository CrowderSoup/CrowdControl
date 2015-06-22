from app import db


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
