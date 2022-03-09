from flask import Blueprint, current_app, redirect, request, session, url_for
from flask_login import current_user, login_required
from models.credentials import GoogleCredentials
import google_auth_oauthlib.flow

link_google = Blueprint('link-google', __name__, template_folder='templates')

# Google OAuth2 scopes
scopes = [
    'https://www.googleapis.com/auth/classroom.announcements.readonly',
    'https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/classroom.student-submissions.me.readonly',
    'https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly',
    'https://www.googleapis.com/auth/classroom.topics.readonly'
]

@link_google.route('/link-google')
@login_required
def link_google_page():
    # Clear link type and status from session
    session.pop('link_type', None)
    session.pop('link_status', None)

    # Create login flow
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json', scopes=scopes)
    flow.redirect_uri = url_for('link-google.link_google_callback', _external=True)

    # Generate authorization URL for redirection to Google
    # We could optionally include the include_granted_scopes param which will allow the user
    # to select which scopes to grant access to the application, however GoVLê's functionality
    # heavily depends on all the above scopes and will thus not work without them.
    authorization_url, state = flow.authorization_url(
        # Enable offline access, so we can refresh the token without re-authenticating
        access_type='offline'
    )

    # Store state in session for later validation
    session['google_auth_state'] = state

    # Redirect to Google for authorization
    return redirect(authorization_url)


@link_google.route('/link-google/callback')
def link_google_callback():
    # Retrieve state from session
    state = session.get('google_auth_state', None)

    # Store link type for dashboard use
    session['link_type'] = 'google'

    # If state is None, the user is not coming from Google, so redirect to home
    if state is None:
        return redirect(url_for('index.index_page'))

    # Create flow with state
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json', scopes=scopes, state=state)
    flow.redirect_uri = url_for('link-google.link_google_callback', _external=True)

    # Fetch OAuth 2.0 credentials using the authorization code
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Check if a refresh token is present
    credentials = flow.credentials
    if not credentials.refresh_token:
        # No refresh token means the user has already authenticated with Google once.
        # Tell them to revoke access and try again.
        session['link_status'] = 'failure'
        return redirect(url_for('dashboard.dashboard_page'))

    # Save credentials to database
    db = current_app.config['DB']
    google_credentials = GoogleCredentials(
        access_token=credentials.token,
        refresh_token=credentials.refresh_token,
        token_uri=credentials.token_uri,
        client_id=credentials.client_id,
        client_secret=credentials.client_secret,
        scopes=credentials.scopes,
        id_token=credentials.id_token
    )
    db.update_user_google_creds(current_user.user_id, google_credentials)

    # Save credentials to session and redirect to dashboard
    session['google_credentials'] = google_credentials
    session['link_status'] = 'success'
    return redirect(url_for('dashboard.dashboard_page'))
