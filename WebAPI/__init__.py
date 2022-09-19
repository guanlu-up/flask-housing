from flask import Flask

from .views import init_views
from .config import ENVIRON_MAPPER
from .extension import extension_register


def create_app(run_model="development"):
    if run_model not in ENVIRON_MAPPER.keys():
        raise KeyError(f"invalid params (run_model): {run_model}")
    _app = Flask(__name__)
    _app.config.from_object(ENVIRON_MAPPER.get(run_model))
    init_views(_app)
    extension_register(_app)

    return _app
