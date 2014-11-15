from flask import Flask
from flaskext.markdown import Markdown

from config import *


app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY

Markdown(app)