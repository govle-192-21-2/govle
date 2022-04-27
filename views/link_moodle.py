import base64
from cryptography.hazmat.primitives.asymmetric import padding
from flask import Blueprint, current_app, render_template, request
from flask_login import login_required
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
        return "No credentials supplied", 400

    # Decrypt credentials (encoded as base64)
    cipher = current_app.config['RSA_CIPHER']
    decoded_credentials = base64.b64decode(encrypted_credentials)
    decrypted_credentials = cipher.decrypt(decoded_credentials, padding.PKCS1v15()).decode('utf-8')
    uvle_username, uvle_password = decrypted_credentials.split(':')

    # Attempt to get token from Moodle
    moodle_domain = environ['MOODLE_DOMAIN']
    moodle_token_url = f'https://{moodle_domain}/login/token.php'
    moodle_token_data = {
        'username': uvle_username,
        'password': uvle_password,
        'service': 'moodle_mobile_app'
    }
    moodle_token_response = get(moodle_token_url, params=moodle_token_data).json()
    if 'token' not in moodle_token_response or len(moodle_token_response['token']) < 32:
        return '{"success": false, "reason": "Invalid credentials"}', 400
    
    # TODO: Store token in database
    db = current_app.config['DB']

    return '{"success": true}'
