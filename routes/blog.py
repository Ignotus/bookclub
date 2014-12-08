import re
import datetime

from sqlalchemy import desc

from core.tables import BlogDetailed, Blog, Tags
from core.db import db
from core.forms import BlogPost
from core.utils import get_page_info

from flask import render_template, Blueprint
from flask_login import current_user, login_required


blog = Blueprint("blog", __name__, url_prefix="/blog")


@blog.route("/", methods=["GET"])
def blog_main():
    all_posts_request = db.session.query(BlogDetailed).order_by(desc(BlogDetailed.id))
    
    posts, page, max_page = get_page_info(all_posts_request)
    
    return render_template("blog/main.html", posts=posts, current_page=page, max_page=max_page)


@blog.route("/update", methods=["POST"])
@login_required
def blog_add_submit():
    form = BlogPost()

    if form.validate_on_submit():
        if not form.data["id"]:
            tag_string = form.tags.data
            tags = re.split("\s*,\s*", tag_string)

            new_post = Blog(datetime.datetime.now(),
                            current_user.id,
                            form.topic.data,
                            form.content.data,
                            tag_string)
            db.session.add(new_post)

            db.session.commit()

            for tag in tags:
                db.session.add(Tags(new_post.id, tag))

        # Update old posts
        else:
            post = db.session.query(Blog).filter_by(id=form.id.data).first()

            if post:
                # Delete all tags
                db.session.query(Tags).filter_by(blog_id=post.id).delete()

                post.last_update = datetime.datetime.now()
                post.topic = form.topic.data
                post.content = form.content.data
                post.tags = form.tags.data

                for tag in re.split("\s*,\s*", post.tags):
                    db.session.add(Tags(post.id, tag))

        db.session.commit()

        msg = dict(type="ok")
    else:
        msg = dict(type="error", message="please fill all fields")

    return render_template("plain_data.html", data=msg)


@blog.route("/<id>")
def blog_post(id):
    post = db.session.query(BlogDetailed).filter_by(id=id).first()

    tags = re.split("\s*,\s*", post.tags)
    return render_template("blog/post.html", post=post, tags=tags)


@blog.route("/<id>/update")
@login_required
def blog_update(id):
    post = db.session.query(Blog).filter_by(id=id).first()

    form = BlogPost()
    form.id.data = post.id
    form.topic.data = post.topic
    form.content.data = post.content
    form.tags.data = post.tags
    return render_template("blog/add.html", form=form)


@blog.route("/add")
@login_required
def blog_add():
    return render_template("blog/add.html", form=BlogPost())


@blog.route("/filter/tag/<tag>", methods=["GET"])
def blog_filter_by_tag(tag):
    posts_with_tags = db.session.query(Tags).filter_by(tag=tag)

    posts_request = db.session.query(BlogDetailed)\
        .filter_by(id=posts_with_tags.subquery().columns.blog_id)\
        .order_by(desc(BlogDetailed.id))

    posts, page, max_page = get_page_info(posts_request)
    
    return render_template("blog/main.html", posts=posts, current_page=page, max_page=max_page)