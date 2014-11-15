from functools import wraps

from include import *

from flask_wtf import Form
from wtforms import PasswordField
from wtforms.validators import DataRequired


class PasswordForm(Form):
    password = PasswordField('password', validators=[DataRequired()])


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('blog'))


@app.route('/login', methods=["POST"])
def login():
    form = PasswordForm()
    if form.validate_on_submit() and form.password.data == PASSWORD:
        return facebook.authorize(callback=PROTOCOL + '://' + HOST + '/login/authorized?next=%2Fhome')
    else:
        return render_template('error.html', msg="Where are you from, dude? Your password isn't correct")


def check_authentication(func):
    @wraps(func)
    def func_wrapper():
        if current_user.is_authenticated():
            return func()

        next_url = request.args.get('next') or url_for('home')

        form = PasswordForm()

        return render_template('authorization.html', next=next_url, login_form=form)

    return func_wrapper


@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or url_for('home')

    if resp is None:
        # The user likely denied the request
        flash(u'There was a problem logging in.')
        return redirect(next_url)

    session['oauth_token'] = (resp['access_token'], '')
    user_data = facebook.get('/me').data
    user = User.query.filter(User.first_name == user_data['first_name'] and User.last_name == user_data['last_name']).first()
    if user is None:
        if 'email' in user_data:
            new_user = User(first_name=user_data['first_name'], last_name=user_data['last_name'], email=user_data['email'])
            db.session.add(new_user)
        else:
            new_user = User(first_name=user_data['first_name'], last_name=user_data['last_name'])
            db.session.add(new_user)

        db.session.commit()
        login_user(new_user)
    else:
        login_user(user)

    return redirect(next_url)