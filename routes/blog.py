import re
import datetime

from include import *

from sqlalchemy import desc

from flask_wtf import Form
from wtforms import StringField, HiddenField, TextAreaField
from wtforms.validators import DataRequired


@app.route('/blog')
def blog():
    posts = db.session.query(BlogDetailed).all()
    return render_template('blog.html', posts=posts)


class BlogPost(Form):
    id = HiddenField('id')
    topic = StringField('topic', validators=[DataRequired()])
    content = TextAreaField('content', validators=[DataRequired()])
    tags = StringField('tags', validators=[DataRequired()])


@app.route('/blog/add/submit', methods=["POST"])
@login_required
def blog_add_submit():
    form = BlogPost()

    if form.validate_on_submit():
        if not form.data['id']:
            tag_string = form.tags.data
            tags = re.split('\s*,\s*', tag_string)

            new_post = Blog(datetime.datetime.now(),
                            current_user.id,
                            form.topic.data,
                            form.content.data,
                            tag_string)
            db.session.add(new_post)

            db.session.commit()

            for tag in tags:
                db.session.add(Tags(new_post.id, tag))
        else: # Update old posts
            post = db.session.query(Blog).filter_by(id=form.id.data).first()

            if post:
                # Delete all tags
                tags = db.session.query(Tags).filter_by(blog_id=post.id).all()
                for tag in tags:
                    db.session.delete(tag)
                db.session.commit()

                post.last_update = datetime.datetime.now()
                post.topic = form.topic.data
                post.content = form.content.data
                post.tags = form.tags.data

                tags = re.split('\s*,\s*', post.tags)
                for tag in tags:
                    db.session.add(Tags(post.id, tag))

        db.session.commit()

        msg = dict(type='ok')
    else:
        msg = dict(type='error', message='please fill all fields')

    return render_template('plain_data.html', data=msg)

@app.route('/blog/<id>')
def blog_post(id):
    post = db.session.query(BlogDetailed).filter_by(id=id).first()

    tags = re.split('\s*,\s*', post.tags)
    return render_template('blog_post.html', post=post, tags=tags)


@app.route('/blog/<id>/update')
@login_required
def blog_update(id):
    post = db.session.query(Blog).filter_by(id=id).first()

    form = BlogPost()
    form.id.data = post.id
    form.topic.data = post.topic
    form.content.data = post.content
    form.tags.data = post.tags

    return render_template('blog_add.html', form=form)


@app.route('/blog/add')
@login_required
def blog_add():
    form = BlogPost()
    return render_template('blog_add.html', form=form)


@app.route('/blog/filter/tag/<tag>')
def blog_filter_by_tag(tag):
    posts_with_tags = db.session.query(Tags).filter_by(tag=tag).all()

    post_ids = [post.blog_id for post in posts_with_tags]

    posts = []

    for id in post_ids:
        posts += [db.session.query(BlogDetailed).filter_by(id=id).first()]

    return render_template('blog.html', posts=posts)