from include import *
from login import check_authentication

@app.route('/')
@check_authentication
def main():
    return redirect(url_for('home'))