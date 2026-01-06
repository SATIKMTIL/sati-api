from datetime import datetime
import re


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def sanitize_input(text):
    """Sanitize user input"""
    if not text:
        return text
    # Remove potentially harmful characters
    return text.strip()


def format_datetime(dt):
    """Format datetime to ISO string"""
    if isinstance(dt, datetime):
        return dt.isoformat()
    return dt


def paginate(items, page=1, per_page=50):
    """Helper function for pagination"""
    start = (page - 1) * per_page
    end = start + per_page
    return items[start:end]
