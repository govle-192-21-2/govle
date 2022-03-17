from flask import Blueprint, render_template
from flask_login import login_required

link_moodle = Blueprint('link-moodle', __name__, template_folder='templates')

@link_moodle.route('/link-uvle', methods=['GET'])
@login_required
def link_moodle_page():
    return render_template('login-uvle.html')
