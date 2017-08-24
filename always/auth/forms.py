from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, \
    BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Regexp,\
    EqualTo, ValidationError

from always.models import User


# a custom validator for forms
def verification(FlaskForm, field):
    pass

# login form
class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Length(1, 64), Email()])
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

# change password
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('old password', validators=[DataRequired()])
    password = PasswordField('new password', validators=[DataRequired(),
                    EqualTo('password2', message='密码必须确认一致。')])
    password2 = PasswordField('confirm new password', validators=[DataRequired()])
    change_password = SubmitField('change password')

# change personal data
class ChangeDataForm(FlaskForm):
    nickname = StringField('nickname', validators=[DataRequired(), Length(1, 64),
                    Regexp('^[\u4e00-\u9fa5]|[a-z]|[A-Z][0-9_.]*', 0,
                           "昵称必须以汉字或字母开头哦。")])
    sex = SelectField('sex', choices=[('男', '男'), ('女', '女'), ('保密', '保密')])
    profile = TextAreaField('profile', validators=[Length(0, 140)])
    save_setting = SubmitField('save settings')

