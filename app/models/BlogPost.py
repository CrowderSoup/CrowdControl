from app import db


class BlogPost(db.Model):
    __tablename__ = 'blogposts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    slug = db.Column(db.String(256), unique=True, index=True)
    content = db.Column(db.Text, nullable=True)
    blogcategory_id = db.Column(db.Integer, db.ForeignKey('blogcategories.id'))
    blogpoststatus_id = db.Column(db.Integer, db.ForeignKey('blogpoststatus.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_on = db.Column(db.DateTime)
    published_on = db.Column(db.DateTime)

    def __repr__(self):
        return '<BlogPost {!r}>'.format(self.title)
