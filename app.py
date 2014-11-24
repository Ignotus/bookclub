from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user
from flaskext.markdown import Markdown
from flask_assets import Environment, Bundle

route_modules = ["auth", "blog", "progress", "home", "calendar", "books"]
for module in route_modules:
    exec("from routes.%s import %s" % (module, module))

from core.config import *
from core.db import db
from core.tables import User

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+cymysql://" + DB_USER + ":" + DB_PASSWORD + "@" + DB_HOST + "/" + DB

db.init_app(app)

Markdown(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(userid):
    user = User.query.get(int(userid))
    if user:
        return user


app.debug = DEBUG
app.secret_key = SECRET_KEY

@app.route("/")
def main():
    if current_user.is_authenticated():
        return redirect(url_for("home.main"))
    return redirect(url_for("blog.blog_main"))

modules = [auth, blog, progress, home, calendar, books]

for module in modules:
    app.register_blueprint(module)


@app.errorhandler(401)
def custom_401(error):
    return render_template("unauthorized.html")

assets = Environment(app)
css = Bundle("css/blog.css", "css/style.css",
            filters="cssmin", output="gen/style.min.css")

js_markdown = Bundle("js/to-markdown.js", "js/markdown.js",
                     filters="jsmin", output="gen/markdown.min.js")

css_tagsinput = Bundle("css/bootstrap-tagsinput.css", filters="cssmin",
                        output="gen/bootstrap-tagsinput.min.css")

js_tagsinput = Bundle("js/bootstrap-tagsinput.js", filters="jsmin",
                        output="gen/bootstrap-tagsinput.min.js")

assets.register("css_all", css)
assets.register("js_markdown", js_markdown)
assets.register("css_tagsinput", css_tagsinput)
assets.register("js_tagsinput", js_tagsinput)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=PORT)
