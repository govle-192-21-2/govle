from flask import Blueprint, render_template, request, session
from flask_login import current_user, login_required

dashboard = Blueprint('dashboard', __name__, template_folder='templates')

@dashboard.route('/dashboard')
@login_required
def dashboard_page():
    # Check if the user is new via session
    if 'IS_NEW_USER' in session and session['IS_NEW_USER'] == 'True':
        # User is new, show new user dashboard
        return render_template('dashboard-new-user.html', active_nav='home')

    # Does the current user have complete linked accounts?
    incomplete_moodle = current_user.moodle_account.password == ''
    current_user_google = current_user.google_accounts
    incomplete_google = len(current_user_google.keys()) == 0

    # Check if we are returning from account linking process
    if 'link_type' in session:
        # User is returning from account linking process
        link_type = session['link_type']
        link_status = session['link_status']
        del session['link_type']
        del session['link_status']
        return render_template('dashboard.html',
                               active_nav='home',
                               link_type=link_type,
                               link_status=link_status,
                               incomplete_google=incomplete_google,
                               incomplete_moodle=incomplete_moodle)

    # User is returning, show normal dashboard
    return render_template('dashboard.html',
                           active_nav='home',
                           incomplete_google=incomplete_google,
                           incomplete_moodle=incomplete_moodle)
