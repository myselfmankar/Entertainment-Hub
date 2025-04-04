from flask import Flask, render_template
import logging
from firebase_util import initialize_firebase
from routes.favorites import favorites_bp
from routes.media import media_bp
from routes.api import api_bp
from routes.main import main_bp
from routes.auth import auth_bp
from config import FIREBASE_CONFIG

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key
app.config['FIREBASE_CONFIG'] = FIREBASE_CONFIG

# Initialize Firebase
initialize_firebase()

# Register blueprints
app.register_blueprint(favorites_bp)
app.register_blueprint(media_bp)
app.register_blueprint(api_bp)
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
