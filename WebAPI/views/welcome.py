from flask import Blueprint, redirect, url_for

welcome_view = Blueprint("welcome", __name__, url_prefix="/api")


@welcome_view.route("", methods=["GET"])
def helloworld():

    return {"satus": 200, "message": "hello 欢迎访问HomeApp的API"}


@welcome_view.route("/welcome", methods=["GET"])
def welcome_api():
    return redirect(url_for("welcome.helloworld"))
