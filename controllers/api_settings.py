from flask import Blueprint
from flask_login import login_required, current_user
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