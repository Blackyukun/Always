from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError

from always.models import User


# login form
class LoginForm(FlaskForm):
    nickname = StringField('nickname', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember', default=False)


# register form
class RegisterForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Length(1, 64), Email()])
    nickname = StringField('nickname', validators=[DataRequired(), Length(1, 64),
                    Regexp('^[\u4e00-\u9fa5]|[a-z]|[A-Z][0-9_.]*', 0,
                           "昵称必须以汉字或字母开头哦。")])
    password = PasswordField('password', validators=[DataRequired(),
                    EqualTo('password2', message="密码必须确认一致。")])
    password2 = PasswordField('confirm password', validators=[DataRequired()])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("这个邮箱已被注册。")

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError("这个昵称已经存在了。")

