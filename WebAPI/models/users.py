import sqlalchemy as alchemy
from werkzeug.security import check_password_hash

from ..extension import db
from .basic import RecordTimeModel
from .house import House
from .order import Order

__all__ = ["User", "House", "Order"]


class User(db.Model, RecordTimeModel):

    __tablename__ = "user"

    id = alchemy.Column(alchemy.Integer, primary_key=True, autoincrement=True)
    username = alchemy.Column(alchemy.String(256), nullable=False, unique=True, doc="username")
    password = alchemy.Column(alchemy.String(256), nullable=False, doc="password")
    is_admin = alchemy.Column(alchemy.Boolean, nullable=False, default=False, doc="是否为管理员")
    is_delete = alchemy.Column(alchemy.Boolean, nullable=False, default=False, doc="是否已删除")
    phone = alchemy.Column(alchemy.String(11), unique=True, nullable=False, doc="手机号")
    real_name = alchemy.Column(alchemy.String(32), doc="真实名称")
    id_card = alchemy.Column(alchemy.String(20), doc="身份证号")
    avatar_url = alchemy.Column(alchemy.String(128), doc="用户头像")

    houses = db.relationship("House", backref="user")
    orders = db.relationship("Order", backref="user")

    def __init__(
            self,
            username: str,
            password: str,
            phone: str,
            real_name: str,
            id_card: str,
            avatar_url=None,
            is_admin=False,
            is_delete=False
    ):
        self.username = username
        self.password = password
        self.phone = phone
        self.real_name = real_name
        self.id_card = id_card
        self.avatar_url = avatar_url
        self.is_admin = is_admin
        self.is_delete = is_delete

    def verify_password(self, password):
        return check_password_hash(self.password, password)
