import datetime
import re

from flask import redirect, url_for, request, render_template
from flask.ext.login import login_required, login_user, current_user

from auth import *
from utils import get_current_book


@app.route('/')
def main():
    if current_user.is_authenticated():
        return redirect(url_for('home'))

    next_url = request.args.get('next') or url_for('home')

    return render_template('authorization.html', next=next_url)


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
    books_info = db.session.query(Books).all()
    return render_template('books.html', books=books_info)


@app.route('/books/read/<id>')
@login_required
def book_read(id):
    current_book = Common.query.filter_by(key="current_book").first()
    if current_book is None:
        db.session.add(Common("current_book", str(id)))
    else:
        current_book.value = str(id)

    db.session.commit()
    return redirect(url_for('home'))


@app.route('/books/add/submit', methods=['POST'])
@login_required
def books_add_submit():
    msg = dict()
    if not ('author' in request.form and 'name' in request.form
            and 'img' in request.form and 'url' in request.form
            and 'description' in request.form):
        msg = dict(type='error', message='please fill all fields')
    else:
        db.session.add(Books(request.form['name'], request.form['author'], request.form['description'],
                             request.form['img'], request.form['url']))
        db.session.commit()
        msg = dict(type='ok')

    return render_template('progress_data.html', data=msg)

@app.route('/books/add')
@login_required
def books_add():
    return render_template('books_add.html')


@app.route('/books/edit/<id>')
@login_required
def books_edit(id):
    book_data = Books.query.filter_by(id=id).first()
    return render_template('books_add.html', book_data=book_data)


@app.route('/books/delete/<id>')
@login_required
def books_delete(id):
    db.session.delete(Books.query.filter_by(id=id).first())
    db.session.commit()
    return redirect(url_for('books'))


@app.route('/comment/submit/<id>', methods=["POST"])
@login_required
def comment_submit(id):
    if 'comment' in request.form:
        comment = re.sub('<[^<]+?>', '', request.form['comment'])
        rx = re.compile("\s*$")
        if not rx.match(comment):
            db.session.add(Comments(datetime.datetime.now(), id, current_user.id, comment))
            book = Books.query.filter_by(id=id).first()
            book.comment_count += 1
            db.session.commit()
    return redirect(url_for('books_comment', id=id))


@app.route('/books/comment/<id>')
@login_required
def books_comment(id):
    book = Books.query.filter_by(id=id).first()
    comments = Comments.query.filter_by(book_id=id).all()

    comment_data = [(User.query.filter_by(id=comment.user_id).first(), comment) for comment in comments]

    return render_template('books_comment.html', comment_data=comment_data, book=book)


@app.route('/books/update', methods=["POST"])
@login_required
def books_update():
    msg = dict()
    if not ('author' in request.form and 'name' in request.form
            and 'img' in request.form and 'url' in request.form
            and 'description' in request.form):
        msg = dict(type='error', message='please fill all fields')
    else:
        item = Books.query.filter_by(id=request.form['id']).first()
        item.book_name = request.form['name']
        item.book_author = request.form['author']
        item.description = request.form['description']
        item.img = request.form['img']
        item.url = request.form['url']
        db.session.commit()
        msg = dict(type='ok')

    return render_template('progress_data.html', data=msg)


def render_progress(book):
    progress_data = []
    if book is None:
        return render_template('progress_data.html', progress_data=progress_data)

    for user in User.query.all():
        progress_data_element = dict(key=user.first_name)
        progress_data_element["values"] = []

        for prog in Progress.query.filter_by(book_id=book.id).filter_by(user_id=user.id).all():
            progress_data_element["values"] += [[int(1000 * (prog.timestamp - datetime.datetime(1970, 1, 1)).total_seconds()),
                                                 prog.progress]]

        if len(progress_data_element["values"]) != 0:
            progress_data += [progress_data_element]

    return render_template('progress_data.html', data=progress_data, book=book)


@app.route('/progress/data/<id>')
@login_required
def progress_book_handler(id):
    return render_progress(db.session.query(Books).filter_by(id=id).first())


@app.route('/progress/book/<id>')
@login_required
def progress_data_handler(id):
    return render_template('progress.html', book=db.session.query(Books).filter_by(id=id).first())


@app.route('/progress')
@login_required
def progress():
    return render_template('progress.html', book=get_current_book())


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
        .order_by(Progress.id.desc()).first() if current_book is not None else None

    return render_template('home.html',
                           current_user=current_user,
                           current_book=current_book,
                           last_progress_info=last_progress_info)


@app.route('/login', methods=["POST"])
def login():
    next_url = request.form['next']

    if 'password' in request.form and request.form['password'] == PASSWORD:
        return facebook.authorize(callback=url_for('facebook_authorized',
                                  next=next_url,
                                  _external=True))
    else:
        return "Where are you from, dude? Your password isn't correct"

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
