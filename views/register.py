from flask import Blueprint

register = Blueprint('register', __name__, template_folder='templates')

@register.route('/register', methods=['GET'])
def register_page():
    return 'register page'
