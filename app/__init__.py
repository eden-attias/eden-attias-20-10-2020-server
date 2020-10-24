import os

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from config import config

cors = CORS()
db = SQLAlchemy()
jwt = JWTManager()

from app.models.Message import Message
from app.models.User import User


def identity(payload):
    current_user = User.query.filter(User.user_name == payload).first()
    return current_user.user_name


def user_loader(payload):
    return User.query.filter(User.user_name == payload).first()


def create_app():
    # Load Config
    conf = config['local']

    # Init App
    app = Flask(__name__)

    app.config.from_object(conf)

    cors.init_app(app)

    # Database
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'mysql://%s:%s@%s:%s/%s' % (app.config['MYSQL_USER'], app.config['MYSQL_PASSWORD'], app.config['MYSQL_HOST'],
                                    app.config['MYSQL_PORT'], app.config['MYSQL_DB'])

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.logger.info(app.config['SQLALCHEMY_DATABASE_URI'])

    jwt.user_identity_loader(identity)
    jwt.user_loader_callback_loader(user_loader)

    app.config['JWT_SECRET_KEY'] = "v3ry_s3cr3t_k3y"
    jwt.init_app(app)

    # Init DB
    db.init_app(app)

    # Views additon
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
