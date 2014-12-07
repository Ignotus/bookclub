from flask import request

from .tables import Common, Books
from .db import db
from .config import PAGE_SIZE

def get_page_info(sql_request):
    page = 1 if 'page' not in request.args else int(request.args.get('page'))
    item_count = sql_request.count()
    if item_count == 0:
      return ([], 1, 1)
    
    max_page = item_count / PAGE_SIZE
    if item_count % PAGE_SIZE != 0:
      max_page += 1
      
    if page < 0:
      page = 0
    elif page > max_page:
      page = max_page
      
    return (sql_request.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE).all(), page, max_page)


def get_current_book():
    currrent_book_id = db.session.query(Common).filter_by(key="current_book").first()
    if currrent_book_id is None:
        return None

    return db.session.query(Books).filter_by(id=currrent_book_id.value).first()
