from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField, SelectField
from wtforms.validators import DataRequired, Length


class ArticleForm(FlaskForm):
    title = StringField('title', validators=[DataRequired(), Length(1, 64)])
    body = TextAreaField('article', validators=[DataRequired()])
    tag = StringField('tag', validators=[DataRequired()])
    save_draft = SubmitField('save draft')
    submit = SubmitField('submit')

class NovelForm(FlaskForm):
    novel = StringField('novel', validators=[DataRequired(), Length(1, 64)])
    category = SelectField('categories', choices=[('长篇', '长篇'), ('短篇', '短篇')])
    # tag = RadioField('tags', choices=[('玄幻奇幻', '玄幻奇幻'), ('武侠仙侠', '武侠仙侠'), \
    #                        ('都市言情', '都市言情'), ('历史军事', '历史军事'), ('科幻灵异', '科幻灵异'), \
    #                        ('网游竞技', '网游竞技'), ('女频频道', '女频频道')], default='玄幻奇幻')
    tag = StringField('tags', validators=[DataRequired()])

class ChapterForm(FlaskForm):
    chapter = StringField('chapter', validators=[DataRequired(), Length(1, 64)])
    body = TextAreaField('body', validators=[DataRequired()])
    save_draft = SubmitField('save draft')
    submit = SubmitField('submit')

class CommentForm(FlaskForm):
    body = TextAreaField('comment', validators=[DataRequired()])

