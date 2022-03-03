from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

index = Blueprint('index', __name__, template_folder='templates')

@index.route('/', methods=['GET'])
def index_page():
    # Redirect to dashboard if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard_page'))
    return render_template('homepage.html', full_width='true')
