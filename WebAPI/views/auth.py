import re

from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import jwt_required

from ..database.users import UsersDB
from ..extension import redis

auth_view = Blueprint("auth", __name__, url_prefix="/api")


@auth_view.route("/login", methods=["POST"])
def login():
    phone = request.json.get("phone", None)
    password = request.json.get("password", None)
    if phone is None or password is None:
        return {"message": "Required param is missing"}, 400

    if not re.match(r"1[34578]\d{9}", phone):
        return {"message": "手机号格式不正确!"}, 400
    retry_times = redis.get(f"login_retry_{phone}")
    if retry_times is not None and int(retry_times) > 5:
        return {"message": "重试次数过多,请稍后再试!"}, 400

    user_db = UsersDB()
    user = user_db.query_by_phone(phone)
    if user is None or user.is_delete is True or not user.verify_password(password):
        if retry_times is None:
            retry_times = 0
        redis.setex(f"login_retry_{phone}", (60 * 5), int(retry_times) + 1)
        return {"message": "手机号或密码错误!"}, 400
    if retry_times:
        redis.move(f"login_retry_{phone}", 1)

    token_key = {"userid": user.id, "phone": user.phone}
    access_token = create_access_token(
        token_key, additional_claims={"is_admin": user.is_admin})
    refresh_token = create_refresh_token(phone)
    data = {
        "username": user.username,
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
    return {"status": 200, "message": "success", "data": data}


@auth_view.route("/logout", methods=["GET"])
@jwt_required()
def logout():
    return {"status": 200, "message": "ok"}
