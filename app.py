from flask import Flask
from config import *
from flask_login import LoginManager
from flask import render_template

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return render_template('unauthorized.html')
