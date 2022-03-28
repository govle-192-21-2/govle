from flask import Blueprint, render_template
from flask_login import login_required

classes = Blueprint('classes', __name__, template_folder='templates')

@classes.route('/classes')
@login_required
def classes_page():
    return render_template('classes.html', active_nav='classes')
