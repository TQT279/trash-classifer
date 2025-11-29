import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .config import config
from .models import db
from .routes.auth_routes import auth_bp
from .routes.classification_routes import classification_bp
from .routes.feedback_routes import feedback_bp
from .routes.user_routes import user_bp
from dotenv import load_dotenv


def create_app(config_name=None):
    """Create and configure Flask application"""
    
    # Load environment variables from .env file
    load_dotenv()
    
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.environ.get('FLASK_ENV', 'default')
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Initialize CORS
    CORS(app, origins=app.config.get('CORS_ORIGINS', ['*']))
    
    # Create upload folder if it doesn't exist
    upload_folder = app.config.get('UPLOAD_FOLDER', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(classification_bp)
    app.register_blueprint(feedback_bp)
    app.register_blueprint(user_bp)
    
    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': {
                'message': 'Bad request',
                'code': 400
            }
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': {
                'message': 'Unauthorized',
                'code': 401
            }
        }), 401
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': {
                'message': 'Resource not found',
                'code': 404
            }
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': {
                'message': 'Internal server error',
                'code': 500
            }
        }), 500
    
    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'success': False,
            'error': {
                'message': 'Token has expired',
                'code': 'TOKEN_EXPIRED'
            }
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'success': False,
            'error': {
                'message': 'Invalid token',
                'code': 'INVALID_TOKEN'
            }
        }), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            'success': False,
            'error': {
                'message': 'Authorization token is missing',
                'code': 'MISSING_TOKEN'
            }
        }), 401
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'success': True,
            'message': 'API is running',
            'status': 'healthy'
        }), 200
    
    # Root endpoint
    @app.route('/', methods=['GET'])
    def root():
        return jsonify({
            'success': True,
            'message': 'Waste Classification API',
            'version': '1.0.0'
        }), 200
    
    return app


def init_db(app):
    """Initialize database tables"""
    with app.app_context():
        db.create_all()
        app.logger.info("Database tables created")


if __name__ == '__main__':
    app = create_app()
    
    # Initialize database (uncomment if you want to create tables on startup)
    # init_db(app)
    
    # Run the application
    app.run(
        host=os.environ.get('FLASK_HOST', '0.0.0.0'),
        port=int(os.environ.get('FLASK_PORT', 5000)),
        debug=app.config.get('DEBUG', False)
    )

