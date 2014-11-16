import datetime

from flask import render_template, Blueprint
from flask_login import current_user, login_required

from core.utils import get_current_book
from core.tables import Progress, Books, User
from core.forms import ProgressForm
from core.db import db

progress = Blueprint('progress', __name__, url_prefix='/progress')


@progress.route('/')
@login_required
def progress_graph():
    return render_template('progress/progress.html', book=get_current_book())


@progress.route('/book/<int:id>')
@login_required
def progress_data_handler(id):
    return render_template('progress/progress.html', book=db.session.query(Books).filter_by(id=id).first())


@progress.route('/update', methods=['POST'])
@login_required
def progress_update():
    form = ProgressForm()

    if form.validate_on_submit():
        book_id = int(form.id.data)
        progress = int(form.progress.data)

        db.session.add(Progress(datetime.datetime.now(), book_id, int(current_user.id), progress))
        db.session.commit()
        return "Weeeee, you have read " + str(progress) + "% of this book!"

    return "Something wrong"


@progress.route('/data/<int:id>')
@login_required
def progress_book_handler(id):
    book = db.session.query(Books).filter_by(id=id).first()
    progress_data = []
    if book is None:
        return render_template('plain_data.html', progress_data=progress_data)

    for user in User.query.all():
        progress_data_element = dict(key=user.first_name)
        progress_data_element["values"] = []

        for prog in Progress.query.filter_by(book_id=book.id, user_id=user.id).all():
            progress_data_element["values"] += [[int(1000 * (prog.timestamp - datetime.datetime(1970, 1, 1)).total_seconds()),
                                                 prog.progress]]

        if len(progress_data_element["values"]) != 0:
            progress_data += [progress_data_element]

    try:
        min_date = min(progress_data, key=lambda p: p["values"][0])["values"][0][0] - 1000 * 24 * 60 * 60
    except ValueError:
        pass

    for data in progress_data:
        data["values"] = [[min_date, 0]] + data["values"]

    return render_template('plain_data.html', data=progress_data)