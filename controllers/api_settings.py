from flask import Blueprint, current_app, request
from flask_login import login_required, current_user, logout_user
from hashlib import md5
from json import dumps

govle_settings = Blueprint('govle_settings', __name__)

# Nice way to require login for entire blueprint
@govle_settings.before_request
@login_required
def govle_settings_before_request():
    pass


@govle_settings.route('/accounts')
def govle_settings_accounts():
    accounts = {
        'google': [],
        'moodle': None
    }

    # Check if user has Moodle linked
    if current_user.moodle_account.password != '':
        accounts['moodle'] = {
            'username': current_user.moodle_account.username,
            'server': current_user.moodle_account.server
        }

    # Get list of Google accounts
    for _, google_credentials in current_user.google_accounts.items():
        # Hash e-mail address for Gravatar URL
        gravatar_hash = md5(google_credentials['email'].lower().encode('utf-8')).hexdigest()

        accounts['google'].append({
            'email': google_credentials['email'],
            'gravatar': f'https://www.gravatar.com/avatar/{gravatar_hash}?s=200',
            'id': google_credentials['user_id']
        })
    
    # Return as JSON
    return dumps(accounts)


@govle_settings.route('/settings/unlink', methods=['POST'])
@login_required
def unlink_page():
    # Get account type from query string
    account_type = request.json['type']
    if account_type == 'google':
        # Get Google account ID to unlink
        account_id = request.json['id']
        if account_id not in current_user.google_accounts:
            return '{"success": false, "error": "No such linked Google account"}', 404

        # Delete from database
        db = current_app.config['DB']
        db.delete_user_google_creds(current_user.user_id, account_id)

        return f'"success": true, "type": "google", "id": {account_id}', 200
    elif account_type == 'moodle':
        # Delete from database
        db = current_app.config['DB']
        db.delete_user_moodle_creds(current_user.user_id)

        return '{"success": true, "type": "moodle"}', 200
    
    return '{"success": false, "error": "Unknown account type"}', 400

@govle_settings.route('/settings/delete_account', methods=['POST'])
@login_required
def delete_account_page():
    # Delete user from database
    db = current_app.config['DB']
    db.delete_user(current_user.user_id)

    # Logout
    logout_user()
    return '{"success": true}', 200
