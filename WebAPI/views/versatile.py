import json

from flask import Blueprint
from flask import request

from ..database.house import CityAreaDB
from ..schema.house import CityAreaSchema
from ..extension import redis
from ..constants import Versatile


versatile_view = Blueprint("versatile", __name__, url_prefix="/api")


@versatile_view.route("/areas", methods=["GET"])
def current_areas():
    """ 获取当前所有的城区名字
    先从redis中尝试获取城区信息, 若redis中没有数据则从数据库中查询
    查询到数据后再重新保存到redis中, 最后将结果返回"""
    response = redis.get("city_areas")
    if response is not None:
        return response

    db = CityAreaDB()
    schema = CityAreaSchema()

    instances: list = db.query_all()
    data = [schema.dump(instance) for instance in instances]
    response = {"status": 200, "message": "success", "data": data}
    response = json.dumps(response, ensure_ascii=False)
    redis.setex("city_areas", Versatile.CITY_AREAS_TIME, response)
    return response
