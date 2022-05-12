from flask import Blueprint, current_app, request
from flask_login import login_required
from json import dumps
from requests import get
from typing import Tuple

weather = Blueprint('weather', __name__)

# Mappings for OpenMeteo WMO codes and weather-icons glyphs
weather_codes = {
    '0': ('Clear', 'day-sunny', 'night-clear'),
    '1': ('Mostly clear', 'day-cloudy', 'night-alt-cloudy'),
    '2': ('Partly cloudy', 'day-cloudy', 'night-partly-cloudy'),
    '3': ('Overcast', 'cloudy', 'cloudy'),
    '45': ('Fog', 'fog', 'night-fog'),
    '48': ('Freezing fog', 'fog', 'night-fog'),
    '51': ('Light drizzle', 'day-sprinkle', 'night-sprinkle'),
    '53': ('Moderate drizzle', 'day-sprinkle', 'night-sprinkle'),
    '55': ('Dense drizzle', 'day-sprinkle', 'night-sprinkle'),
    '56': ('Light freezing drizzle', 'day-rain-mix', 'night-rain-mix'),
    '57': ('Dense freezing drizzle', 'day-rain-mix', 'night-rain-mix'),
    '61': ('Light rain', 'day-showers', 'night-showers'),
    '63': ('Moderate rain', 'day-showers', 'night-showers'),
    '65': ('Heavy rain', 'day-showers', 'night-showers'),
    '66': ('Light freezing rain', 'day-sleet', 'night-sleet'),
    '67': ('Heavy freezing rain', 'day-sleet', 'night-sleet'),
    '71': ('Light snow', 'day-snow', 'night-snow'),
    '73': ('Moderate snow', 'day-snow', 'night-snow'),
    '75': ('Heavy snow', 'day-snow', 'night-snow'),
    '77': ('Snow grains', 'day-snow', 'night-snow'),
    '80': ('Light rain showers', 'day-rain', 'night-rain'),
    '81': ('Moderate rain showers', 'day-rain', 'night-rain'),
    '82': ('Violent rain showers', 'day-rain', 'night-rain'),
    '85': ('Light snow showers', 'day-snow', 'night-snow'),
    '86': ('Heavy snow showers', 'day-snow', 'night-snow'),
    '95': ('Thunderstorm', 'day-thunderstorm', 'night-thunderstorm'),
    '96': ('Thunderstorm with slight hail', 'day-sleet-storm', 'night-sleet-storm'),
    '99': ('Thunderstorm with heavy hail', 'day-sleet-storm', 'night-sleet-storm'),
}

# Require login before request
@login_required
@weather.before_request
def weather_before_request():
    pass


@weather.route('/weather')
def weather_route():
    # Return dummy data if running in development mode
    if current_app.config['DEBUG'] or 'X-Forwarded-For' not in request.headers:
        return dumps({
            'condition': 'Clear',
            'icon': 'day-sunny',
            'temperature': '-10',
            'place': 'London (dummy data)',
            'feels_like': '-9'
        })

    # Get user IP address and time of day
    ip_address_list = request.headers.getlist('X-Forwarded-For')
    ip_address = ip_address_list[0].split(',')[0]
    time_of_day = request.args.get('timeOfDay')
    icon_index = 1 if time_of_day == 'day' else 2

    # Geolocate IP address
    geo_response = get(f'http://ip-api.com/json/{ip_address}')
    geo_data = geo_response.json()
    lat = geo_data['lat']
    lon = geo_data['lon']
    region_name = geo_data['regionName']

    # Get weather for IP address geolocation
    weather_response = get(f'https://api.open-meteo.com/v1/forecast', params={
        'latitude': lat,
        'longitude': lon,
        'current_weather': 'true',
        'hourly': 'apparent_temperature'
    })
    weather_data = weather_response.json()

    # Was there an error?
    if 'error' in weather_data.keys() and weather_data['error']:
        return dumps({
            'condition': 'Unknown',
            'icon': 'cloud',
            'place': 'Unknown',
            'temperature': 'Unknown',
            'feels_like': 'Unknown'
        })

    # Get apparent temperature for current hour
    current_hour = weather_data['current_weather']['time']
    apparent_temp_index = weather_data['hourly']['time'].index(current_hour)
    apparent_temp = weather_data['hourly']['apparent_temperature'][apparent_temp_index]

    # Return data with appropriate condition and icon name
    mapped_condition = weather_codes[str(weather_data['current_weather']['weathercode'])]
    return dumps({
        'condition': mapped_condition[0],
        'icon': mapped_condition[icon_index],
        'place': region_name,
        'temperature': weather_data['current_weather']['temperature'],
        'feels_like': apparent_temp
    })

