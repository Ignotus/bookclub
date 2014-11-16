from flask import Flask, render_template
from flask_login import LoginManager
from flaskext.markdown import Markdown

from routes.auth import auth
from routes.blog import blog
from routes.progress import progress
from routes.home import home
from routes.calendar import calendar
from routes.books import books

from core.config import *
from core.db import db
from core.tables import User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_HOST + '/' + DB

db.init_app(app)

Markdown(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(userid):
    user = User.query.get(int(userid))
    if user:
        return user


app.debug = DEBUG
app.secret_key = SECRET_KEY

modules = [auth, blog, progress, home, calendar, books]

for module in modules:
    app.register_blueprint(module)


@app.errorhandler(401)
def custom_401(error):
    return render_template('unauthorized.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=PORT)