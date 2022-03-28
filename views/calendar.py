from flask import Blueprint, render_template
from flask_login import login_required

calendar = Blueprint('calendar', __name__, template_folder='templates')

@calendar.route('/calendar')
@login_required
def calendar_page():
    return render_template('calendar.html', active_nav='calendar')
