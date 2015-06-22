from app import db


class BlogPostStatus(db.Model):
    __tablename__ = 'blogpoststatus'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    blogposts = db.relationship('BlogPost', backref='blogpoststatus', lazy='dynamic')