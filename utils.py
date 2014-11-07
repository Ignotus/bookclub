from schema import *


def get_current_book():
    currrent_book_id = db.session.query(Common).filter_by(key="current_book").first()
    if currrent_book_id is None:
        return None

    return db.session.query(Books).filter_by(id=currrent_book_id.value).first()