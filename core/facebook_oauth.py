from flask import session
from flask_oauth import OAuth

from config import FACEBOOK_APP_ID, FACEBOOK_APP_SECRET

oauth = OAuth()

facebook = oauth.remote_app('facebook',
                            base_url='https://graph.facebook.com/',
                            request_token_url=None,
                            access_token_url='/oauth/access_token',
                            authorize_url='https://www.facebook.com/dialog/oauth',
                            consumer_key=FACEBOOK_APP_ID,
                            consumer_secret=FACEBOOK_APP_SECRET,
                            request_token_params={'scope': 'email'})


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')