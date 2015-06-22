from app import db


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
