from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from config import config
from app.database.connection import db
from app.utils.logger import setup_logging
from app.middleware.errors import register_error_handlers
from swagger_config import swagger_config, swagger_template
import logging

logger = logging.getLogger(__name__)


def create_app(config_name='development'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Validate configuration
    if not config[config_name].validate_config():
        logger.error("Configuration validation failed")
        raise ValueError("Invalid configuration. Check environment variables.")
    
    # Setup logging
    setup_logging(app)
    
    # Initialize CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Auto-add Bearer prefix for Swagger compatibility
    # This allows users to enter just the token without typing "Bearer "
    @app.before_request
    def fix_authorization_header():
        """Add Bearer prefix if missing (for Swagger UI compatibility)"""
        auth_header = request.headers.get('Authorization', '')
        if auth_header and not auth_header.startswith('Bearer ') and auth_header.startswith('eyJ'):
            request.environ['HTTP_AUTHORIZATION'] = f'Bearer {auth_header}'
    
    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'success': False,
            'message': 'Token has expired',
            'error': 'token_expired'
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'success': False,
            'message': 'Invalid token',
            'error': 'invalid_token'
        }), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            'success': False,
            'message': 'Missing authorization token',
            'error': 'authorization_required'
        }), 401
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'success': False,
            'message': 'Token has been revoked',
            'error': 'token_revoked'
        }), 401
    
    # Initialize Swagger/OpenAPI documentation
    swagger = Swagger(app, config=swagger_config, template=swagger_template)
    logger.info("Swagger documentation initialized")
    
    # Initialize database
    try:
        db.initialize(app.config['MONGO_URI'])
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise
    
    # Register blueprints
    from app.auth.routes import auth_bp
    from app.scam_detection.routes import scam_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(scam_bp)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Health check endpoint
    @app.route('/')
    def health_check():
        """
        Root endpoint - Health check
        ---
        tags:
          - Health
        responses:
          200:
            description: Service is running
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: true
                message:
                  type: string
                  example: SATI API is running
                version:
                  type: string
                  example: 1.0.0
        """
        return {
            'success': True,
            'message': 'SATI API is running',
            'version': '1.0.0'
        }
    
    @app.route('/api/v1/health')
    def api_health():
        """
        API health check
        ---
        tags:
          - Health
        responses:
          200:
            description: API health status
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: true
                message:
                  type: string
                  example: API is healthy
                database:
                  type: string
                  example: connected
        """
        return {
            'success': True,
            'message': 'API is healthy',
            'database': 'connected'
        }
    
    logger.info(f"Application created with config: {config_name}")
    
    return app
