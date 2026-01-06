from functools import wraps
from flask import request, jsonify
from time import time
import logging

logger = logging.getLogger(__name__)

# Simple in-memory rate limiting
# For production, use Redis or a proper rate limiting library
rate_limit_store = {}


def rate_limit(max_requests=5, window_seconds=60):
    """
    Simple rate limiting decorator
    
    Args:
        max_requests: Maximum number of requests allowed in the time window
        window_seconds: Time window in seconds
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get client identifier (IP address or user agent)
            client_id = request.remote_addr or 'unknown'
            
            current_time = time()
            
            # Initialize client record if not exists
            if client_id not in rate_limit_store:
                rate_limit_store[client_id] = []
            
            # Remove old requests outside the window
            rate_limit_store[client_id] = [
                req_time for req_time in rate_limit_store[client_id]
                if current_time - req_time < window_seconds
            ]
            
            # Check if limit exceeded
            if len(rate_limit_store[client_id]) >= max_requests:
                logger.warning(f"Rate limit exceeded for client: {client_id}")
                return jsonify({
                    'success': False,
                    'message': f'Rate limit exceeded. Maximum {max_requests} requests per {window_seconds} seconds.',
                    'error': 'rate_limit_exceeded'
                }), 429
            
            # Add current request
            rate_limit_store[client_id].append(current_time)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def cleanup_rate_limit_store():
    """Cleanup old entries from rate limit store"""
    current_time = time()
    for client_id in list(rate_limit_store.keys()):
        rate_limit_store[client_id] = [
            req_time for req_time in rate_limit_store[client_id]
            if current_time - req_time < 3600  # Keep entries for 1 hour
        ]
        if not rate_limit_store[client_id]:
            del rate_limit_store[client_id]
