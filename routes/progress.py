import datetime
import sys

from flask import render_template, Blueprint
from flask_login import current_user, login_required

from core.utils import get_current_book
from core.tables import Progress, Books, User
from core.forms import ProgressForm
from core.db import db

progress = Blueprint("progress", __name__, url_prefix="/progress")


@progress.route("/")
@login_required
def progress_graph():
    return render_template("progress/progress.html", book=get_current_book())


@progress.route("/book/<int:id>")
@login_required
def progress_data_handler(id):
    return render_template("progress/progress.html", book=db.session.query(Books).filter_by(id=id).first())


@progress.route("/update", methods=["POST"])
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


@progress.route("/data/<int:id>")
@login_required
def progress_book_handler(id):
    book = db.session.query(Books).filter_by(id=id).first()
    progress_data = []
    if not book:
        return render_template("plain_data.html", progress_data=progress_data)

    users = {user.id : user.first_name for user in User.query.all()}
    progress_per_user = {user_id : [] for user_id in users}

    world_creation = datetime.datetime(1970, 1, 1)

    min_date = sys.maxint
    for progress in Progress.query.filter_by(book_id=book.id).all():
        timestamp = int(1000 * (progress.timestamp - world_creation).total_seconds())
        progress_per_user[progress.user_id] += [[timestamp, progress.progress]]
        min_date = min(min_date, timestamp - 1000 * 24 * 60 * 60)

    if min_date == sys.maxint:
        progress_data = []
    else:
        progress_data = [{"key": users[id],
                          "values": [[min_date, 0]] + progress_per_user[id]}
                         for id in users]

    return render_template("plain_data.html", data=progress_data)