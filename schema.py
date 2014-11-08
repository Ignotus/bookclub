from flask.ext.sqlalchemy import SQLAlchemy

from app import *

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + USER + ':' + DB_PASSWORD + '@' + DB_HOST + '/' + DB
db = SQLAlchemy(app)


class Common(db.Model):
    __tablename__ = 'common'
    id = db.Column(db.INTEGER, primary_key=True)
    key = db.Column(db.String, unique=True)
    value = db.Column(db.String)

    def __init__(self, key, value):
        self.key = key
        self.value = value


class Books(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.INTEGER, primary_key=True)
    book_name = db.Column(db.String, unique=True)
    book_author = db.Column(db.String)
    img = db.Column(db.String)
    description = db.Column(db.String)
    url = db.Column(db.String)
    comment_count = db.Column(db.INTEGER)

    def __init__(self, book_name, book_author, description, img, url):
        self.book_name = book_name
        self.book_author = book_author
        self.img = img
        self.description = description
        self.url = url
        self.comment_count = 0


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


class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.INTEGER, primary_key=True)
    timestamp = db.Column(db.DateTime)
    book_id = db.Column(db.INTEGER)
    user_id = db.Column(db.INTEGER)
    comment = db.Column(db.String)

    def __init__(self, timestamp, book_id, user_id, comment):
        self.timestamp = timestamp
        self.book_id = book_id
        self.user_id = user_id
        self.comment = comment


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
