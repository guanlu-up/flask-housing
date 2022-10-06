from flask import Blueprint
from flask import request


house_view = Blueprint("house", __name__, url_prefix="/api/house")


