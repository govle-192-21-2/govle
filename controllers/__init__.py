from flask import Flask
from .api_gclass import gclass as gclass_api
from .api_moodle import moodle as moodle_api
from .api_settings import govle_settings as settings_api
from .api_weather import weather as weather_api


def init_api(app: Flask):
    app.register_blueprint(gclass_api, url_prefix='/api/v1/google')
    app.register_blueprint(moodle_api, url_prefix='/api/v1/moodle')
    app.register_blueprint(settings_api, url_prefix='/api/v1')
    app.register_blueprint(weather_api, url_prefix='/api/v1')
