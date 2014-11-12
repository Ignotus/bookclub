import datetime
from include import *

from flask_wtf import Form
from flask_wtf.html5 import URLField
from wtforms import StringField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, url


@app.route('/books')
@login_required
def books():
    books_info = db.session.query(Books).all()
    return render_template('books.html', books=books_info)


@app.route('/books/<int:id>/read')
@login_required
def book_read(id):
    current_book = Common.query.filter_by(key="current_book").first()
    if current_book is None:
        db.session.add(Common("current_book", str(id)))
    else:
        current_book.value = str(id)

    db.session.commit()
    return redirect(url_for('home'))


class BookInfoForm(Form):
    id = HiddenField('id')
    author = StringField('author', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    img = URLField(validators=[url()])
    url = URLField(validators=[url()])
    description = TextAreaField(validators=[DataRequired()])


@app.route('/books/add')
@login_required
def books_add():
    form = BookInfoForm()
    return render_template('books_add.html', form=form)


@app.route('/books/<int:id>/edit')
@login_required
def books_edit(id):
    book_data = Books.query.filter_by(id=id).first()

    form = BookInfoForm()
    form.id.data = book_data.id
    form.author.data = book_data.book_author
    form.name.data = book_data.book_name
    form.img.data = book_data.img
    form.url.data = book_data.url
    form.description.data = book_data.description

    return render_template('books_add.html', form=form)


@app.route('/books/<int:id>/delete')
@login_required
def books_delete(id):
    db.session.delete(Books.query.filter_by(id=id).first())
    db.session.commit()
    return redirect(url_for('books'))


class CommentForm(Form):
    comment = TextAreaField(validators=[DataRequired()])

@app.route('/books/<int:id>/comment/submit', methods=["POST"])
@login_required
def comment_submit(id):
    form = CommentForm()

    if form.validate_on_submit():
        print "Submit"
        db.session.add(Comments(datetime.datetime.now(), id, current_user.id, form.comment.data))
        book = Books.query.filter_by(id=id).first()
        book.comment_count += 1
        db.session.commit()

    return redirect(url_for('books_comment', id=id))


@app.route('/books/<int:id>/comment')
@login_required
def books_comment(id):
    book = Books.query.filter_by(id=id).first()
    comments = Comments.query.filter_by(book_id=id).all()

    comment_data = [(User.query.filter_by(id=comment.user_id).first(), comment) for comment in comments]

    comment_form = CommentForm()

    return render_template('books_comment.html', comment_data=comment_data, book=book, comment_form=comment_form)


@app.route('/books/update', methods=["POST"])
@login_required
def books_update():
    form = BookInfoForm()
    if form.validate_on_submit():
        # Add new item
        if not form.data['id']:
            db.session.add(Books(form.name.data,
                                 form.author.data,
                                 form.description.data,
                                 form.img.data,
                                 form.url.data))
        else:
            item = Books.query.filter_by(id=request.form['id']).first()
            item.book_name = form.name.data
            item.book_author = form.author.data
            item.description = form.description.data
            item.img = form.img.data
            item.url = form.url.data

        db.session.commit()
        msg = dict(type='ok')
    else:
        msg = dict(type='error', message='please fill all fields')

    return render_template('plain_data.html', data=msg)