from app import app
from config import *
from routes import all

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=PORT)
