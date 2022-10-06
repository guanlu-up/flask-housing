import re

from flask import Blueprint
from flask import request
from werkzeug.security import generate_password_hash

from ..models import users as users_model
from ..database.users import UsersDB
from ..schema.users import UserSchema

USER_SCHEMA = UserSchema()
users_view = Blueprint("users", __name__, url_prefix="/api/users")


@users_view.route("", methods=["POST"])
def add_user():
    api = UsersAPI()

    if request.method == "POST":
        return api.create_user()


@users_view.route("/<int:userid>", methods=["GET", "PUT", "DELETE"])
def user_update(userid):
    api = UsersAPI()

    # 获取用户详细信息
    if request.method == "GET":
        user_db = UsersDB()
        user: users_model.User = user_db.query_by_id(int(userid))
        if user is None or user.is_delete:
            return {"message": "user not exist!"}, 400

        data = USER_SCHEMA.dump(user)
        return {"status": 200, "message": "ok", "data": data}

    # 更新用户信息
    elif request.method == "PUT":
        params: dict = request.get_json()
        if "password" in params.keys():
            if len(params.keys()) == 1:
                return api.update_password(userid)
            params.pop("password")

        if params:
            return api.update(userid, param_mapper=params)

    # 设置用户状态为delete
    elif request.method == "DELETE":
        return api.update(userid, {"is_delete": True})


class UsersAPI(object):

    def __init__(self):
        self.db = UsersDB()

    def update_password(self, userid: int):
        """更新用户密码"""
        password = request.json.get("password")
        if password is None:
            return {'message': 'Required param is missing'}, 400
        user: users_model.User = self.db.query_by_id(userid)
        if user is None or user.is_delete:
            return {"message": "user does not exist"}, 400
        entity, ok = self.db.update(
            userid, {"password": generate_password_hash(password)})
        if not ok:
            return {"status": 400, "message": "update password fail!"}
        data = USER_SCHEMA.dump(entity)
        return {"status": 200, "message": "success", "data": data}

    def update(self, userid: int, param_mapper=None):
        """ 更新用户信息; 如果param_mapper为None则从request.json中获取修改信息"""
        if not param_mapper or not isinstance(param_mapper, dict):
            param_mapper: dict = request.get_json()
        if not param_mapper:
            return {'message': 'Required param is missing'}, 400

        user: users_model.User = self.db.query_by_id(userid)
        if user is None:
            return {"message": "user does not exist"}, 400

        entity, ok = self.db.update(userid, param_mapper)
        if not ok:
            return {"status": 400, "message": "update fail!"}
        data = USER_SCHEMA.dump(entity)
        return {"status": 200, "message": "success", "data": data}

    def create_user(self):
        """创建新用户"""
        attributes = ["username", 'password', "phone", "real_name", "id_card"]
        _json = request.get_json()
        userinfo = {key: _json.get(key, None) for key in attributes}
        if not all(userinfo.values()):
            return {'message': 'Required param is missing'}, 400

        if not re.match(r"1[34578]\d{9}", userinfo["phone"]):
            return {"message": "无效的手机号!"}, 400
        if len(userinfo["id_card"]) != 18:
            return {"message": "身份证号必须为18位!"}, 400

        user = self.db.query_by_username(userinfo["username"])
        if user is not None:
            return {'message': 'user already exist!'}, 400

        user = self.db.query_by_phone(userinfo["phone"])
        if user is not None:
            return {'message': '手机号已被使用!'}, 400

        userinfo["password"] = generate_password_hash(userinfo.pop("password"))
        userinfo.update(avatar_url=_json.get("avatar_url", None))
        userinfo.update(is_delete=_json.get("is_delete", False))
        userinfo.update(is_admin=_json.get("is_admin", False))

        model = self.db.create(userinfo)
        data = USER_SCHEMA.dump(model)
        return {"status": 200, "message": "success", "data": data}
