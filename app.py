from flask import Flask
from config import *

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
