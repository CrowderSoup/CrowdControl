from app import db


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
