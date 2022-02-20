# Main application file for GoVLê
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from os import environ
from views import *

# Environment variables
load_dotenv()

# Flask app
app = Flask(__name__)

# Authentication
if not 'FLASK_SECRET_KEY' in environ:
    raise RuntimeError('FLASK_SECRET_KEY environment variable not set')
app.secret_key = environ['FLASK_SECRET_KEY']
login_manager = LoginManager()
login_manager.init_app(app)

# Routes
app.register_blueprint(index_blueprint)
app.register_blueprint(login_blueprint)

# Run app
if __name__ == '__main__':
    app.run(debug=True)
