from flask import render_template, redirect, url_for, request, Blueprint, flash
from flask_login import login_user, login_required, logout_user

from always import db
from always.models import User
from .forms import LoginForm, RegisterForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(nickname=form.nickname.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('main.index'))
        flash('账号或密码无效。')
    return render_template('auth/login.html',
                           title='登录',
                           form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已经登出账号。')
    return redirect(url_for('main.index'))

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

