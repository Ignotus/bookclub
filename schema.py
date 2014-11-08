from flask_sqlalchemy import SQLAlchemy

from app import app
from config import *

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_HOST + '/' + DB
db = SQLAlchemy(app)