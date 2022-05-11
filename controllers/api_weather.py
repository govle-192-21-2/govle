from flask import Blueprint
from flask_login import login_required

weather = Blueprint('weather', __name__)

# Require login before request
@login_required
@weather.before_request
def weather_before_request():
    pass


@weather.route('/weather')
def weather_route():
    # Get latitude and longitude from request data
    raise NotImplementedError('Weather not implemented yet')
