from flask import Blueprint
from flask_login import login_required, current_user

gclass = Blueprint('gclass', __name__)

# Nice way to require login for entire blueprint
@gclass.before_request
@login_required
def gclass_before_request():
    pass

@gclass.route('/classes')
def gclass_classes():
    return 'test'
