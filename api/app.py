from flask import Flask, jsonify
from routes import register_routes
from db import close_db_connection
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from log_config import setup_logging  # Import the logging setup

# Initialize logging
setup_logging()

app = Flask(__name__)

# Configure cache
app.config['CACHE_TYPE'] = 'simple'  # Simple cache, in-memory
cache = Cache(app)

# Set up rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per minute"]  # Set a global limit of 5 requests per minute
)

# Register all routes
register_routes(app, cache, limiter)

# Ensure the database connection is closed when the application context ends
@app.teardown_appcontext
def close_connection(exception):
    close_db_connection()

# Error handler for 404 Not Found
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Not Found", "message": "The requested resource was not found."}), 404

# Error handler for 429 Too Many Requests
@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        "error": "Too Many Requests",
        "message": "You have exceeded your request limit. Please try again later."
    }), 429

if __name__ == '__main__':
    app.run(debug=True)
