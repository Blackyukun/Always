from datetime import datetime
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash

from always import db, lm

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)

    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name

# 权限设置
class Permission(object):
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80

# 检验用户权限对应的类
class AnonymousUser(AnonymousUserMixin):
    def operation(self, permissions):
        return False

    def is_administrator(self):
        return False


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    sex = db.Column(db.String(), default='保密')
    profile = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    # 关注，被关注
    followed = db.relationship('Follow',
                               foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    followers = db.relationship('Follow',
                                foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['ADMINMAIL']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    # 检查用户是否有指定权限
    def operation(self, permissions):
        return self.role is not None and \
               (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.operation(Permission.ADMINISTER)

    # 关注
    def follow(self, user):
        if not self.is_following(user):
            follower = Follow(follower=self, followed=user)
            db.session.add(follower)

    # 取消关注
    def unfollow(self, user):
        follower = self.followed.filter_by(followed_id=user.id).first()
        if follower:
            db.session.delete(follower)

    # 做了一个followed关系查询，这个查询返回所有当前用户作为关注者的(follower, followed)对
    def is_following(self, user):
        return self.followed.filter_by(followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        return self.followers.filter_by(follower_id=user.id).first() is not None

    # 获取关注者文章
    @property
    def followed_posts(self):
        return Post.query.join(Follow, Follow.followed_id == Post.author_id).filter(
            Follow.follower_id == self.id)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Gravatar提供用户头像
    def gravatar(self, size):
        return 'http://www.gravatar.com/avatar/' + md5(self.email.encode('utf-8')).hexdigest() + '?d=mm&s=' + str(
            size)

# 加载用户的回调
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    unread = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# 文章模型
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    body = db.Column(db.Text)
    tag = db.Column(db.String())
    disabled = db.Column(db.Boolean)
    view_num = db.Column(db.Integer, default=0)
    draft = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    like_num = db.relationship('Like', backref='post', lazy='dynamic')
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    # tag_name = db.Column(db.String(), db.ForeignKey('post_tags,name'))

# 小说
class Novel(db.Model):
    __tablename__ = 'novels'
    id = db.Column(db.Integer, primary_key=True)
    novel = db.Column(db.String(64))
    category = db.Column(db.String(), default='长篇')
    tag = db.Column(db.String())
    view_num = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # tag_name = db.Column(db.String(), db.ForeignKey('novel_tags,name'))
    chapters = db.relationship('Chapter', backref='novel', lazy='dynamic')
    # like_num = db.relationship('Like', backref='post', lazy='dynamic')
    # comments = db.relationship('Comment', backref='post', lazy='dynamic')

# 小说章节
class Chapter(db.Model):
    __tablename__ = 'chapters'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    body = db.Column(db.Text)
    disabled = db.Column(db.Boolean)
    view_num = db.Column(db.Integer, default=0)
    draft = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    novel_id = db.Column(db.Integer, db.ForeignKey('novels.id'))

# 评论
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    disabled = db.Column(db.Boolean)
    # 评论类型有comment,reply
    comment_type = db.Column(db.String(64), default='comment')
    reply_to = db.Column(db.String(128), default='notReply')
    unread = db.Column(db.Boolean)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'))

# 点赞
class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    unread = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())

    liker_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'))

# 私信会话
class Conversation(db.Model):
    __tablename__ = 'conversations'
    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    to_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    letter = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    unread = db.Column(db.Boolean, default=True)

    to_user = db.relationship('User', lazy='joined', foreign_keys=[to_user_id])
    from_user = db.relationship('User', lazy='joined', foreign_keys=[from_user_id])

# 管理
class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    notice = db.Column(db.String(25))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())

    def __repr__(self):
        return '<Admin %r>' % (self.notice)
