from flask import Flask
from .calendar import calendar as calendar_blueprint
from .classes import classes as classes_blueprint
from .dashboard import dashboard as dashboard_blueprint
from .index import index as index_blueprint
from .link_google import link_google as link_google_blueprint
from .link_moodle import link_moodle as link_moodle_blueprint
from .login import login as login_blueprint
from .logout import logout as logout_blueprint
from .settings import settings as settings_blueprint


def init_views(app: Flask):
    app.register_blueprint(calendar_blueprint)
    app.register_blueprint(classes_blueprint)
    app.register_blueprint(dashboard_blueprint)
    app.register_blueprint(index_blueprint)
    app.register_blueprint(link_google_blueprint)
    app.register_blueprint(link_moodle_blueprint)
    app.register_blueprint(login_blueprint)
    app.register_blueprint(logout_blueprint)
    app.register_blueprint(settings_blueprint)
