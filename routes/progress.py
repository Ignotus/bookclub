import datetime
from include import *


@app.route('/progress')
@login_required
def progress():
    return render_template('progress.html', book=get_current_book())


@app.route('/progress/book/<id>')
@login_required
def progress_data_handler(id):
    return render_template('progress.html', book=db.session.query(Books).filter_by(id=id).first())


@app.route('/progress/update', methods=['POST'])
@login_required
def progress_update():
    book_id = int(request.form['book_id'])
    progress = int(request.form['progress'])

    db.session.add(Progress(datetime.datetime.now(), book_id, int(current_user.id), progress))
    db.session.commit()
    return "Weeeee, you have read " + str(progress) + "% of this book!"


@app.route('/progress/data/<id>')
@login_required
def progress_book_handler(id):
    book = db.session.query(Books).filter_by(id=id).first()
    progress_data = []
    if book is None:
        return render_template('progress_data.html', progress_data=progress_data)

    for user in User.query.all():
        progress_data_element = dict(key=user.first_name)
        progress_data_element["values"] = []

        for prog in Progress.query.filter_by(book_id=book.id).filter_by(user_id=user.id).all():
            progress_data_element["values"] += [[int(1000 * (prog.timestamp - datetime.datetime(1970, 1, 1)).total_seconds()),
                                                 prog.progress]]

        try:
            min_timestamp = min(progress_data_element["values"], key=lambda val: val[0])[0]
            progress_data_element["values"] = [[min_timestamp - 1000 * 24 * 60 * 60, 0]] + progress_data_element["values"]
        except ValueError:
            pass

        if len(progress_data_element["values"]) != 0:
            progress_data += [progress_data_element]

    return render_template('progress_data.html', data=progress_data, book=book)