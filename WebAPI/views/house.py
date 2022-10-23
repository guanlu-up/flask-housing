import json

from flask import Blueprint
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..database.house import CityAreaDB, HouseDB, Facility
from ..database.users import UsersDB
from ..database.order import OrderDB
from ..models.house import House as HouseModel
from ..schema.house import HouseSchema, HouseFullSchema
from ..constants import Houses as HouseCons
from ..extension import redis


house_view = Blueprint("house", __name__, url_prefix="/api/house")
houses_view = Blueprint("houses", __name__, url_prefix="/api/houses")


# 房源的增删改查
@house_view.route("", methods=["POST"])
@jwt_required()
def house_action():
    if request.method == "POST":
        """发布新房源的API"""
        attributes = ['title', 'price', 'address', 'room_count', 'acreage', 'unit',
                      'capacity', 'beds', 'deposit', 'min_days', 'max_days', 'area_id']
        body: dict = request.get_json()
        columns = {key: body.get(key, None) for key in attributes}
        if None in columns.values():
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
        house_schema = HouseFullSchema()
        data = house_schema.dump(house_model.change_unit())
        return {"status": 200, "message": "success", "data": data}


# 返回当前用户所发布的所有房源信息
@house_view.route("/user", methods=["GET"])
@jwt_required()
def user_houses():
    identity: dict = get_jwt_identity()
    user_db = UsersDB()
    current_user = user_db.query_by_id(identity["userid"])
    house_schema = HouseFullSchema(many=True)
    data = house_schema.dump([house.change_unit() for house in current_user.houses])
    return {"status": 200, "message": "success", "data": data}


# 返回当前销量最好的房源
@house_view.route("/hot", methods=["GET"])
@jwt_required()
def hot_sale_housing():
    # 先查询redis, 如果redis中存在则直接返回
    response = redis.get(HouseCons.HOT_HOUSES_SIGN)
    if response is not None:
        return response, 200, {"Content-Type": "application/json"}

    limit = request.args.get("limit", HouseCons.HOT_HOUSES_LIMIT)
    db, schema = HouseDB(), HouseSchema(many=True)
    houses = db.order_by(HouseModel.order_count.desc(), limit=limit)
    data = schema.dump([house.change_unit() for house in houses])
    response = {"status": 200, "message": "success", "data": data}

    # 将房源信息暂时存储在redis
    redis.setex(HouseCons.HOT_HOUSES_SIGN, HouseCons.HOT_HOUSES_TIME, json.dumps(response))
    return response


# 返回某个房源的详细信息
@house_view.route("/details/<int:house_id>", methods=["GET"])
@jwt_required()
def house_details(house_id):
    db, schema = HouseDB(), HouseFullSchema()
    house = db.query_by_id(house_id)
    if house is None:
        return {"status": 400, "message": "房源ID不存在!"}, 400
    data = schema.dump(house.change_unit())

    if data["user"]["username"] == data["user"]["phone"]:
        data["user"]["username"] = "匿名用户"

    return {"status": 200, "message": "success", "data": data}


@houses_view.route("", methods=["GET"])
def query_houses_by_condition():
    """按照条件查询所有符合的房源, 用于搜索页面"""
    from datetime import datetime

    keymapper = {"start_date": None, "end_date": None,
                 "area_id": None, "sort_key": None, "page": 1}
    conditions = {key: request.args.get(key, value) for key, value in keymapper.items()}
    if not conditions.get("area_id"):
        return {"status": 400, "message": "缺少必须的参数: area_id"}, 400
    conditions["page"] = int(conditions["page"])

    try:
        if conditions.get("start_date"):
            conditions["start_date"] = datetime.strptime(conditions["start_date"], "%Y-%m-%d")
        if conditions.get("end_date"):
            conditions["end_date"] = datetime.strptime(conditions["end_date"], "%Y-%m-%d")
        if conditions.get("start_date") and conditions.get("end_date"):
            assert conditions["start_date"] <= conditions["end_date"]
    except (AssertionError, ValueError):
        return {"status": 400, "message": "日期格式或日期范围不合规!"}, 400

    area = CityAreaDB().query_by_id(int(conditions["area_id"]))
    if not area:
        return {"status": 400, "message": "参数`area_id`无效!"}, 400

    order_db, house_db = OrderDB(), HouseDB()
    _filter = []
    orders = order_db.query_by_vague_date(conditions["start_date"], conditions["end_date"])
    if orders:
        ignore_houses_id = [order.house_id for order in orders]
        _filter.append(HouseModel.id.not_in(ignore_houses_id))
    if conditions.get("area_id"):
        _filter.append(HouseModel.area_id == conditions["area_id"])

    sorts = {
        "new": HouseModel.start_time.desc(),    # 最新发布
        "booking": HouseModel.order_count.desc(),   # 订单量最多
        "price_asc": HouseModel.price.asc(),    # 价格生序
        "price_desc": HouseModel.price.desc()   # 价格降序
    }
    if conditions["sort_key"] not in sorts.keys():
        conditions["sort_key"] = "new"
    _query = house_db.query.filter(*_filter).order_by(sorts.get(conditions["sort_key"]))

    paginate = _query.paginate(page=conditions["page"], per_page=HouseCons.HOUSES_PER_PAGE, error_out=False)
    schema = HouseSchema(many=True)
    data: list = schema.dump([house.change_unit() for house in paginate.items])
    return {"status": 200, "message": "success", "data": data,
            "pages": paginate.pages, "current_page": conditions["page"]}
