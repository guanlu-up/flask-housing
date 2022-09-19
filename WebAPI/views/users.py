from flask import Blueprint
from flask import request
from werkzeug.security import generate_password_hash

from ..models import users as users_model
from ..database.users import UsersDB

users_view = Blueprint("users", __name__, url_prefix="/users")


@users_view.route("", methods=["GET", "POST"])
def add_user():
    api = UsersAPI()
    if request.method == "GET":
        return api.get_user()
    if request.method == "POST":
        return api.create_user()


@users_view.route("/<int:user_id>", methods=["PUT", "DELETE"])
def user_update(user_id):
    api = UsersAPI()
    if request.method == "PUT":
        if "password" in request.json.keys():
            return api.update_password(user_id)
        return api.update(user_id)
    if request.method == "DELETE":
        return api.delete_user(user_id)


class UsersAPI(object):

    def __init__(self):
        self.db = UsersDB()

    def update_password(self, user_id: int):
        """更新用户密码"""
        password = request.json.get("password")
        if password is None:
            return {'message': 'Required param is missing'}, 400
        user: users_model.User = self.db.query_by_id(user_id)
        if user is None:
            return {"message": "user_id invalid"}, 400
        entity, ok = self.db.update(
            user_id, {"password": generate_password_hash(password)})
        if not ok:
            return {"status": 400, "message": "update fail"}

        return {"status": 200, "message": "success"}

    def update(self, user_id: int):
        user: users_model.User = self.db.query_by_id(user_id)
        if user is None:
            return {"message": "user_id invalid"}, 400
        param_mapper: dict = request.get_json()
        if param_mapper:
            entity, ok = self.db.update(user_id, param_mapper)
            if not ok:
                return {"status": 400, "message": "update fail"}
        return {"status": 200, "message": "success"}

    def get_user(self):
        """获取用户信息"""
        _id = request.args.get("id")
        if _id is None or not str(_id).isdigit():
            return {'message': 'Required param is missing'}, 400

        user: users_model.User = self.db.query_by_id(int(_id))
        if user is None:
            return {"message": "user not exist!"}, 400
        userinfo = {
            "username": user.username,
            "password": user.password,
            "is_admin": user.is_admin,
        }
        return {"status": 200, "message": userinfo}

    def create_user(self):
        """创建新用户"""
        username = request.json.get("username")
        password = request.json.get("password")
        is_admin = request.json.get("is_admin")
        if username is None or password is None or is_admin is None:
            return {'message': 'Required param is missing'}, 400

        user = self.db.query_by_username(username)
        if user is not None:
            return {'message': 'user already exist!'}, 400

        self.db.create({
            "username": username,
            "password": generate_password_hash(password),
            "is_admin": is_admin,
        })
        return {"status": 200, "message": "success"}

    def delete_user(self, user_id: int):
        """删除用户"""
        ok = self.db.delete(user_id)
        if not ok:
            return {"message": "delete fail!"}, 400
        return {"status": 200, "message": "success"}
