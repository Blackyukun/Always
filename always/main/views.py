from flask import render_template, redirect, url_for, request, Blueprint, flash

from always import db
from always.models import User, Post

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
def index():
    return render_template('main/index.html')

@main.route('/user/<nickname>')
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user == None:
        flash("未发现用户：" + nickname)
        return redirect(url_for('main.index'))
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    posts = [post for post in posts if post.draft == False]
    return render_template('main/user.html',
                           user=user,
                           posts=posts,
                           title='个人资料')


