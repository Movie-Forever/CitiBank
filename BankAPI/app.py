"""
Banking REST API - Flask Application
Main entry point for the Banking API with MongoDB Integration
"""
import os

from flask import Flask, jsonify
from flasgger import Flasgger
from flask_cors import CORS
from data_store import DataStore
from routes import customers_bp, accounts_bp


def get_allowed_origins():
    """Read allowed CORS origins from ALLOWED_ORIGINS."""
    origins = os.getenv('ALLOWED_ORIGINS', '').strip()
    if origins:
        return [origin.strip() for origin in origins.split(',') if origin.strip()]

    if os.getenv('FLASK_ENV') == 'production':
        raise ValueError("ALLOWED_ORIGINS must be set in production")

    return '*'


def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Enable CORS for the configured frontend domains.
    CORS(app, resources={
        r"/api/*": {
            "origins": get_allowed_origins(),
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
    
    # Initialize Swagger/Flasgger
    Flasgger(app)
    
    # Initialize MongoDB data store with seed data
    try:
        DataStore.initialize()
    except Exception as e:
        print(f"Error initializing MongoDB: {e}")
        if os.getenv('FLASK_ENV') == 'production':
            raise
        return None
    
    # Register blueprints
    app.register_blueprint(customers_bp)
    app.register_blueprint(accounts_bp)
    
    # Root endpoint
    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
            'message': 'Banking REST API',
            'version': '1.0.0',
            'database': 'MongoDB Atlas',
            'endpoints': {
                'customers': '/api/customers',
                'accounts': '/api/accounts',
                'api_docs': '/apidocs'
            }
        }), 200
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({'status': 'healthy'}), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({'error': 'Method not allowed'}), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app


if __name__ == '__main__':
    app = create_app()
    if app:
        debug = os.getenv('FLASK_ENV') != 'production'
        port = int(os.getenv('PORT', '5000'))
        app.run(debug=debug, host='0.0.0.0', port=port)
    else:
        print("Failed to create app due to database connection error")
