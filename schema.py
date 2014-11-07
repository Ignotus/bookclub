from flask.ext.sqlalchemy import SQLAlchemy

from app import *

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/ignotus/bookclub/bookclub.db'
db = SQLAlchemy(app)


class Books(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.INTEGER, primary_key=True)
    book_name = db.Column(db.String, unique=True)
    book_author = db.Column(db.String)
    img = db.Column(db.String)
    description = db.Column(db.String)

    def __init__(self, book_name, book_author, description, img=None):
        self.book_name = book_name
        self.book_author = book_author
        self.img = img
        self.description = description


class Progress(db.Model):
    __tablename__ = 'progress'
    id = db.Column(db.INTEGER, primary_key=True)
    timestamp = db.Column(db.DateTime)
    book_id = db.Column(db.INTEGER)
    user_id = db.Column(db.INTEGER)
    progress = db.Column(db.INTEGER)

    def __init__(self, timestamp, book_id, user_id, progress):
        self.timestamp = timestamp
        self.book_id = book_id
        self.user_id = user_id
        self.progress = progress


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)

    def __init__(self, email, first_name=None, last_name=None):
        self.email = email.lower()
        self.first_name = first_name
        self.last_name = last_name

    # These four methods are for Flask-Login
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)