from flask import Flask
from .api_gclass import gclass as gclass_api


def init_api(app: Flask):
    app.register_blueprint(gclass_api, url_prefix='/api/v1')
