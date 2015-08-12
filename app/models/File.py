from app import db


class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    photo_galleries = db.relationship('Page', backref='menu', lazy='dynamic')
