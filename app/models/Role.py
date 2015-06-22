from app import db


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')
    created_on = db.Column(db.DateTime)

    def __repr__(self):
        return '<Role {!r}>'.format(self.name)