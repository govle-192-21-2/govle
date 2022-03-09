from flask import Blueprint, render_template, session
from flask_login import login_required

dashboard = Blueprint('dashboard', __name__, template_folder='templates')

@dashboard.route('/dashboard')
@login_required
def dashboard_page():
    # Check if the user is new via session
    if 'new_user' in session and session['new_user'] == 'True':
        # User is new, show new user dashboard
        return render_template('dashboard-new-user.html', active_nav='home')

    # User is returning, show normal dashboard
    return render_template('dashboard.html', active_nav='home')
