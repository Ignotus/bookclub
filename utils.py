from flask import url_for, request, render_template
from flask_login import current_user

from tables import Common, Books
from schema import db


def check_authentication(render_func):
    if current_user.is_authenticated():
        return render_func()

    next_url = request.args.get('next') or url_for('home')

    return render_template('authorization.html', next=next_url)


def get_current_book():
    currrent_book_id = db.session.query(Common).filter_by(key="current_book").first()
    if currrent_book_id is None:
        return None

    return db.session.query(Books).filter_by(id=currrent_book_id.value).first()
