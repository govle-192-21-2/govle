from flask import Blueprint, render_template

login = Blueprint('login', __name__, template_folder='templates')

@login.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html', full_width='true')
