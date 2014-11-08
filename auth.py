from flask import session
from flask_login import LoginManager
from flask_oauth import OAuth

from config import *
from app import app
from tables import User

### OAuth Settings
oauth = OAuth()

facebook = oauth.remote_app('facebook',
                            base_url='https://graph.facebook.com/',
                            request_token_url=None,
                            access_token_url='/oauth/access_token',
                            authorize_url='https://www.facebook.com/dialog/oauth',
                            consumer_key=FACEBOOK_APP_ID,
                            consumer_secret=FACEBOOK_APP_SECRET,
                            request_token_params={'scope': 'email'})

### Login manager settings
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(userid):
    user = User.query.get(int(userid))
    if user:
        return user


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')