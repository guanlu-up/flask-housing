from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

from .config import EnvironConfig

# migrate: 数据库迁移
migrate = Migrate()
# jwt: 用于token认证
jwt = JWTManager()
# 利用flask-session, 把session保存到redis中
flask_redis = Session()
redis = EnvironConfig.SESSION_REDIS
# ORM
db = SQLAlchemy()


def extension_register(app: Flask):
    db.init_app(app)
    # db.app = app
    migrate.init_app(app, db)
    jwt.init_app(app)
    flask_redis.init_app(app)
