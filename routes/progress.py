import datetime
from include import *
from flask_wtf import Form
from flask_wtf.html5 import IntegerField
from wtforms import HiddenField
from wtforms.validators import DataRequired, NumberRange

from login import check_authentication


class ProgressForm(Form):
    id = HiddenField('id')
    progress = IntegerField('name', validators=[DataRequired(), NumberRange(0, 100)])


@app.route('/home')
@check_authentication
def home():
    current_book = get_current_book()

    last_progress_info = db.session.query(Progress).filter_by(book_id=current_book.id) \
        .filter_by(user_id=current_user.id) \
        .order_by(Progress.id.desc()).first() if current_book is not None else None

    form = ProgressForm()
    form.id.data = current_book.id

    if last_progress_info:
        form.progress.data = last_progress_info.progress
    else:
        form.progress.data = 0

    return render_template('home.html',
                           current_user=current_user,
                           current_book=current_book,
                           form=form)


@app.route('/progress')
@login_required
def progress():
    return render_template('progress.html', book=get_current_book())


@app.route('/progress/book/<int:id>')
@login_required
def progress_data_handler(id):
    return render_template('progress.html', book=db.session.query(Books).filter_by(id=id).first())


@app.route('/progress/update', methods=['POST'])
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


@app.route('/progress/data/<int:id>')
@login_required
def progress_book_handler(id):
    book = db.session.query(Books).filter_by(id=id).first()
    progress_data = []
    if book is None:
        return render_template('plain_data.html', progress_data=progress_data)

    for user in User.query.all():
        progress_data_element = dict(key=user.first_name)
        progress_data_element["values"] = []

        for prog in Progress.query.filter_by(book_id=book.id).filter_by(user_id=user.id).all():
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

    return render_template('plain_data.html', data=progress_data, book=book)