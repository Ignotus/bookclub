from include import *


@app.route('/')
def main():
    return check_authentication(lambda: redirect(url_for('home')))


def render_home():
    current_book = get_current_book()

    last_progress_info = db.session.query(Progress).filter_by(book_id=current_book.id) \
        .filter_by(user_id=current_user.id) \
        .order_by(Progress.id.desc()).first() if current_book is not None else None

    return render_template('home.html',
                           current_user=current_user,
                           current_book=current_book,
                           last_progress_info=last_progress_info)


@app.route('/home')
def home():
    return check_authentication(render_home)