from flask import render_template, Blueprint, redirect, url_for, request, session

from flask_login import current_user, login_user, logout_user


from core.config import *
from core.tables import *
from core.db import db
from core.forms import PasswordForm
from core.facebook_oauth import facebook

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("blog.blog_main"))


@auth.route("/login", methods=["POST"])
def login():
    form = PasswordForm()
    if form.validate_on_submit() and form.password.data == PASSWORD:
        return facebook.authorize(callback=PROTOCOL + "://" + HOST + "/auth/authorized?next=%2Fblog")
    else:
        return render_template("error.html", msg="Where are you from, dude? Your password isn't correct")


@auth.route("/")
def authorization_main():
    next_url = request.args.get("next") or url_for("home.main")
    if current_user.is_authenticated():
        return redirect(next_url)

    form = PasswordForm()

    return render_template("auth/main.html", next=next_url, login_form=form)


@auth.route("/authorized")
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get("next") or url_for("home.main")

    if resp is None:
        # The user likely denied the request
        flash(u"There was a problem logging in.")
        return redirect(next_url)

    session["oauth_token"] = (resp["access_token"], "")
    user_data = facebook.get("/me").data
    user = User.query.filter_by(first_name=user_data["first_name"], last_name=user_data["last_name"]).first()
    if not user:
        if "email" in user_data:
            new_user = User(first_name=user_data["first_name"],
                            last_name=user_data["last_name"],
                            email=user_data["email"])
            db.session.add(new_user)
        else:
            new_user = User(first_name=user_data["first_name"], last_name=user_data["last_name"])
            db.session.add(new_user)

        db.session.commit()
        login_user(new_user)
    else:
        login_user(user)

    return redirect(next_url)