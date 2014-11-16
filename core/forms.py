from flask_wtf import Form

from wtforms import PasswordField, StringField, HiddenField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, NumberRange, url
from flask_wtf.html5 import URLField


class PasswordForm(Form):
    password = PasswordField('password', validators=[DataRequired()])


class BlogPost(Form):
    id = HiddenField('id')
    topic = StringField('topic', validators=[DataRequired()])
    content = TextAreaField('content', validators=[DataRequired()])
    tags = StringField('tags', validators=[DataRequired()])


class ProgressForm(Form):
    id = HiddenField('id')
    progress = IntegerField('name', validators=[DataRequired(), NumberRange(0, 100)])


class BookInfoForm(Form):
    id = HiddenField('id')
    author = StringField('author', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    img = URLField(validators=[url()])
    url = URLField(validators=[url()])
    description = TextAreaField(validators=[DataRequired()])


class CommentForm(Form):
    comment = TextAreaField(validators=[DataRequired()])