from flask import Flask, render_template
import logging
from routes.favorites import favorites_bp
from routes.media import media_bp
from routes.api import api_bp
from routes.main import main_bp

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Register blueprints
app.register_blueprint(favorites_bp)
app.register_blueprint(media_bp)
app.register_blueprint(api_bp)
app.register_blueprint(main_bp)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
