from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Test(db.Model):
    """
    Represents one 'test run' which could contain multiple pages.
    """
    id = db.Column(db.Integer, primary_key=True)
    creation_time = db.Column(db.DateTime, default=None, nullable=True)
    pages = db.relationship('Page', backref='test',
                            cascade='all, delete-orphan')


class Page(db.Model):
    """
    Represents one page from a test run.
    """
    id = db.Column(db.Integer, primary_key=True)
    load_time = db.Column(db.Float, default=None, nullable=True)
