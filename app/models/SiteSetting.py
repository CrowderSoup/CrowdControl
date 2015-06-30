from app import db


class SiteSetting(db.Model):
    __tablename__ = 'sitesettings'

    name = db.Column(db.String(128), unique=True)
    value = db.Column(db.String())
