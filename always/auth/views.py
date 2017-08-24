from flask import render_template, redirect, \
    url_for, request, Blueprint, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user

from always import db
from always.models import User
from .forms import LoginForm, RegisterForm, ChangePasswordForm, ChangeDataForm

auth = Blueprint('auth', __name__)

# login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('main.index'))
        flash('账号或密码无效。')
    return render_template('auth/login.html',
                           title='登录',
                           form=form)

# logout
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已经登出账号。')
    return redirect(url_for('main.index'))

# register
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    nickname=form.nickname.data,
                    password=form.password.data)
        db.session.add(user)
        flash('你可以登录了。')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',
                           title='注册',
                           form=form)

# change password and personal data
@auth.route('/settings', methods=['GET','POST'])
@login_required
def change_data():
    form = ChangePasswordForm()
    form2 = ChangeDataForm()
    # change password
    if form.change_password.data and form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('你的密码已经更改。')
            return redirect(url_for('auth.change_data'))
        else:
            flash('无效的密码。')

    # setting data
    if form2.save_setting.data and form2.validate_on_submit():
        current_user.nickname = form2.nickname.data
        current_user.sex = form2.sex.data
        current_user.profile = form2.profile.data
        db.session.add(current_user)
        flash('更改资料成功。')
        return redirect(url_for('auth.change_data'))
    else:
        form2.nickname.data = current_user.nickname
        form2.sex.data = current_user.sex
        form2.profile.data = current_user.profile

    return render_template('auth/settings.html',
                           title='设置资料',
                           form=form,
                           form2=form2)
