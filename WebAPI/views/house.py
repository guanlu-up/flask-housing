import json

from flask import Blueprint
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..database.house import CityAreaDB, HouseDB, Facility
from ..database.users import UsersDB
from ..models.house import House as HouseModel
from ..schema.house import HouseSchema, HouseAllSchema
from ..constants import Houses as HouseCons
from ..extension import redis


house_view = Blueprint("house", __name__, url_prefix="/api/house")


@house_view.route("", methods=["POST"])
@jwt_required()
def house_action():
    if request.method == "POST":
        """发布新房源的API"""
        attributes = ['title', 'price', 'address', 'room_count', 'acreage', 'unit',
                      'capacity', 'beds', 'deposit', 'min_days', 'max_days', 'area_id']
        body: dict = request.get_json()
        columns = {key: body.get(key, None) for key in attributes}
        if not all(columns.values()):
            return {'message': 'Required param is missing'}, 400
        try:
            columns["price"] = int(float(columns["price"]) * 100)
            columns["deposit"] = int(float(columns["deposit"]) * 100)
        except ValueError:
            return {'message': '房屋价格或押金参数值错误'}, 400

        area_db = CityAreaDB()
        if area_db.query_by_id(int(columns["area_id"])) is None:
            return {'message': '城区ID错误'}, 400

        identity: dict = get_jwt_identity()
        columns["user_id"] = identity["userid"]
        # 查询房屋设施信息
        facility = body.get("facility")
        if facility and isinstance(facility, list):
            facilities = Facility.query.filter(Facility.id.in_(facility)).all()
            columns["facilities"] = facilities

        house_db = HouseDB()
        house_model = house_db.create(column_mapper=columns)
        house_schema = HouseAllSchema()
        data = house_schema.dump(house_model)
        return {"status": 200, "message": "success", "data": data}


@house_view.route("/user", methods=["GET"])
@jwt_required()
def user_houses():
    """返回当前用户所发布的所有房源信息"""

    identity: dict = get_jwt_identity()
    user_db = UsersDB()
    current_user = user_db.query_by_id(identity["userid"])
    house_schema = HouseAllSchema()
    data = [house_schema.dump(house) for house in current_user.houses]
    return {"status": 200, "message": "success", "data": data}


@house_view.route("/hot", methods=["GET"])
@jwt_required()
def hot_sale_housing():
    """返回当前销量最好的房源"""

    # 先查询redis, 如果redis中存在则直接返回
    response = redis.get(HouseCons.HOT_HOUSES_SIGN)
    if response is not None:
        return response, 200, {"Content-Type": "application/json"}

    limit = request.args.get("limit", HouseCons.HOT_HOUSES_LIMIT)
    db, schema = HouseDB(), HouseSchema()
    houses = db.order_by(HouseModel.order_count.desc(), limit=limit)
    data = [schema.dump(house) for house in houses]
    response = {"status": 200, "message": "success", "data": data}

    # 将房源信息暂时存储在redis
    redis.setex(HouseCons.HOT_HOUSES_SIGN, HouseCons.HOT_HOUSES_TIME, json.dumps(response))
    return response
