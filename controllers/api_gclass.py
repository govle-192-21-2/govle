from controllers.gclass import GoogleClassroomClient
from flask import Blueprint, current_app, redirect, session, url_for
from flask_login import login_required, current_user
from json import dumps
from models.credentials import GoogleCredentials
from models.learning_env_class import LearningEnvClassEnc

gclass = Blueprint('gclass', __name__)

# Nice way to require login for entire blueprint
@gclass.before_request
@login_required
def gclass_before_request():
    # Check if user has Google credentials
    if len(current_user.google_accounts.keys()) == 0:
        # Redirect to Google account linking page
        return redirect(url_for('link_google.link_google_page'))


# Will run if tokens are updated
def on_token_refresh(google_credentials: GoogleCredentials):
    # Update credentials in DB
    db = current_app.config['DB']
    db.update_user_google_creds(current_user.user_id, google_credentials.user_id, google_credentials)


@gclass.route('/classes')
def gclass_classes():
    # Perform request for all linked accounts
    all_classes = {}
    for _, google_credentials in current_user.google_accounts.items():
        # Get list of classes from Google Classroom API
        client = GoogleClassroomClient(google_credentials, on_token_refresh)
        all_classes[google_credentials['email']] = client.get_classes()
    
    # The classes are returned as a list of GoogleClass dataclass instances,
    # so we need to serialize them to JSON.
    return dumps(all_classes, cls=LearningEnvClassEnc)
