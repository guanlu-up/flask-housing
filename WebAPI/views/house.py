from flask import Blueprint
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..database.house import CityAreaDB, HouseDB, Facility
from ..schema.house import HouseSchema


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
        house_schema = HouseSchema()
        data = house_schema.dump(house_model)
        return {"status": 200, "message": "success", "data": data}

