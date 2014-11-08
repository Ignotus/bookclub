import re
import datetime
from include import *

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
        db.session.add(Books(request.form['name'],
                             request.form['author'],
                             request.form['description'],
                             request.form['img'],
                             request.form['url']))
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
        comment = request.form['comment']
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