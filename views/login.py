from flask import Blueprint, render_template, request
from google.auth.transport import requests
from google.oauth2 import id_token
from os import environ

login = Blueprint('login', __name__, template_folder='templates')

@login.route('/login', methods=['GET'])
def login_page():
    if not 'DOMAIN' in environ:
        raise RuntimeError('DOMAIN environment variable not set')
    if not 'GOOGLE_CLIENT_ID' in environ:
        raise RuntimeError('GOOGLE_CLIENT_ID environment variable not set')
    return render_template(
        'login.html',
        full_width='true',
        domain=environ['DOMAIN'],
        google_client_id=environ['GOOGLE_CLIENT_ID']
    )

@login.route('/login', methods=['POST'])
def login_form():
    # If the POSTed form data has the "g_csrf_token" field,
    # then we assume the login was with a Google account
    # and the form data contains a JWT token we should verify.
    if 'g_csrf_token' in request.form:
        # First check if the CSRF token checks out...
        csrf_cookie = request.cookies.get('g_csrf_token')
        if not csrf_cookie:
            return 'CSRF token missing', 400
        if csrf_cookie != request.form['g_csrf_token']:
            return 'CSRF token mismatch', 400

        # ...then decode the JWT using Google's library
        try:
            id_info = id_token.verify_oauth2_token(
                request.form['credential'],
                requests.Request(),
                environ['GOOGLE_CLIENT_ID']
            )
        except Exception as e:
            # Could not decode JWT
            return f'Invalid JWT: {str(e)}', 400
        else:
            # Decoded JWT successfully
            return 'OK'

    return 'OK'
