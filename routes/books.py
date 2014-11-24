import datetime

from core.db import db
from core.forms import BookInfoForm, CommentForm
from core.tables import Books, Common, Comments, CommentsDetailed

from flask import render_template, Blueprint, redirect, url_for, request
from flask_login import current_user, login_required


books = Blueprint("books", __name__, url_prefix="/books")


@books.route("/")
@login_required
def main():
    books_info = db.session.query(Books).all()
    return render_template("books/main.html", books=books_info)


@books.route("/<int:id>/read")
@login_required
def book_read(id):
    current_book = Common.query.filter_by(key="current_book").first()
    if current_book is None:
        db.session.add(Common("current_book", str(id)))
    else:
        current_book.value = str(id)

    db.session.commit()
    return redirect(url_for("home.main"))


@books.route("/add")
@login_required
def books_add():
    form = BookInfoForm()
    return render_template("books/add.html", form=form)


@books.route("/<int:id>/edit")
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

    return render_template("books/add.html", form=form)


@books.route("/<int:id>/delete")
@login_required
def books_delete(id):
    db.session.delete(Books.query.filter_by(id=id).first())
    db.session.commit()
    return redirect(url_for("main"))


@books.route("/<int:id>/comment/submit", methods=["POST"])
@login_required
def comment_submit(id):
    form = CommentForm()

    if form.validate_on_submit():
        db.session.add(Comments(datetime.datetime.now(), id, current_user.id, form.comment.data))
        book = Books.query.filter_by(id=id).first()
        book.comment_count += 1
        db.session.commit()

    return redirect(url_for("books.books_comment", id=id))


@books.route("/<int:id>/comment")
@login_required
def books_comment(id):
    book = Books.query.filter_by(id=id).first()
    comments = CommentsDetailed.query.filter_by(book_id=id).all()

    comment_form = CommentForm()

    return render_template("books/comment.html", comment_data=comments, book=book, comment_form=comment_form)


@books.route("/update", methods=["POST"])
@login_required
def books_update():
    form = BookInfoForm()
    if form.validate_on_submit():
        # Add new item
        if not form.data["id"]:
            db.session.add(Books(form.name.data,
                                 form.author.data,
                                 form.description.data,
                                 form.img.data,
                                 form.url.data))
        else:
            item = Books.query.filter_by(id=request.form["id"]).first()
            item.book_name = form.name.data
            item.book_author = form.author.data
            item.description = form.description.data
            item.img = form.img.data
            item.url = form.url.data

        db.session.commit()
        msg = dict(type="ok")
    else:
        msg = dict(type="error", message="please fill all fields")

    return render_template("plain_data.html", data=msg)