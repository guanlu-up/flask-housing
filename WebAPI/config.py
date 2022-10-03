import datetime

import redis


class DATABASE(object):
    HOST = "192.168.0.105"
    PORT = "3306"
    USERNAME = "root"
    PASSWORD = "root123"
    DB = "HomeApp"
    URI = (USERNAME, PASSWORD, HOST, PORT, DB)


class EnvironConfig(object):
    JSON_AS_ASCII = False
    SQLALCHEMY_DATABASE_URI = "mysql://{}:{}@{}:{}/{}".format(*DATABASE.URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "10#*secret#*%$key!@01"

    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=1)

    REDIS_HOST = "192.168.0.105"
    REDIS_PORT = 6379

    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True   # 对cookie中的session_id进行混淆处理
    PERMANENT_SESSION_LIFETIME = (60 * 60) * 24     # session数据的有效期,单位秒


class DevelopmentConfig(EnvironConfig):
    """开发环境的配置"""
    DEBUG = True
    ENV = "development"


class ProductionConfig(EnvironConfig):
    """生产环境的配置"""
    DEBUG = False
    ENV = "production"


ENVIRON_MAPPER = dict(
    development=DevelopmentConfig,
    production=ProductionConfig,
)
