from schema import *


def get_current_book():
    return db.session.query(Books).order_by(Books.id.desc()).first()