from app import db


class BlogCategory(db.Model):
    __tablename__ = 'blogcategories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    slug = db.Column(db.String(256), unique=True, index=True)
    description = db.Column(db.String(512), nullable=True)
    blogposts = db.relationship('BlogPost', backref='blogcategory', lazy='dynamic')
    created_on = db.Column(db.DateTime)

    def __repr__(self):
        return '<BlogCategory {!r}>'.format(self.name)
