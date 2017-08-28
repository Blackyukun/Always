from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment

from config import config

db = SQLAlchemy()
lm = LoginManager()
lm.login_view = 'auth.login'
mail = Mail()
moment = Moment()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    lm.init_app(app)
    mail.init_app(app)
    moment.init_app(app)

    from always.main.views import main as main_blueprint
    from always.auth.views import auth as auth_blueprint
    from always.admin.views import admin as admin_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    return app
