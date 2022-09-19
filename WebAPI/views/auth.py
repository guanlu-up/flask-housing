from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import jwt_required

from ..database.users import UsersDB

auth_view = Blueprint("auth", __name__, url_prefix="/api")


@auth_view.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    user = UsersDB().query_by_username(username)
    if user is None or not user.verify_password(password):
        return {"status": 401, "message": "Wrong username or password"}

    token_key = {"user_id": user.id, "username": user.username}
    access_token = create_access_token(
        token_key, additional_claims={"is_admin": user.is_admin})
    refresh_token = create_refresh_token(username)
    data = {
        "username": username,
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

    return {"status": 200, "message": data}


@auth_view.route("/logout", methods=["GET"])
@jwt_required()
def logout():
    return {"status": 200, "message": "ok"}
