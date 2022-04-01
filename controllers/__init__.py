from flask import Flask
from .api_gclass import gclass as gclass_api
from .api_settings import govle_settings as settings_api


def init_api(app: Flask):
    app.register_blueprint(gclass_api, url_prefix='/api/v1')
    app.register_blueprint(settings_api, url_prefix='/api/v1')
