import sqlalchemy as alchemy

from ..extension import db
from .basic import RecordTimeModel
from .order import Order

__all__ = ["CityArea", "House", "HouseImage", "Order", "Facility"]


class CityArea(db.Model, RecordTimeModel):
    """城区 Table"""

    __tablename__ = "city_area"

    id = alchemy.Column(alchemy.Integer, primary_key=True, autoincrement=True)
    name = alchemy.Column(alchemy.String(32), nullable=False, doc="area name")

    # 区域的房屋
    houses = db.relationship("House", backref="city_area")


# 房屋设施表，建立房屋与设施的多对多关系
house_facility = db.Table(
    "house_facility",
    alchemy.Column("house_id", alchemy.Integer, alchemy.ForeignKey("house.id"), primary_key=True),
    alchemy.Column("facility_id", alchemy.Integer, alchemy.ForeignKey("facility.id"), primary_key=True),
)


class House(db.Model, RecordTimeModel):
    """房屋 Table"""

    __tablename__ = "house"

    id = alchemy.Column(alchemy.Integer, primary_key=True, autoincrement=True)
    user_id = alchemy.Column(alchemy.Integer, alchemy.ForeignKey("user.id"), nullable=False, doc="当前房屋所属的用户ID")
    area_id = alchemy.Column(alchemy.Integer, alchemy.ForeignKey("city_area.id"), nullable=False, doc="所属的城区ID")

    title = alchemy.Column(alchemy.String(64), nullable=False, doc="标题")
    price = alchemy.Column(alchemy.Integer, default=0, doc="价格,单位:分")
    address = alchemy.Column(alchemy.String(512), default="", doc="地址")
    room_count = alchemy.Column(alchemy.Integer, default=1, doc="房间数量")
    acreage = alchemy.Column(alchemy.Integer, default=0, doc="房屋面积")
    unit = alchemy.Column(alchemy.String(32), default="", doc="房屋单元,如:一室一厅")
    capacity = alchemy.Column(alchemy.Integer, default=1, doc="房屋容纳的人数")
    beds = alchemy.Column(alchemy.String(64), default="", doc="房屋床铺的配置")
    deposit = alchemy.Column(alchemy.Integer, default=0, doc="房屋的押金,单位:分")
    min_days = alchemy.Column(alchemy.Integer, default=1, doc="最少入住天数")
    max_days = alchemy.Column(alchemy.Integer, default=0, doc="最多入住天数, 0表示不限制")
    order_count = alchemy.Column(alchemy.Integer, default=0, doc="当前房屋已经完成预定的订单数")
    image_url = alchemy.Column(alchemy.String(256), default="", doc="房屋主图片路径")

    # params: secondary; 表示想要得到Facility表中的数据需要先去house_facility表中查询相同house.id的值
    facilities = db.relationship("Facility", secondary=house_facility)  # 房屋的设施
    images = db.relationship("HouseImage")   # 房屋的图片
    orders = db.relationship("Order", backref="house")  # 房屋的订单

    def change_unit(self):
        self.price /= 100
        self.deposit /= 100
        return self


class Facility(db.Model, RecordTimeModel):
    """房屋设施 Table"""
    __tablename__ = "facility"

    id = alchemy.Column(alchemy.Integer, primary_key=True, autoincrement=True)
    name = alchemy.Column(alchemy.String(32), nullable=False, doc="area name")


class HouseImage(db.Model, RecordTimeModel):
    """房屋图片 Table"""

    __tablename__ = "house_image"

    id = alchemy.Column(alchemy.Integer, primary_key=True, autoincrement=True)
    house_id = alchemy.Column(alchemy.Integer, alchemy.ForeignKey("house.id"), nullable=False, doc="当前图片所属的房屋ID")
    url = alchemy.Column(alchemy.String(256), nullable=False, doc="图片所在的URL地址")
