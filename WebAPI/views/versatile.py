from flask import Blueprint
from flask import request

from ..database.house import CityAreaDB
from ..schema.house import CityAreaSchema


versatile_view = Blueprint("versatile", __name__, url_prefix="/api")


@versatile_view.route("/areas", methods=["GET"])
def current_areas():
    """获取当前所有的城区名字"""
    db = CityAreaDB()
    schema = CityAreaSchema()
    instances: list = db.query_all()
    data = [schema.dump(instance) for instance in instances]
    return {"status": 200, "message": "success", "data": data}
