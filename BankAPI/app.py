"""
Banking REST API - Flask Application
Main entry point for the Banking API
"""
from flask import Flask, jsonify
from flasgger import Flasgger
from data_store import DataStore
from routes import customers_bp, accounts_bp


def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Initialize Swagger/Flasgger
    Flasgger(app)
    
    # Initialize data store with seed data
    DataStore.initialize()
    
    # Register blueprints
    app.register_blueprint(customers_bp)
    app.register_blueprint(accounts_bp)
    
    # Root endpoint
    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
            'message': 'Banking REST API',
            'version': '1.0.0',
            'endpoints': {
                'customers': '/api/customers',
                'accounts': '/api/accounts'
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
    app.run(debug=True, host='0.0.0.0', port=5000)
