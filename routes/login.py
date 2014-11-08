from include import *


@app.route('/login', methods=["POST"])
def login():
    next_url = request.form['next']

    if 'password' in request.form and request.form['password'] == PASSWORD:
        return facebook.authorize(callback=url_for('facebook_authorized',
                                  next=next_url,
                                  _external=True))
    else:
        return render_template('error.html', msg="Where are you from, dude? Your password isn't correct")


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