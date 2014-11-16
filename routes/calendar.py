from flask import render_template, Blueprint
from flask_login import login_required

calendar = Blueprint('calendar', __name__, url_prefix='/calendar')


@calendar.route('/')
@login_required
def main():
    return render_template('calendar/calendar.html')
