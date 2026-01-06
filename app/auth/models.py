from datetime import datetime
from app.utils.helpers import validate_email


class User:
    """User model schema"""
    
    @staticmethod
    def validate_registration(data):
        """Validate user registration data"""
        errors = []
        
        if not data.get('email'):
            errors.append('Email is required')
        elif not validate_email(data.get('email', '')):
            errors.append('Invalid email format')
            
        if not data.get('password'):
            errors.append('Password is required')
        elif len(data.get('password', '')) < 6:
            errors.append('Password must be at least 6 characters')
            
        if not data.get('name'):
            errors.append('Name is required')
        elif len(data.get('name', '').strip()) < 2:
            errors.append('Name must be at least 2 characters')
            
        return errors

    @staticmethod
    def validate_login(data):
        """Validate user login data"""
        errors = []
        
        if not data.get('email'):
            errors.append('Email is required')
            
        if not data.get('password'):
            errors.append('Password is required')
            
        return errors

    @staticmethod
    def to_dict(user_doc):
        """Convert MongoDB document to dict"""
        if not user_doc:
            return None
            
        return {
            'id': str(user_doc['_id']),
            'email': user_doc['email'],
            'name': user_doc['name'],
            'created_at': user_doc['created_at'].isoformat()
        }
