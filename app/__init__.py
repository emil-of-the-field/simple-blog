from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask_ckeditor import CKEditor


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page'
mail = Mail()
moment = Moment()
ckeditor = CKEditor()

def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(Config)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    #mail.init_app(app)
    #moment.init_app(app)
    ckeditor.init_app(app)
    
    return app

from app import models



