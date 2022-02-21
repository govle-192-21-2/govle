from flask import Blueprint, current_app, render_template, request, redirect, url_for
from flask_login import login_user
from google.auth.transport import requests
from google.oauth2 import id_token
from os import environ
from urllib.parse import urljoin, urlparse

login = Blueprint('login', __name__, template_folder='templates')

# https://stackoverflow.com/a/61446498
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

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
            print(id_info)
            return 'OK'
    
    # No JWT data, so decode good old email address and password
    email = request.form['username']
    password = request.form['password']

    # Does this user exist?
    db = current_app.config['DB']
    matching_user = db.lookup_user_by_email(email)
    if not matching_user:
        return 'No such user', 400
    
    # Does the password match?
    if not matching_user.verify_password(password):
        return 'Invalid password', 400
    
    # User exists and password is correct, so log in!
    login_user(matching_user)

    # Redirect to the next page
    next_url = request.args.get('next')
    if not is_safe_url(next_url):
        return 'Unsafe redirect URL', 400
    return redirect(next_url or url_for('index.index_page'))
