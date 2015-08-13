from app import db


class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    photogalleryitems = db.relationship('PhotoGalleryItem', 
                                        backref='file', lazy='dynamic')
