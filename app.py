# Main application file for GoVLê
from flask import Flask
from views import *

app = Flask(__name__)

# Routes
app.register_blueprint(index_blueprint)
app.register_blueprint(login_blueprint)

# Run app
if __name__ == '__main__':
    app.run(debug=True)
