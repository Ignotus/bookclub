import datetime

from flask import Flask, redirect, url_for, session, request, render_template

from flask.ext.sqlalchemy import SQLAlchemy

from flask_login import LoginManager
from flask.ext.login import login_required, login_user

from flask_oauth import OAuth

from config import *

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY


### SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/ignotus/bookclub/bookclub.db'
db = SQLAlchemy(app)

#with app.app_context():
#    db.create_all()


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
    name = db.Column(db.String)
    progress = db.Column(db.INTEGER)

    def __init__(self, timestamp, book_id, name, progress):
      self.timestamp = timestamp
      self.book_id = book_id
      self.name = name
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



### OAuth Settings
oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'}
)

### Login manager settings
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    user = User.query.get(int(userid))
    if user:
        return user


### Routes
@app.route('/')
def main():
    next_url = request.args.get('next') or url_for('home')
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=next_url,
        _external=True))

@app.route('/update_progress', methods=['POST'])
@login_required
def update_progress():
    book_id = int(request.form['book_id'])
    progress = int(request.form['progress'])

    current_user = User.query.filter_by(id=session["user_id"]).first()
    current_user_full_name = current_user.first_name + current_user.last_name

    db.session.add(Progress(datetime.datetime.now(), book_id, current_user_full_name, progress))
    db.session.commit()
    return "OK"
    
@app.route('/home')
@login_required
def home():
    last_book = db.session.query(Books).order_by(Books.id.desc()).first()

    current_user = User.query.filter_by(id=session["user_id"]).first()
    current_user_full_name = current_user.first_name + current_user.last_name

    last_progress_info = db.session.query(Progress).filter_by(book_id=last_book.id).filter_by(name = current_user_full_name).order_by(Progress.id.desc()).first()

    last_items = db.session.query(Progress).order_by(Progress.id.desc()).limit(20)

    if last_progress_info is not None:
      return render_template('home.html', last_book = last_book, last_progress_info=last_progress_info, last_items=last_items) 
    else:
      return render_template('home.html', last_book=last_book, last_items=last_items)

@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or url_for('home')
    if resp is None:
        # The user likely denied the request
        flash(u'There was a problem logging in.')
        return redirect(next_url)
    session['oauth_token'] = (resp['access_token'], '')
    user_data = facebook.get('/me').data
    user = User.query.filter(User.email == user_data['email']).first()
    if user is None:
        new_user = User(email=user_data['email'], first_name=user_data['first_name'], last_name=user_data['last_name'])
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
    else:
        login_user(user)
    return redirect(next_url)


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


if __name__ == '__main__':
    app.run(host=HOST,port=PORT)
