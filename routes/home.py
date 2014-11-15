from include import *
from login import check_authentication

@app.route('/')
def main():
    return redirect(url_for('blog'))