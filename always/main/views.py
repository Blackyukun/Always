from flask import render_template, redirect, url_for, request, Blueprint, flash, current_app
from flask_login import login_required, current_user

from always import db
from always.models import User, Post, Permission, Novel, Comment
from .forms import ArticleForm, NovelForm, ChapterForm, CommentForm

# register blueprint
main = Blueprint('main', __name__)

# index page
@main.route('/')
@main.route('/index')
def index():
    return render_template('main/index.html')

# member information
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

# creation choice
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

    return render_template('main/creation.html',
                           title="创作",
                           form=form)

# write article
@main.route('/write/article', methods=['GET', 'POST'])
@login_required
def write_article():
    form = ArticleForm()
    if current_user.operation(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
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
        return redirect(url_for('main.write_article'))

    return render_template('main/write_article.html',
                           form=form,
                           title='写文章')

# write novel chapter page
@main.route('/write/novel', methods=['GET','POST'])
@login_required
def write_novel():
    form = ChapterForm()
    if current_user.operation(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        if 'save_draft' in request.form and form.validate():
            post = Post(body=form.body.data,
                        title=form.title.data,
                        draft=True,
                        author=current_user._get_current_object())
            db.session.add(post)
            flash('保存成功！')
        elif 'submit' in request.form and form.validate():
            post = Post(body=form.body.data,
                        title=form.title.data,
                        author=current_user._get_current_object())
            db.session.add(post)
            flash('发布成功！')
        return redirect(url_for('main.write_novel'))

    return render_template('main/write_article.html',
                           form=form,
                           title='写小说')
# draft page
@main.route('/draft/')
@login_required
def draft():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items
    drafts = [post for post in posts if post.draft==True]

    return render_template('user/draft.html',
                           title='草稿',
                           pagination=pagination,
                           drafts=drafts)

# delete draft
@main.route('/delete-draft/<int:id>')
@login_required
def delete_draft(id):
    draft = Post.query.get_or_404(id)
    draft.disabled = True
    db.session.add(draft)
    flash('删除草稿成功。')
    return redirect(url_for('user.draft'))

# article details and send comments
@main.route('/post/<int:id>', methods=['GET','POST'])
def post(id):
    post = Post.query.get_or_404(id)
    post.view_num += 1
    db.session.add(post)
    # 评论
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post, unread=True,
                          author=current_user._get_current_object())
        db.session.add(comment)
        flash('你的评论已经发表成功。')
        return redirect(url_for('user.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) / \
               current_app.config['COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['COMMENTS_PER_PAGE'],
        error_out=False
    )
    comments = pagination.items
    return render_template('user/post.html', posts=[post],
                           title=post.title, id=post.id,
                           post=post, form=form,
                           comments=comments,
                           pagination=pagination)
