from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flasgger import swag_from
from app.database.connection import get_database
from app.database.repositories import UserRepository
from app.auth.models import User
from app.utils.helpers import sanitize_input
from app.middleware.rate_limit import rate_limit
import logging

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


@auth_bp.route('/register', methods=['POST'])
@rate_limit(max_requests=3, window_seconds=300)  # 3 registrations per 5 minutes
def register():
    """
    Register a new user
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        description: User registration data
        required: true
        schema:
          type: object
          required:
            - email
            - password
            - name
          properties:
            email:
              type: string
              format: email
              example: user@example.com
              description: User email address (must be unique)
            password:
              type: string
              format: password
              minLength: 6
              example: password123
              description: User password (minimum 6 characters)
            name:
              type: string
              example: John Doe
              description: User's full name
    responses:
      201:
        description: User registered successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: User registered successfully
            access_token:
              type: string
              example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
              description: JWT access token for authentication
            user:
              type: object
              properties:
                id:
                  type: string
                  example: 507f1f77bcf86cd799439011
                email:
                  type: string
                  example: user@example.com
                name:
                  type: string
                  example: John Doe
      400:
        description: Validation error
        schema:
          $ref: '#/definitions/ValidationError'
      409:
        description: Email already registered
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: Email already registered
      500:
        description: Server error
        schema:
          $ref: '#/definitions/Error'
    """
    try:
        data = request.get_json()
        
        # Sanitize inputs
        if data.get('email'):
            data['email'] = sanitize_input(data['email']).lower()
        if data.get('name'):
            data['name'] = sanitize_input(data['name'])
        
        # Validate input
        errors = User.validate_registration(data)
        if errors:
            return jsonify({
                'success': False,
                'errors': errors
            }), 400
        
        # Check if user already exists
        db = get_database()
        user_repo = UserRepository(db)
        
        existing_user = user_repo.find_by_email(data['email'])
        if existing_user:
            return jsonify({
                'success': False,
                'message': 'Email already registered'
            }), 409
        
        # Create user
        user_id = user_repo.create_user(
            email=data['email'],
            password=data['password'],
            name=data['name']
        )
        
        # Create access token
        access_token = create_access_token(identity=user_id)
        
        logger.info(f"New user registered: {data['email']}")
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'access_token': access_token,
            'user': {
                'id': user_id,
                'email': data['email'],
                'name': data['name']
            }
        }), 201
        
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Registration failed',
            'error': str(e)
        }), 500


@auth_bp.route('/login', methods=['POST'])
@rate_limit(max_requests=5, window_seconds=60)  # 5 login attempts per minute
def login():
    """
    Login user
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        description: User login credentials
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              format: email
              example: user@example.com
              description: User email address
            password:
              type: string
              format: password
              example: password123
              description: User password
    responses:
      200:
        description: Login successful
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Login successful
            access_token:
              type: string
              example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
              description: JWT access token for authentication
            user:
              type: object
              properties:
                id:
                  type: string
                  example: 507f1f77bcf86cd799439011
                email:
                  type: string
                  example: user@example.com
                name:
                  type: string
                  example: John Doe
                created_at:
                  type: string
                  format: date-time
                  example: 2024-01-06T10:30:00
      400:
        description: Validation error
        schema:
          $ref: '#/definitions/ValidationError'
      401:
        description: Invalid credentials
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: Invalid email or password
      500:
        description: Server error
        schema:
          $ref: '#/definitions/Error'
    """
    try:
        data = request.get_json()
        
        # Sanitize inputs
        if data.get('email'):
            data['email'] = sanitize_input(data['email']).lower()
        
        # Validate input
        errors = User.validate_login(data)
        if errors:
            return jsonify({
                'success': False,
                'errors': errors
            }), 400
        
        # Find user
        db = get_database()
        user_repo = UserRepository(db)
        
        user = user_repo.find_by_email(data['email'])
        if not user:
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401
        
        # Verify password
        if not user_repo.verify_password(user, data['password']):
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401
        
        # Create access token
        access_token = create_access_token(identity=str(user['_id']))
        
        logger.info(f"User logged in: {data['email']}")
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'access_token': access_token,
            'user': User.to_dict(user)
        }), 200
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Login failed',
            'error': str(e)
        }), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current user information
    ---
    tags:
      - Authentication
    security:
      - BearerAuth: []
    responses:
      200:
        description: Current user information
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            user:
              type: object
              properties:
                id:
                  type: string
                  example: 507f1f77bcf86cd799439011
                email:
                  type: string
                  example: user@example.com
                name:
                  type: string
                  example: John Doe
                created_at:
                  type: string
                  format: date-time
                  example: 2024-01-06T10:30:00
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: Invalid or expired token
      404:
        description: User not found
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: User not found
      500:
        description: Server error
        schema:
          $ref: '#/definitions/Error'
    """
    try:
        user_id = get_jwt_identity()
        
        db = get_database()
        user_repo = UserRepository(db)
        user = user_repo.find_by_id(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        return jsonify({
            'success': True,
            'user': User.to_dict(user)
        }), 200
        
    except Exception as e:
        logger.error(f"Get user error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Failed to get user information',
            'error': str(e)
        }), 500
