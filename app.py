from flask import Flask
from flaskext.markdown import Markdown

from config import *
from flask_login import LoginManager
from flask import render_template


app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY

Markdown(app)

@app.errorhandler(401)
def custom_401(error):
    return render_template('unauthorized.html')
