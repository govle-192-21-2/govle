import base64
from cryptography.hazmat.primitives.asymmetric import padding
from flask import Blueprint, current_app, render_template, request
from flask_login import current_user, login_required
from models.credentials import MoodleCredentials
from os import environ
from requests import get

link_moodle = Blueprint('link-moodle', __name__, template_folder='templates')

@link_moodle.route('/link-uvle', methods=['GET'])
@login_required
def link_moodle_page():
    return render_template('login-uvle.html')

@link_moodle.route('/link-uvle', methods=['POST'])
@login_required
def link_moodle_post():
    # Get credentials from request JSON data
    encrypted_credentials = request.json['credentials']
    if encrypted_credentials is None:
        return '{"success": false, "error": "No credentials specified"}', 400

    # Decrypt credentials (encoded as base64)
    cipher = current_app.config['RSA_CIPHER']
    decoded_credentials = base64.b64decode(encrypted_credentials)
    decrypted_credentials = cipher.decrypt(decoded_credentials, padding.PKCS1v15()).decode('utf-8')
    credentials = decrypted_credentials.split(':')
    if len(credentials) != 2:
        return '{"success": false, "error": "Invalid credentials"}', 400

    # Attempt to get token from Moodle
    uvle_username, uvle_password = credentials
    moodle_domain = environ['MOODLE_DOMAIN']
    moodle_token_url = f'https://{moodle_domain}/login/token.php'
    moodle_token_data = {
        'username': uvle_username,
        'password': uvle_password,
        'service': 'moodle_mobile_app'
    }
    moodle_token_response = get(moodle_token_url, params=moodle_token_data).json()
    if 'token' not in moodle_token_response or len(moodle_token_response['token']) < 32:
        return '{"success": false, "error": "Invalid credentials"}', 400
    
    # Store token in database
    creds = MoodleCredentials(
        username=uvle_username,
        password=moodle_token_response['token'],
        server=moodle_domain
    )
    db = current_app.config['DB']
    db.update_user_moodle_creds(current_user.user_id, creds)

    return '{"success": true}'
