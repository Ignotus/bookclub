import datetime

from flask import redirect, url_for, request, render_template
from flask.ext.login import login_required, login_user, current_user

from auth import *
from utils import get_current_book


@app.route('/')
def main():
    if current_user.is_authenticated():
        return redirect(url_for('home'))

    next_url = request.args.get('next') or url_for('home')
    return facebook.authorize(callback=url_for('facebook_authorized',
                                               next=next_url,
                                               _external=True))


@app.route('/progress/update', methods=['POST'])
@login_required
def update_progress():
    book_id = int(request.form['book_id'])
    progress = int(request.form['progress'])

    db.session.add(Progress(datetime.datetime.now(), book_id, int(current_user.id), progress))
    db.session.commit()
    return "Weeeee, you have read " + str(progress) + "% of this book!"


@app.route('/books')
@login_required
def books():
    return "Not implemented yet"


@app.route('/progress/data')
@login_required
def progress_data_handler():
    progress_data = []
    current_book = get_current_book()
    for user in User.query.all():
        progress_data_element = dict(key=user.first_name)
        progress_data_element["values"] = []

        for prog in Progress.query.filter_by(book_id=current_book.id).filter_by(user_id=user.id).all():
            progress_data_element["values"] += [[int(1000 * (prog.timestamp - datetime.datetime(1970, 1, 1)).total_seconds()),
                                                 prog.progress]]

        if len(progress_data_element["values"]) != 0:
            progress_data += [progress_data_element]

    return render_template('progress_data.html', progress_data=progress_data)


@app.route('/progress')
@login_required
def progress():
    return render_template('progress.html')


@app.route('/calendar')
@login_required
def calendar():
    return render_template('calendar.html')

@app.route('/home')
@login_required
def home():
    current_book = get_current_book()

    last_progress_info = db.session.query(Progress).filter_by(book_id=current_book.id) \
        .filter_by(user_id=current_user.id) \
        .order_by(Progress.id.desc()).first()

    return render_template('home.html',
                           current_user=current_user,
                           current_book=current_book,
                           last_progress_info=last_progress_info)


@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or url_for('home')
    if resp is None:
        # The user likely denied the request
        flash(u'There was a problem logging in.')
        return redirect(next_url)
    session['oauth_token'] = (resp['access_token'], '')
    user_data = facebook.get('/me').data
    user = User.query.filter(User.email == user_data['email']).first()
    if user is None:
        new_user = User(email=user_data['email'], first_name=user_data['first_name'], last_name=user_data['last_name'])
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
    else:
        login_user(user)
    return redirect(next_url)