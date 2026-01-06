from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.database.connection import get_database
from app.database.repositories import UserRepository
import logging

logger = logging.getLogger(__name__)


def token_required(f):
    """Middleware to verify JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return f(*args, **kwargs)
        except Exception as e:
            logger.warning(f"Token verification failed: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Invalid or expired token'
            }), 401
    return decorated


def get_current_user():
    """Get current authenticated user"""
    try:
        user_id = get_jwt_identity()
        db = get_database()
        user_repo = UserRepository(db)
        return user_repo.find_by_id(user_id)
    except Exception as e:
        logger.error(f"Failed to get current user: {str(e)}")
        return None
