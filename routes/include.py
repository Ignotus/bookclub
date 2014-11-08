import sys
sys.path.append("../")

from flask import render_template, redirect, url_for, request, session
from flask_login import current_user, login_required, login_user

from app import app
from schema import db
from tables import *
from utils import check_authentication, get_current_book
from auth import facebook
from config import *