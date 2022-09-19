import sqlalchemy as alchemy

from ..extension import db
from .basic import RecordTimeModel


class Order(db.Model, RecordTimeModel):

    __tablename__ = "order"

    id = alchemy.Column(alchemy.Integer, primary_key=True, autoincrement=True)
    user_id = alchemy.Column(alchemy.Integer, alchemy.ForeignKey("user.id"), nullable=False)
    house_id = alchemy.Column(alchemy.Integer, alchemy.ForeignKey("house.id"), nullable=False)

    begin_date = alchemy.Column(alchemy.DateTime, nullable=False, doc="预定的起始日期")
    end_date = alchemy.Column(alchemy.DateTime, nullable=False, doc="预定的结束日期")
    days = alchemy.Column(alchemy.Integer, nullable=False, doc="预定的总天数")
    house_price = alchemy.Column(alchemy.Integer, nullable=False, doc="房屋的单价")
    amount = alchemy.Column(alchemy.Integer, nullable=False, doc="订单的总金额")
    comment = alchemy.Column(alchemy.Text, doc="订单的评价或拒单原因")
    trade_no = alchemy.Column(alchemy.String(128), doc="交易编号")
    status = alchemy.Column(alchemy.Enum(
        "WAIT_ACCEPT",  # 待接单
        "WAIT_PAYMENT",     # 待支付
        "PAID",     # 已支付
        "WAIT_COMMENT",     # 待评论
        "COMPLETE",     # 已完成
        "CANCELED",     # 已取消
        "REJECTED"      # 已拒单
    ))
