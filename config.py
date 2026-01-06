import os
from dotenv import load_dotenv
import sys

load_dotenv()


class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/sati_api')
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 86400))  # 24 hours
    
    @staticmethod
    def validate_config():
        """Validate required configuration"""
        errors = []
        
        if not os.getenv('GOOGLE_API_KEY'):
            errors.append('GOOGLE_API_KEY environment variable is required')
        
        # Warn about default secrets in production
        if os.getenv('FLASK_ENV') == 'production':
            if os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production') == 'dev-secret-key-change-in-production':
                errors.append('SECRET_KEY must be set in production')
            if os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production') == 'jwt-secret-key-change-in-production':
                errors.append('JWT_SECRET_KEY must be set in production')
        
        if errors:
            print('\n'.join(['Configuration Error:'] + errors), file=sys.stderr)
            return False
        return True


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    MONGO_URI = os.getenv('MONGO_URI_TEST', 'mongodb://localhost:27017/sati_api_test')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
