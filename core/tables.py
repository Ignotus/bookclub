from .db import db

from flask_sqlalchemy import Model
from sqlalchemy import Integer, String, Column, DateTime


class Books(db.Model):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    book_name = Column(String, unique=True)
    book_author = Column(String)
    img = Column(String)
    description = Column(String)
    url = Column(String)
    comment_count = Column(Integer)

    def __init__(self, book_name, book_author, description, img, url):
        self.book_name = book_name
        self.book_author = book_author
        self.img = img
        self.description = description
        self.url = url
        self.comment_count = 0


class Comments(db.Model):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    book_id = Column(Integer)
    user_id = Column(Integer)
    comment = Column(String)

    def __init__(self, timestamp, book_id, user_id, comment):
        self.timestamp = timestamp
        self.book_id = book_id
        self.user_id = user_id
        self.comment = comment


# It's a view
class CommentsDetailed(db.Model):
    __tablename__ = 'comments_detailed'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    book_id = Column(Integer)
    user_first_name = Column(String)
    user_last_name = Column(String)
    comment = Column(String)


class Common(db.Model):
    __tablename__ = 'common'
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)
    value = Column(String)

    def __init__(self, key, value):
        self.key = key
        self.value = value


class Progress(db.Model):
    __tablename__ = 'progress'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    book_id = Column(Integer)
    user_id = Column(Integer)
    progress = Column(Integer)

    def __init__(self, timestamp, book_id, user_id, progress):
        self.timestamp = timestamp
        self.book_id = book_id
        self.user_id = user_id
        self.progress = progress


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)

    def __init__(self, first_name=None, last_name=None, email=None):
        if email is not None:
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
        return str(self.id)


class Blog(db.Model):
    __tablename__ = 'blog'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    last_update = Column(DateTime)
    user_id = Column(Integer)
    topic = Column(String)
    content = Column(String)
    tags = Column(String)

    def __init__(self, timestamp, user_id, topic, content, tags):
        self.timestamp = timestamp
        self.last_update = timestamp
        self.user_id = user_id
        self.topic = topic
        self.content = content
        self.tags = tags


# It's a view
class BlogDetailed(db.Model):
    __tablename__ = 'blog_detailed'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    last_update = Column(DateTime)
    user_first_name = Column(String)
    user_last_name =  Column(String)
    topic = Column(String)
    content = Column(String)
    tags = Column(String)


class Tags(db.Model):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    blog_id = Column(Integer)
    tag = Column(String)

    def __init__(self, blog_id, tag):
        self.blog_id = blog_id
        self.tag = tag