from flask import render_template, Blueprint
from flask_login import current_user, login_required

from core.utils import get_current_book
from core.tables import Progress
from core.forms import ProgressForm
from core.db import db

home = Blueprint('home', __name__, url_prefix='/home')


@home.route('/')
@login_required
def main():
    current_book = get_current_book()

    last_progress_info = db.session.query(Progress).filter_by(book_id=current_book.id, user_id=current_user.id) \
        .order_by(Progress.id.desc()).first() if current_book is not None else None

    form = ProgressForm()
    form.id.data = current_book.id

    if last_progress_info:
        form.progress.data = last_progress_info.progress
    else:
        form.progress.data = 0

    return render_template('home/home.html',
                           current_book=current_book,
                           form=form)