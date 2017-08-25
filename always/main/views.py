from flask import render_template, redirect, url_for, request, Blueprint, flash
from flask_login import login_required, current_user

from always import db
from always.models import User, Post, Permission, Novel
from .forms import ArticleForm, NovelForm, ChapterForm

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

# creation
@main.route('/creation', methods=['GET','POST'])
@login_required
def creation():
    form = NovelForm()
    if form.validate_on_submit():
        novel = Novel(novel=form.novel.data,
                      category=form.category.data,
                      tag=form.tag.data)
        db.session.add(novel)
        flash('你可以开始创作了')
        return redirect(url_for('main.write_novel'))

    return render_template('main/creation.html')

@main.route('/write/article', methods=['GET', 'POST'])
@login_required
def write_article():
    form = ArticleForm()
    if form.validate_on_submit():
        if 'save_draft' in request.form and form.validate():
            post = Post(body=form.body.data,
                        title=form.title.data,
                        tag=form.tag.data,
                        draft=True,
                        author=current_user._get_current_object())
            db.session.add(post)
            flash('保存成功！')
        elif 'submit' in request.form and form.validate():
            post = Post(body=form.body.data,
                        title=form.title.data,
                        tag=form.tag.data,
                        author=current_user._get_current_object())
            db.session.add(post)
            flash('发布成功！')
        return redirect(url_for('main.write'))

    return render_template('main/write_article.html',
                           form=form,
                           title='写文章')

@main.route('/write/novel', methods=['GET','POST'])
@login_required
def write_novel():
    form = ChapterForm()
    pass


